# Stage 5 final evaluation and submission audit

**Audit date** — 2026-11-21 (Asia/Taipei)
**Audited revision** — `b00ff4d`, Stage 4 merge. The working tree was clean at the start of the audit.

## Readiness decision

The repository is ready for submission as a reproducible local Wiki and teaching presentation. It contains seven registered and ingested sources, six Wiki chapters, and a 12-slide Traditional Chinese presentation. The fresh headless Chrome run passed under a Pages-style HTTP subpath. Live GitHub Pages status, live LLM answer quality, assistive technology behavior, and physical-device coverage are outside the verified submission evidence. The UAR formula remains outside the approved teaching content, so the full original evaluation objective is only partly met.

## Material examined

| Area | Files or records inspected |
|---|---|
| Project contract and history | [AGENTS.md](../AGENTS.md), [README](../README.md), [scope](01_scope.md), [workflow graphs](04_workflow.md), and the scaffold, Stage 2, Stage 3 and Stage 4 revisions |
| Ingestion and lint | [Canonical registry](sources.json), [human-readable registry](02_sources.md), [Wiki index](../wiki/index.md), all six chapter files, the [S01–S07 source records](../wiki/sources/), [ingestion log](../logs/ingest.md), [lint log](../logs/lint.md), and seven local PDF hashes |
| Query | [Retriever](../scripts/search_wiki.py), [answer workflow](../scripts/answer_wiki.py), [retrieval tests](../tests/test_search_wiki.py), [answer tests](../tests/test_answer_wiki.py), [query log](../logs/query.md), and a read-only summary of the ignored local `logs/answer-runs.log` |
| Teaching and presentation | [Slide data](../data/slide-content.json), [traceability matrix](03_slide_map.md), [slide-content checker](../scripts/check_slide_content.py), [renderer](../scripts/build_presentation.py), [entry point](../slides/index.html), [stylesheet](../slides/presentation.css), [browser code](../slides/presentation.js), [browser test](../tests/smoke_presentation.mjs), and [validation log](../logs/slide-validation.md) |
| Automation | [Wiki validation workflow](../.github/workflows/validate.yml) and [Pages workflow](../.github/workflows/deploy-pages.yml) |

## Executed checks

The fresh runs used Windows, Python 3.15.2, Node 26.13.1, and headless Chrome 157.0.8103.79. Runtime and browser checks are distinguished below from structure, deterministic content checks, and manual review.

| Command or inspection | Kind | Actual result |
|---|---|---|
| `python -B scripts/check_wiki.py` | Stage 2 deterministic | Pass. Seven verified sources, 14 Wiki pages, six chapters and 35 evidence pointers. Checks include UTF-8, repository-local link targets, reachability, registry agreement and reciprocal evidence mappings. |
| SHA-256 comparison and `git check-ignore` for `raw/S01.pdf` through `raw/S07.pdf` | Stage 2 integrity | All seven files were present, ignored by Git and matched the recorded hashes. S01's baseline hash is in the ingest log. S02–S07 hashes are in their source records. This confirms file identity against the records. The audit did not repeat full-paper verification. |
| `python -B -m unittest discover -s tests -v` | Stage 3 automated | All 17 passed: eight retrieval tests and nine answer-workflow tests. Model responses were scripted, including the subprocess adapter round trip. |
| Five direct calls to `answer(..., dry_run=True)` | Stage 3 real local execution | MFCC retrieved cited text. The combined dataset question missed its IEMOCAP design passage at limit 5 and recovered it at limit 6. An unrelated capital question returned insufficient evidence. UAR retrieved related metrics without establishing the requested formula. Zero generation attempts and zero correction retries. |
| `python -B scripts/check_slide_content.py` | Stage 4 deterministic | Pass. Replayed 13 Stage 3 queries and checked 31 exact claim-to-evidence mappings across 12 slides, verified source locators, quiz answers, and synthetic arithmetic. |
| `python -B scripts/build_presentation.py --check` | Stage 4 deterministic | Pass. Rendered in memory and matched the checked-in `slides/index.html`. It was unnecessary to rewrite the published artifact. |
| `node --check slides/presentation.js` | Static JavaScript | Pass. |
| `node tests/smoke_presentation.mjs "C:/Program Files/Google/Chrome/Application/chrome.exe"` | Stage 4 browser | Pass on the first audit run. The browser served the deck at a local `/ser-llm-wiki/` path. It compared rendered content, all 31 citations and seven reference URLs, exercised navigation, focus, keyboard controls, progress, diagrams and quiz, and found zero console errors or missing local assets. All 36 slide/viewport pairs at 1440, 390 and 320 CSS pixels passed the sampled contrast, font-size and horizontal-overflow checks. Reduced-motion and JavaScript-disabled reading passed. |
| `git diff --check` | Repository hygiene | Pass. |

