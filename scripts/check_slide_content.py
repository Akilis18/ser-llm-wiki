#!/usr/bin/env python3
"""Check slide structure and replay evidence retrieval. Semantic review is separate."""

import argparse
import json
from pathlib import Path
import sys

if __package__:
    from .answer_wiki import ROOT, answer
    from .check_wiki import EVIDENCE
else:
    from answer_wiki import ROOT, answer
    from check_wiki import EVIDENCE


CLAIM_KINDS = {
    "concept", "research_method", "research_finding", "research_proposal",
    "review_synthesis", "review_recommendation",
}
VISUAL_KINDS = {"diagram", "teaching_example", "synthetic_data", "quiz"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def check_synthetic(visual: dict) -> None:
    data = visual["data"]
    labels, counts = data["labels"], data["counts"]
    require("合成資料" in visual["description"], "Synthetic data must be visibly labeled")
    require(len(labels) == len(counts) >= 2 and len(set(labels)) == len(labels)
            and all(nonempty(label) for label in labels), "Invalid synthetic class labels")
    require(all(len(row) == len(labels) and all(type(n) is int and n >= 0 for n in row)
                for row in counts), "Invalid synthetic confusion matrix")
    diagonal = [row[i] for i, row in enumerate(counts)]
    total = sum(map(sum, counts))
    index = labels.index(data["recall"]["label"])
    support = sum(counts[index])
    require(total > 0 and support > 0, "Synthetic metric denominators must be positive")
    require(data["accuracy"] == {"numerator": sum(diagonal), "denominator": total}
            and data["recall"] == {"label": labels[index], "numerator": diagonal[index],
                                   "denominator": support}, "Synthetic metrics do not match counts")


def validate(data: dict) -> tuple[int, int, int]:
    require(data["language"] == "zh-Hant" and all(nonempty(data[k]) for k in ("title", "audience")),
            "Missing Traditional Chinese presentation metadata")
    require(data["review_method"] == "manual_wiki_claim_review", "Missing semantic review method")
    slides = data["slides"]
    require([s["number"] for s in slides] == list(range(1, 13)), "Expected ordered slides 1–12")
    registry = json.loads((ROOT / "docs/sources.json").read_text(encoding="utf-8"))
    source_records = {}
    for row in registry:
        if row["status"] == "verified":
            sid = row["id"]
            path = ROOT / "wiki/sources" / f"{sid}.md"
            source_records[sid] = {(source, (path.parent / page).resolve(), location)
                                   for source, location, page in EVIDENCE.findall(
                                       path.read_text(encoding="utf-8"))}

    claim_ids = set()
    query_count = evidence_count = 0
    used_sources = set()
    for slide in slides:
        label = f"Slide {slide['number']}"
        require(all(nonempty(slide[key]) for key in ("title", "explanation"))
                and isinstance(slide["learning_objectives"], list)
                and bool(slide["learning_objectives"])
                and all(map(nonempty, slide["learning_objectives"])), f"{label}: missing teaching content")
        visual = slide["visual"]
        require(visual["kind"] in VISUAL_KINDS and nonempty(visual["description"]),
                f"{label}: invalid visual")
        if visual["kind"] == "synthetic_data":
            check_synthetic(visual)
        require(0 <= slide["correction_retries"] <= 2
                and len(slide["retrieval"]) == slide["correction_retries"] + 1,
                f"{label}: retrieval retry count mismatch")
        passages = {}
        for record in slide["retrieval"]:
            require(nonempty(record["query"]) and type(record["limit"]) is int
                    and record["limit"] >= 1, f"{label}: invalid query")
            result = answer(record["query"], dry_run=True, limit=record["limit"])
            require(record["status"] == result["status"] and result["attempts"] == []
                    and record["deterministic_sufficiency"] == result["sufficiency"]["deterministic"]
                    and record["semantic_sufficiency"] == result["sufficiency"]["semantic"]
                    and record["retrieved_ids"] == [p["passage_id"] for p in result["retrieved"]],
                    f"{label}: retrieval record differs from replay")
            passages.update({p["passage_id"]: p for p in result["retrieved"]
                             if p["passage_id"] in result["eligible_ids"]})
            query_count += 1

        require(isinstance(slide["key_points"], list) and bool(slide["key_points"]),
                f"{label}: missing claims")
        slide_claim_ids = set()
        for claim in slide["key_points"]:
            cid = claim["id"]
            require(nonempty(cid) and cid not in claim_ids and nonempty(claim["text"])
                    and claim["kind"] in CLAIM_KINDS and isinstance(claim["evidence"], list)
                    and bool(claim["evidence"]), f"{label}: invalid claim {cid}")
            slide_claim_ids.add(cid)
            claim_ids.add(cid)
            for ref in claim["evidence"]:
                passage = passages.get(ref["passage_id"])
                sid, loc = ref["source_id"], ref["location"]
                require(passage is not None and ref["path"] == passage["path"]
                        and sid in passage["source_ids"] and sid in source_records,
                        f"{cid}: unknown or unverified evidence")
                index = ref["block"]
                require(type(index) is int and 1 <= index <= len(passage["blocks"])
                        and ref["excerpt"] == passage["blocks"][index - 1]
                        and nonempty(loc) and f"[{sid}], {loc}." in ref["excerpt"],
                        f"{cid}: cited block or location differs from the retrieved Wiki")
                require((sid, (ROOT / ref["path"]).resolve(), loc) in source_records[sid],
                        f"{cid}: locator is missing from the verified source record")
                used_sources.add(sid)
                evidence_count += 1
        if visual["kind"] == "quiz":
            require(bool(slide["quiz"]) and all(nonempty(q["question"])
                    and q["answer_claim_id"] in slide_claim_ids for q in slide["quiz"]),
                    f"{label}: quiz answer does not map to a reviewed claim")

    require(set(slides[-1]["reference_sources"]) == used_sources,
            "Reference slide does not list exactly the sources used")
    for item in data["unapproved"]:
        require(item["status"] == "unapproved" and 1 <= item["slide"] <= len(slides)
                and 0 <= item["correction_retries"] <= slides[item["slide"] - 1]["correction_retries"]
                and nonempty(item["topic"]) and nonempty(item["reason"]),
                "Invalid unapproved-topic record")
    return len(claim_ids), evidence_count, query_count


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("path", nargs="?", type=Path, default=ROOT / "data/slide-content.json")
    args = parser.parse_args()
    try:
        claims, evidence, queries = validate(json.loads(args.path.read_text(encoding="utf-8")))
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(f"Slide content check failed: {error}", file=sys.stderr)
        return 1
    print(f"Deterministic checks passed: 12 slides, {claims} claims, {evidence} evidence mappings, "
          f"{queries} Stage 3 query replays. Semantic support requires review.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
