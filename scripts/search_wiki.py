#!/usr/bin/env python3
"""Search Wiki Markdown with standard-library BM25."""

import argparse
from collections import Counter
from dataclasses import dataclass
import math
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
HEADING = re.compile(r"^ {0,3}#{1,6}[ \t]+(.+?)\s*$")
FENCE = re.compile(r"^ {0,3}(`{3,}|~{3,})(.*)$")
LINK = re.compile(r"\[([^\]\n]+)\]\([^)\n]+\)")
CITATION = re.compile(r"\[(S[0-9]{2})\]")
TOKEN = re.compile(r"[^\W_]+", re.UNICODE)
STOP_WORDS = frozenset(
    "a an and are as at be between by difference different does for from has how i in is it of on or "
    "that the to was what when which who why with".split()
)
TOKEN_ALIASES = {"mfccs": "mfcc"}
SNIPPET_LENGTH = 440


@dataclass(frozen=True)
class Passage:
    path: str
    heading: str
    line: int
    blocks: tuple[str, ...]


@dataclass(frozen=True)
class SearchResult:
    path: str
    heading: str
    snippet: str
    score: float
    source_ids: tuple[str, ...]
    passage_id: str
    blocks: tuple[str, ...]
    passage_source_ids: tuple[str, ...]


def display_text(markdown: str) -> str:
    """Keep link labels and source markers visible without indexing URLs."""
    text = LINK.sub(
        lambda match: f"[{match[1]}]" if CITATION.fullmatch(f"[{match[1]}]") else match[1],
        markdown,
    )
    return " ".join(text.replace("`", "").replace("**", "").split())


def normalize_token(word: str) -> str:
    folded = word.casefold()
    return TOKEN_ALIASES.get(folded, folded)


def tokenize(text: str) -> list[str]:
    words = map(normalize_token, TOKEN.findall(text))
    return [word for word in words if word not in STOP_WORDS]


def passages_from_markdown(path: str, text: str) -> list[Passage]:
    passages = []
    heading = Path(path).stem
    line_number = 1
    lines: list[str] = []
    fence = ""

    def finish() -> None:
        blocks = []
        paragraph = []
        for line in [*lines, ""]:
            stripped = line.strip()
            if stripped.startswith("|") or not stripped:
                if paragraph:
                    blocks.append(display_text(" ".join(paragraph)))
                    paragraph.clear()
                if stripped.startswith("|") and not re.fullmatch(r"[|:\s-]+", stripped):
                    blocks.append(display_text(stripped.strip("|").replace("|", " · ")))
            else:
                paragraph.append(stripped)
        if blocks:
            passages.append(Passage(path, heading, line_number, tuple(blocks)))

    for number, line in enumerate(text.splitlines(), 1):
        marker = FENCE.match(line)
        if fence:
            if marker and marker[1].startswith(fence) and not marker[2].strip():
                fence = ""
            continue
        if marker:
            fence = marker[1]
            continue
        match = HEADING.match(line)
        if match:
            finish()
            heading = display_text(re.sub(r"\s+#+$", "", match[1]))
            line_number = number
            lines.clear()
        else:
            lines.append(line)
    finish()
    return passages


def load_passages(root: Path = ROOT) -> list[Passage]:
    root = root.resolve()
    wiki = root / "wiki"
    passages = []
    for path in sorted(wiki.rglob("*.md")):
        resolved = path.resolve()
        if resolved.is_relative_to(wiki) and resolved.suffix == ".md" and path.is_file():
            passages.extend(passages_from_markdown(
                path.relative_to(root).as_posix(), path.read_text(encoding="utf-8")
            ))
    return passages


def make_result(passage: Passage, score: float, weights: dict[str, float]) -> SearchResult:
    def relevance(block: str) -> float:
        words = set(tokenize(block))
        return sum(weight for term, weight in weights.items() if term in words)

    block = max(passage.blocks, key=relevance)
    remaining = weights.keys() - set(tokenize(block))
    # A comparison may need two paragraphs from the same heading.
    extra = max(passage.blocks, key=lambda item: sum(
        weight for term, weight in weights.items() if term in remaining and term in tokenize(item)
    ))
    if remaining.intersection(tokenize(extra)) and len(block) + len(extra) + 1 <= SNIPPET_LENGTH:
        block = f"{block} {extra}"
    source_ids = set(CITATION.findall(block + " " + passage.heading))
    source_path = re.fullmatch(r"wiki/sources/(S[0-9]{2})\.md", passage.path)
    if source_path:
        source_ids.add(source_path[1])

    snippet = block
    if len(block) > SNIPPET_LENGTH:
        match = max(TOKEN.finditer(block), key=lambda item: weights.get(normalize_token(item[0]), 0),
                    default=None)
        start = 0 if match is None else max(0, match.start() - 70)
        if start:
            start = block.rfind(" ", 0, start + 1) + 1
        end = start + SNIPPET_LENGTH
        if end < len(block):
            boundary = block.rfind(" ", start, end)
            if boundary > start:
                end = boundary
        snippet = ("…" if start else "") + block[start:end] + ("…" if end < len(block) else "")
    passage_sources = source_ids | set(CITATION.findall(" ".join(passage.blocks)))
    return SearchResult(
        passage.path, passage.heading, snippet, score, tuple(sorted(source_ids)),
        f"{passage.path}#L{passage.line}", passage.blocks, tuple(sorted(passage_sources)),
    )


def search(query: str, *, root: Path = ROOT, limit: int = 5) -> list[SearchResult]:
    terms = sorted(set(tokenize(query)))
    if not terms or limit <= 0:
        return []
    passages = load_passages(root)
    if not passages:
        return []

    counts = [
        Counter(tokenize(f"{p.heading} {p.heading} {' '.join(p.blocks)}"))
        for p in passages
    ]
    document_frequency = Counter(term for count in counts for term in count)
    weights = {
        term: math.log1p((len(counts) - document_frequency[term] + 0.5)
                         / (document_frequency[term] + 0.5))
        for term in terms
    }
    average_length = sum(count.total() for count in counts) / len(counts) or 1
    scores = []
    for passage, count in zip(passages, counts):
        norm = 1.5 * (0.25 + 0.75 * count.total() / average_length)
        score = 0.0
        for term in terms:
            if frequency := count[term]:
                score += weights[term] * (frequency * 2.5 / (frequency + norm))
        if score > 0:
            scores.append((score, passage))

    scores.sort(key=lambda item: (-item[0], item[1].path, item[1].line))
    return [make_result(passage, score, weights) for score, passage in scores[:limit]]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("query", nargs="?", default="", help="English search terms")
    parser.add_argument("--limit", type=int, default=5, help="maximum results (default: 5)")
    args = parser.parse_args()
    if args.limit < 1:
        parser.error("--limit must be at least 1")
    results = search(args.query, limit=args.limit)
    if not results:
        print("No matching Wiki passages. Try English terms or a different query.")
    for result in results:
        sources = ", ".join(f"[{sid}]" for sid in result.source_ids) or "none"
        print(f"{result.path} | {result.heading} | score {result.score:.6f} | sources {sources}")
        print(f"  {result.snippet}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    main()