## Implemented workflows and validation timing

| Workflow | Implemented nodes and evidence | Gate and ownership |
|---|---|---|
| Ingest | Select and discuss source → acquire and compare full text, metadata and rights → extract located evidence → review against the source → update the chapter, source record and registry → log and lint. Stage 2 records seven completed ingestions. | Human source review precedes registry verification. The expanded linter checks the resulting pointers. PDF acquisition, evidence review and registry edits are recorded human work. |
| Query | BM25 ranks heading-level Wiki passages → Stage 3 checks for source-linked passages → when an adapter is configured, semantic sufficiency precedes generation → deterministic citation membership precedes semantic claim review → withhold or release → log. | The CLI accepts a JSON subprocess adapter and an optional separate reviewer. One initial generation and two correction retries are enforced. Dry runs end before generation and semantic checks. |
| Lint | Compare registry and records → check chapter navigation and links → check exact source/locator pairs in both directions → report structural failures. | The GitHub Actions validate workflow runs Wiki lint on pushes and pull requests. Scientific accuracy, duplication in meaning, and publisher URL availability still require separate review. |
| Slide generation | Select teaching objectives → query the Wiki → draft the Traditional Chinese dataset and traceability map → replay retrieval and review claim meaning → render static HTML → run browser smoke tests → repair and recheck. | Task 2 and Task 3 logs record evidence validation before HTML generation. The browser suite verifies rendered content and behavior separately. The renderer and Pages workflow do not invoke the evidence checker. The Pages workflow checks for the entry point and uploads the already-built folder. |

### Observed changes versus recommendations

| Implemented change | Evidence of improvement or earlier validation | Remaining boundary |
|---|---|---|
| Expanded Wiki lint | The scaffold at `64a74de` checked basic registry shape and Wiki links. Stage 2 added chapter reachability and source evidence reciprocity. Its first expanded run exposed locator and encoding issues missed by the scaffold. This broadened the post-ingest gate and made it repeatable in CI. | It cannot establish PDF contents or entailment. |
| Query sufficiency and citation gates | The Stage 3 answer path checks source-linked evidence before model generation. It rejects bad citation membership before semantic review and caps correction attempts before release. Fixture runs demonstrate both orders. | Live adapter judgments and adversarial resistance were not measured. |
| Pre-HTML evidence validation | The authored dataset and replay checker made the documented pre-HTML gate executable. A malformed slide 5 locator was corrected at the content gate, before the renderer was used. | Earlier validation was implemented and exercised locally. It is not a mandatory Pages or renderer gate. Adding CI checks would be a future improvement. |
| Repeatable presentation QA | Chrome initially exposed harness and resource issues. The final smoke test traces DOM content to the artifact while exercising a real browser on a project subpath. | This is local headless Chrome evidence. A deployed smoke test and an assistive technology pass remain future work. |
| Retrieval and provenance fixes | Normalized singular/plural MFCCs and retained both sides of the mel-spectrogram comparison. The current audit reproduced relevant MFCC results. Increasing the comparison result limit recovered the IEMOCAP design passage. | The latter is a retrieval workaround. Default top-five ranking did not change for that query. |

## Evidence coverage and generation provenance

The registry and source records agree on S01–S07. The fresh browser test confirmed that all seven rendered reference URLs match the verified registry, and the content replay linked every claim to the exact retrieved block and a registered source-record locator. Publisher endpoints were not fetched in this audit. The existing Stage 4 semantic review is a manual Wiki-based review, and deterministic checks replay its evidence selection. The audit checked the scoped distinctions in the approved artifact: RAVDESS percentages are human judgments, the original wav2vec 2.0 result concerns ASR, and the F0/speaking-rate idea is a proposal. The worksheet matrix is labeled synthetic.

| Wiki chapter | Main teaching coverage |
|---|---|
| 1. SER fundamentals | Slides 1–2 and 12, including SER versus ASR and the limits of pitch alone |
| 2. Acoustic signals and features | Slides 3–4, including waveform, sampling, pitch, signal energy, mel spectrograms and MFCCs |
| 3. Emotion representations | Slide 5, categorical labels and valence–arousal |
| 4. Models and learned representations | Slides 6–8, a feature pipeline, CNN/LSTM, and pretrained representations |
| 5. Datasets and evaluation | Slides 9–10, RAVDESS, IEMOCAP, held-out sessions, the synthetic matrix, accuracy, precision, recall and F1 |
| 6. Applications and limitations | Slide 11, transfer conditions, bias, children's data, consent and privacy |

