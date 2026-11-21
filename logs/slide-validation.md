# Slide validation log

## 2026-11-21 · Stage 4 Task 1 content validation

Inputs were the Stage 3 `scripts.answer_wiki.answer(..., dry_run=True, limit=10)` results and their retrieved Wiki blocks. The authoring pass recorded 13 accepted retrieval runs for 12 slides, including one follow-up query for slide 10. Every dry run found source-linked text. Dry-run semantic sufficiency was skipped and generation attempts were zero. No live model, PDFs, or external pages were used. The [dataset](../data/slide-content.json) retains the query strings, rank-ordered passage IDs, evidence excerpts, source IDs, locators, and retry counts. The [traceability matrix](../docs/03_slide_map.md) lists the evidence for each teaching point.

### Deterministic checks

| Check | Actual result |
|---|---|
| `python -B scripts/check_slide_content.py` | Passed. Checked 12 slides, 31 claims, 31 exact evidence mappings and 13 Stage 3 query replays. Also checked verified source records, quiz references and the synthetic metrics. |
| Targeted negative fixtures | Four passed. The checker rejected an unretrieved passage, an incorrect locator, a wrong synthetic metric, and a quiz answer with an unknown claim ID. The fixtures were mutated in memory. |
| `python -B -m unittest discover -s tests -v` | All 17 tests passed. |
| `python -B scripts/check_wiki.py` | Passed with 7 verified sources, 14 Wiki pages, 6 chapters, and 35 evidence pointers. |
| `git diff --check` | Passed. |
| `git diff --exit-code -- wiki raw slides scripts/search_wiki.py scripts/answer_wiki.py` | Passed. No changes in these paths. |

The first slide-content checker run rejected claim 05.1. The locator extraction had captured part of the next bullet because the retriever groups adjacent bullet lines into one block. Replaced the two slide 5 locators with their individual entries and checked each locator within the exact retrieved block. The first correction retry passed. No retrieval changes were required for this issue.

### Manual semantic review

Reviewed all 31 Traditional Chinese claims against their selected English Wiki blocks and checked the quiz keys and teaching visuals against those claims. Confirmed that the RAVDESS percentage is an aggregate human identification result, the wav2vec 2.0 example separates the original ASR objective from downstream SER, and the F0 statistics idea remains a research proposal. The confusion matrix is labeled synthetic. Its two fractions are computed from its example counts using the checked metric definitions. The validator checks pointers and arithmetic. The manual review assesses meaning and scope.

| Slide | Approved claims | Source coverage |
|---|---:|---|
| 1 | 1 | S01 |
| 2 | 2 | S01 |
| 3 | 1 | S02 |
| 4 | 4 | S01, S02, S07 |
| 5 | 2 | S01 |
| 6 | 3 | S01, S02 |
| 7 | 2 | S07 |
| 8 | 3 | S01, S05 |
| 9 | 3 | S03, S04 |
| 10 | 3 | S01, S06 |
| 11 | 4 | S01, S06, S07 |
| 12 | 3 | S01 for the recap and quiz. References list all seven sources used across the deck. |

### Unapproved material

The initial evaluation-metrics query and one follow-up found checked definitions for accuracy, precision, recall, and class F1. The retrieved material gave no checked UAR formula. UAR is recorded as unapproved and excluded from the slide's teaching claims. The deck is ready for HTML implementation using the approved content. Browser navigation, responsive layout, and accessibility checks remain for the HTML stage.

## 2026-11-21 · Stage 4 Task 2 presentation validation

Ran the slide-content checker before generating HTML. It passed with 12 slides, 31 claim mappings and 13 Stage 3 query replays. The build used the validated JSON for scientific text and the verified registry for bibliographic titles and links. The source dataset, Wiki, and Pages workflow were preserved.

| Check | Actual result |
|---|---|
| `python -B scripts/build_presentation.py --check` | Generated HTML matched the validated dataset and renderer. |
| `node --check slides/presentation.js` | Passed. |
| `node tests/smoke_presentation.mjs "C:/Program Files/Google/Chrome/Application/chrome.exe"` | Passed on Windows in headless Chrome 157.0.8103.79. Checked local assets, all 31 displayed claim texts and source/passage mappings, seven references, buttons, arrow keys, focus, progress, reference navigation and browser Back. Exercised the waveform, valence–arousal plot, pipeline details, confusion-matrix exercise and quiz. |
| Responsive and accessibility smoke checks | All 12 slides passed horizontal overflow and sampled font-size checks at 1440, 390, and 320 CSS pixels. Slider arrow keys adjusted the waveform instead of changing slides. Reduced-motion mode disabled the slide animation. The no-JavaScript run exposed all 12 slides in reading order and disabled the waveform slider. |
| `python -B -m unittest discover -s tests -v` and `python -B scripts/check_wiki.py` | Passed. The Python suite ran 17 tests, and structural lint found 7 verified sources and 35 evidence pointers. |
| `git diff --check` | Passed. |

