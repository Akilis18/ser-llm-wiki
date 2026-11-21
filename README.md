# SER LLM Wiki

**AI 如何聽出情緒？從聲音特徵到深度學習的語音情緒辨識入門**

A source-grounded Markdown knowledge base about Speech Emotion Recognition (SER), inspired by [Karpathy's LLM Wiki proposal](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f). The HTML teaching presentation is generated *from the verified Wiki*, not directly from the source papers.

## Status

- [x] Repository scaffold and source manifest
- [x] Discuss and ingest at least five complete source documents (target: seven)
- [ ] Query and lint the Wiki with logged evidence
- [ ] Generate, test, and deploy interactive HTML slides
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

## Local preview

```bash
python -m http.server 8000
# Open http://localhost:8000/slides/
```

## Deployment

The included `.github/workflows/deploy-pages.yml` publishes `slides/` from `main` using GitHub Actions. In repository **Settings → Pages**, set **Build and deployment → Source: GitHub Actions**. The current HTML is only a Stage 1 placeholder; a teaching presentation has not been produced or deployed.
