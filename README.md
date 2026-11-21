# SER LLM Wiki

**AI 如何聽出情緒？從聲音特徵到深度學習的語音情緒辨識入門**

A source-grounded Markdown knowledge base about Speech Emotion Recognition (SER), inspired by [Karpathy's LLM Wiki proposal](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The HTML teaching presentation is generated *from the verified Wiki*, not directly from the source papers.

## Status

- [x] Repository scaffold and source manifest
- [x] Discuss and ingest at least five complete source documents (target: seven)
- [ ] Query and lint the Wiki with logged evidence
- [x] Generate and test interactive HTML slides
- [ ] Deploy the presentation to GitHub Pages
- [ ] Record a real workflow revision and reflection

**Seven of seven references are verified.** See the [Wiki index](wiki/index.md) for current chapter coverage. Original PDFs should be obtained from their publishers or authors where allowed. Do not commit copies you lack permission to redistribute. Git ignores the `raw/` folder.

## Structure

- `AGENTS.md`: behavioral contract for coding and Wiki agents
- `docs/`: scope, syllabus, workflows, source-to-slide mapping
- `raw/`: local source PDFs/text (not tracked)
- `wiki/`: maintained Markdown pages with source references
- `wiki/sources/`: one ingestion record per source
- `logs/`: real query, lint, validation and correction logs
- `scripts/`: deterministic project checks
- `slides/`: standalone GitHub Pages presentation

## First actions

1. Review `docs/01_scope.md` and `docs/02_sources.md` together before generation.
2. Download full research texts to `raw/` locally; check each source title and metadata.
3. Ingest one source at a time following `AGENTS.md`, saving an entry in `logs/ingest.md`.
4. Run `python scripts/check_wiki.py` to inspect ingestion coverage and links.
5. Generate teaching content from verified Wiki pages only.

## Search the Wiki

```bash
python scripts/search_wiki.py "spectrogram frequency" --limit 3
python -m unittest discover -s tests -v
```

The search command uses standard-library Python and rebuilds its index from Markdown under `wiki/`, including source records. BM25 ranks passages by words in their heading and text. Each result includes a repository-relative path, heading, snippet, score, and any source IDs associated with the snippet or source record. Equal scores are ordered by path and heading position.

Use English keywords or technical terms such as `MFCC` and `wav2vec`. Chinese text is read as Unicode, but the search has no Chinese word segmentation or translation. A Chinese-only query will usually miss the English Wiki. Try the English term or include the English acronym in a mixed query. Scores indicate lexical relevance. Check the returned passage and source citation before relying on it, particularly when only some query terms match.

See the [query validation log](logs/query.md) for examples run against this Wiki.

## Answer questions from the Wiki

```bash
python scripts/answer_wiki.py "What is MFCC?" --dry-run
python scripts/answer_wiki.py "What is MFCC?" --model-command python --model-arg path/to/adapter.py
```

Without an adapter the CLI defaults to dry run. It lists retrieved passage IDs and source IDs and records whether source-linked evidence was found. It skips generation and semantic review. Use `--json` to inspect the full result and retrieved blocks.

The adapter reads one UTF-8 JSON object on stdin and writes one JSON object to stdout per call. Route by `phase` (`sufficiency`, `generate`, or `validate`). Pass the supplied instructions and fields to your model, using the `passages` as its factual context. Each phase's instructions define the required JSON response. Repeat `--model-arg` for extra executable arguments. By default the same adapter handles generation and review. To configure a separate reviewer, pass `--review-command` and repeat `--review-arg` as needed.

Deterministic validation checks that every claim has a retrieved passage ID and a source ID present in that passage. Semantic review evaluates whether the cited words support the claim and whether the answer addresses the question. A review pass is a model judgment. The workflow allows one initial generation and up to two corrections. Unresolved validation failures and adapter errors exit with status 1.

Each invocation appends a JSON record to the local, Git-ignored `logs/answer-runs.log`. It includes the question, passage IDs, actual check outcomes, retries and any accepted claims. Use `--log` to choose the destination. A configured adapter receives the question and retrieved Wiki text.

## Local preview

Open [the presentation](slides/index.html) in a browser, or serve it locally:

```bash
python -m http.server 8000
# Open http://localhost:8000/slides/
```

Use the previous and next buttons, the left and right arrow keys, or the slide menu. Each citation can reveal its Wiki passage, source location, and supporting excerpt. With JavaScript disabled, the twelve slides appear in reading order and the evidence and quiz answers remain expandable.

The published folder contains its own HTML, CSS, and JavaScript. After an approved change to the [slide dataset](data/slide-content.json), run the content checker before rebuilding:

```bash
python -B scripts/check_slide_content.py
python -B scripts/build_presentation.py
python -B scripts/build_presentation.py --check
node tests/smoke_presentation.mjs "/path/to/chrome"
```

The browser smoke test requires Node and a local Chromium-family browser. Set `CHROME_BIN` or pass the executable path. See the [validation log](logs/slide-validation.md) for coverage and limitations.

## Deployment

The included `.github/workflows/deploy-pages.yml` publishes `slides/` from `main` using GitHub Actions. In repository **Settings → Pages**, set **Build and deployment → Source: GitHub Actions**. The workflow uploads the self-contained `slides/` folder directly.
