# Agent instructions — SER LLM Wiki

## Mission
Maintain an auditable, source-grounded Speech Emotion Recognition Wiki, then generate an accessible beginner-friendly HTML presentation exclusively from checked Wiki material.

## Design rule: discuss before generating
Before the first ingest, agree on scope, audience, teaching goals and the meaning of each chapter. Before each source ingest, briefly explain the paper's role, limitations and proposed Wiki changes. Await user approval when decisions materially alter scope.

## Source-grounding requirements
1. Treat `docs/sources.json` as the reference registry. `planned` means **not ingested**.
2. Do not claim to have read or ingested a source without accessing its full relevant text.
3. Separate paper claims, general explanatory analogies and proposed examples. Attribute factual paper claims with `[Sxx]` and a precise section/page when possible.
4. Never fabricate quotations, metrics, results, paper content, file paths or test outcomes.
5. For papers about representation learning (e.g. wav2vec 2.0), distinguish their original task from SER downstream uses.
6. Preserve important disagreements between sources; do not silently reconcile contradictions.
7. Keep raw inputs unchanged; do not commit restricted PDF copies.

## Ingest operation
- Read and discuss a source; verify title/authors/venue and rights.
- Extract independently checkable claims with locations in the source.
- Compare existing pages; update concepts and cross-links rather than writing isolated paper summaries only.
- Add `wiki/sources/Sxx.md` with the true ingestion status, claims and locations.
- Update registry status only when ingestion is complete and checked.
- Log date, input, changed files, validation results and unresolved questions.

## Query operation
- Search Wiki pages and source records first, not original PDFs.
- Return answers with Wiki page paths and `[Sxx]` references.
- If Wiki coverage is insufficient, report a knowledge gap; propose additional ingestion instead of guessing.

## Lint operation
- Check broken local Markdown links, unsupported factual claims, missing source locations, duplicate/contradictory explanations, orphan pages and missing chapters.
- Record actual detected failures and fixes in `logs/lint.md`.

## Slide-generation contract
- Source slides solely from verified Wiki pages; log source-to-slide traceability in `docs/03_slide_map.md`.
- Teaching progression: motivation → audio features → emotion representation → models → datasets/evaluation → limitations → review.
- Use clear beginner explanations and label any synthetic demo data.
- Validate citations **before** HTML generation; independently validate HTML navigation and responsive layout afterward.
- Use bounded retries (maximum 2 attempts per failure, then log and escalate).

## Safety and scientific clarity
SER predictions are uncertain and context-dependent. Do not imply pitch, loudness or one waveform uniquely determines emotion. Avoid presenting SER as a reliable diagnostic, lie detector or direct measure of private mental states.

## Deliverables
At least 5 genuinely ingested sources; 6 structured Wiki chapters; a working presentation; verifiable query/lint/HTML checks; and a reflection grounded in real recorded failures.