The first asset smoke check found a malformed word-boundary escape in the test's asset matcher. Correcting it allowed the test to validate both local assets. Chrome exited during sandboxed launch, and the first approved run outside the sandbox passed. Neither issue required a content correction.

This was a local Chrome smoke test with desktop and emulated mobile viewports. Physical-device and screen-reader testing and a deployed Pages check remain unverified. The waveform is a normalized, silent simulation and the valence–arousal plot uses illustrative coordinates. The confusion matrix is synthetic. The UAR formula remains outside the approved content.

## 2026-11-21 · Stage 4 Task 3 readiness

### Content and scientific review

Replayed the 13 Stage 3 Wiki queries from the teaching dataset and validated 31 evidence mappings before rebuilding HTML. The replay used deterministic dry runs. It establishes which Wiki evidence was retrieved. The Chrome test independently compared the 12 rendered slide titles, explanations and objective lists, all 31 claim texts, passage IDs, locators and excerpts, and the seven S01–S07 reference targets against the dataset and verified registry.

Manually compared the Traditional Chinese claims to the retrieved Wiki excerpts. All six chapters are represented: fundamentals (slides 1–2 and 12), acoustics (3–4), emotion representation (5), models (6–8), datasets and evaluation (9–10), and limitations (11). Checked the scope of the RAVDESS human score, the distinction between original ASR and downstream SER, the conditional interpretation of pitch, and the F0/speaking-rate research proposal. The paired-session test split and synthetic matrix are labeled teaching examples. No unsupported or overstated claim requiring a content correction was found. The UAR formula remains unapproved and excluded. No scientific content changed in Task 3.

### End-to-end checks

| Command | Final observed result |
|---|---|
| `python -B scripts/check_wiki.py` | Stage 2 structural lint passed. 7 verified sources, 14 Wiki pages, 6 chapters and 35 evidence pointers. |
| `python -B -m unittest discover -s tests -v` | All 17 Stage 3 tests passed. Model calls in these tests used fixtures. |
| `python -B scripts/check_slide_content.py` | Deterministic content check passed. 12 slides, 31 claim mappings and 13 query replays. |
| `python -B scripts/build_presentation.py` and `python -B scripts/build_presentation.py --check` | Rebuilt the static entry point and verified it matches the renderer and current artifact. |
| `node --check slides/presentation.js` | Passed. |
| `node tests/smoke_presentation.mjs "C:/Program Files/Google/Chrome/Application/chrome.exe"` | Passed in headless Chrome 157.0.8103.79 under a local `/ser-llm-wiki/` HTTP subpath. CSS and JS loaded locally, no missing HTTP assets or console errors were recorded, and references matched all seven verified registry URLs. |
| `git diff --check` | Passed. |

The browser suite checked all slide positions with the next button and left-arrow navigation, both end boundaries, counter and progress at every position, all menu destinations, previous-button navigation, the wordmark, the skip link, direct links to slides and references, and browser Back/Forward. The frequency, amplitude, valence and arousal controls were exercised, including keyboard adjustments that preserve the current slide. The pipeline, matrix disclosure and both quiz answers worked. All 36 combinations of slide and viewport (1440, 390 and 320 CSS pixels) passed horizontal-overflow, sampled font-size and sampled 4.5:1 text-contrast checks. JavaScript-disabled reading and reduced-motion behavior passed.

### Failures, repairs and retry counts

| Finding | Repair and observed retry count |
|---|---|
| The first browser run failed to open the quiz with a simulated Enter key. | Supplied the Enter character in Chrome's key event so the fixture exercises native disclosure behavior. Passed on correction retry 1. No application keyboard handler was needed. |
| The next run recorded three HTTP 404 console errors. | Declared an inline icon so Chrome no longer performs the implicit icon request in the static preview. The next run recorded zero console errors and zero missing assets. Passed on correction retry 1 for this failure. |
| Slide 5 described two high-arousal examples while the diagram showed only the adjustable point. | Added two visibly distinct example markers on opposing sides of the valence axis. The geometry check passed on first verification after the presentation repair. No claim or dataset edit was made. |

### Readiness

Ready for a GitHub Pages deployment check using the unchanged workflow. The tested HTTP subpath serves only the presentation folder. Live Pages deployment, outbound publisher responses, physical devices, non-Chromium browsers and assistive technologies were outside this local QA run. The contrast check samples visible text and does not constitute a full accessibility audit.