The Stage 3 logs distinguish real retrieval and control flow from mocked generation and semantic review. The ignored local operational log had 22 entries at audit time: 14 `dry_run` results and eight `insufficient_evidence` results, all in dry-run mode and with zero generation attempts. These counts describe this checkout's log rather than completeness across other machines. Stage 4 recorded 13 dry retrieval calls, zero generation attempts, and human preparation and review of 31 teaching statements. There is no verifiable live LLM execution in the examined records.

## Observed failures and retries

Counts below are deduplicated issue episodes evidenced by the historical records. A failed batch is counted once when the log describes one underlying cause. Expected negative fixtures, warning-only events, and an issue found by inspection are tracked separately from failed executions. Log coverage is uneven, so the counts do not estimate failure rates or establish the overall highest-risk node.

| Node | Observed failed execution or missing evidence | Correction and recorded retry count |
|---|---|---|
| Ingest source access or extraction | **5 episodes.** S01 package installation failed, Word automation returned `0x80070520`, and the web PDF returned a cache miss. S05 exceeded the PDF parser's content-stream limit. S06's publisher reader returned HTTP 403. | S01 used direct local extraction and publisher HTML. Its aggregate retry count was not recorded. S05 used PyMuPDF and recovered on one extraction retry with zero claim-validation or lint retries. S06 used the available local full text with zero retries. S02 and S03 reader warnings are excluded from the failure count. |
| Wiki structural lint | One failed expanded-check run with two causes: an ASCII replacement of an em dash and missing precise pointers for two S01 chapter citations. | Corrected the Unicode comparison and added specific evidence rows. Both cleared on the first retry. |
| Query CLI and retrieval | Three episodes: the empty argument produced a PowerShell usage error, singular MFCC missed, and the default top five missed IEMOCAP design evidence. | Optional CLI input resolved the shell error on its first retry. MFCC normalization fixed the miss without a recorded numeric retry count. The larger-limit follow-up recovered the dataset passage, with zero answer corrections. |
| Slide evidence validation | One failed check, where adjacent bullets contaminated a slide 5 locator. The UAR formula is a separate evidence gap. | Exact per-claim locators passed after one correction. One UAR re-query still lacked evidence, so the formula was excluded. |
| Browser QA | **4 episodes.** The asset matcher used a malformed escape, sandboxed Chrome exited, simulated Enter failed to open a quiz item, and one HTTP run produced three icon-related 404 errors. | Fixed the matcher and reran. The first approved Chrome run passed. Enter input and the inline icon each cleared on their first correction retry. An additional presentation issue found by inspection, the missing valence–arousal example markers, passed its first post-repair check. |
| Scripted negative validation | Missing source ID, nonexistent passage and injected 99% IEMOCAP accuracy. These are deliberate fixtures and are excluded from the operational counts. | Missing source ID was corrected in one retry. Repeated invalid or unsupported fixtures were withheld after two corrections, with no released claims. |

**Highest observed count under this counting rule:** source access and extraction, five episodes. Browser QA has four failed executions, plus the separately discovered visualization defect. If that inspection finding is included in a broader presentation-and-QA bucket, the two buckets tie at five. The logs do not provide consistent denominators, exact S01 retry totals, or a complete per-attempt event stream, so a definitive project-wide ranking is unavailable.

## Remaining limitations

- **Coverage:** The UAR formula remains unapproved. The S04 manuscript and publisher pagination differ, S05's byline variation is recorded, and S07's conflicting corpus totals are excluded from teaching claims. The review evidence should not be read as comparable cross-study SER performance.
- **Queries:** Retrieval is lexical. Short or mixed-topic queries can rank overview material or metadata above direct evidence, and Chinese word segmentation is unavailable. Dry-run source membership cannot decide semantic sufficiency.
- **Deployment and accessibility:** The deck passed a local Pages-style HTTP test. Live deployment, external reference availability, physical devices, other browser engines and screen readers were not verified. Sampled contrast and focus checks are not a full accessibility audit.
- **Automation and records:** CI runs Wiki lint, while the pre-HTML evidence check and browser test are separate commands. If stronger submission assurance is required, archive a deployed smoke result, run a controlled live adapter evaluation and log comparable per-node attempts. These are recommendations rather than changes made in Stage 5.

The audit added only this report. The original logs, Wiki, slide dataset, presentation, scripts and workflows were preserved. No commit or push was made.
