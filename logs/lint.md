# Wiki lint log

## 2026-11-21 · S01 ingestion

| Check | Actual result |
|---|---|
| Baseline `python scripts/check_wiki.py` | Passed with 7 registered sources, 0 ingested, and 1 Wiki Markdown file. The index had no populated chapters. |
| Post-ingest `python scripts/check_wiki.py` | Passed with 7 registered sources, 1 verified, and 6 Wiki Markdown files. |
| Supplemental Python check | Passed. Checked local links in 15 Markdown files, reachability of all 6 Wiki pages from the index, chapter numbering and pending entries, 10 chapter citations with locations, 8 source evidence rows, registry status and chapter mapping, and the unchanged raw PDF checksum. |
| Manual evidence and consistency review | Compared the 8 evidence rows and 10 chapter citations with the relevant local PDF sections and publisher text. Found no unsupported substantive claim, missing citation location, or conflicting or redundant chapter explanation. The source table repeats chapter claims for traceability. Teaching examples and interpretation guidance are labeled. |
| `git diff --check` and `git check-ignore raw/S01.pdf` | Passed. Git reported its usual LF-to-CRLF conversion warnings for edited files. It confirmed the PDF is ignored. |

The first post-ingest lint passed and required zero retries. Chapters 2 and 5 still lack chapter pages and are marked pending in the [Wiki index](../wiki/index.md). Detailed acoustic features, dataset evaluation metrics and splits, and primary-source wav2vec 2.0 results remain coverage gaps. The review’s §5 wording about weighted and unweighted accuracy was left out of the Wiki pending a source that defines the averaging conventions clearly.

## 2026-11-21 · S02

Passed. 17 Markdown files pass link and UTF-8 checks, 8 Wiki pages are reachable, and 4 new citation lines match the source record. Registry, raw checksum and git diff checks passed.

Manual review checked new evidence against the paper sections and inspected the chapter changes for unsupported claims, duplicated explanations and contradictions. Chapter 5 is still pending. Lint retries: 0.

## 2026-11-21 · S03

Passed. 19 Markdown files pass link and UTF-8 checks, 10 Wiki pages are reachable, and 4 new citation lines match the source record. Registry, raw checksum and git diff checks passed.

Manual review checked new evidence against the paper sections and inspected the chapter changes for unsupported claims, duplicated explanations and contradictions. All six chapter entries now resolve to pages. Lint retries: 0.

## 2026-11-21 · S04

Passed. 20 Markdown files pass link and UTF-8 checks, 11 Wiki pages are reachable, and 4 new citation lines match the source record. Registry, raw checksum and git diff checks passed.

Manual review checked new evidence against the paper sections and inspected the chapter changes for unsupported claims, duplicated explanations and contradictions. The RAVDESS validity percentage and IEMOCAP rater agreement are different quantities and are labeled accordingly. Lint retries: 0.

## 2026-11-21 · S05

Passed. 21 Markdown files pass link and UTF-8 checks, 12 Wiki pages are reachable, and 3 new citation lines match the source record. Registry, raw checksum and git diff checks passed.

Manual review checked new evidence against the paper sections and inspected the chapter changes for unsupported claims, duplicated explanations and contradictions. The original ASR results and the downstream SER workflow are marked with their respective sources. Lint retries: 0.

## 2026-11-21 · S06

Passed. 22 Markdown files pass link and UTF-8 checks, 13 Wiki pages are reachable, and 4 new citation lines match the source record. Registry, raw checksum and git diff checks passed.

Manual review checked new evidence against the paper sections and inspected the chapter changes for unsupported claims, duplicated explanations and contradictions. The chapter distinguishes augmentation examples and author cautions from benchmark findings. Lint retries: 0.

## 2026-11-21 · S07

Passed. 23 Markdown files pass link and UTF-8 checks, 14 Wiki pages are reachable, and 3 new citation lines match the source record. Registry, raw checksum and git diff checks passed.

Manual review checked new evidence against the paper sections and inspected the chapter changes for unsupported claims, duplicated explanations and contradictions. The hybrid approach is attributed to the authors as a proposal, with the internal count discrepancy recorded in the source record. Lint retries: 0.

## 2026-11-21 · Stage 2 final check

The repository checker and supplemental audit passed with seven verified sources, six chapter pages, 14 reachable Wiki pages, and 30 evidence entries including the eight from S01. The audit checked local links in 23 Markdown files, matched all 22 new chapter citation locations to their source records, decoded the files as strict UTF-8 without a BOM or replacement characters, and verified all seven raw PDF hashes and Git ignore rules. It also checked the stored spelling of Wöllmer and Björn and the section and page-range symbols directly. `git diff --check` passed with LF-to-CRLF conversion warnings. The temporary text extracts were removed.

S01 needed a direct page-stream fallback when its extraction tools were unavailable. In the later cycles, a dedicated PDF reader extracted S02–S04, then hit a content-stream limit on S05. Switching readers recovered S05 on its first retry and extracted S06 and S07 on their first attempts. Chapter and source-record validation ran after each ingest, so each source has a separate outcome for comparison with the pilot.

## 2026-11-21 · Global audit and Stage 3 readiness

### Automated checks

- The original checker passed on the seven-source snapshot. It checked basic registry structure and Wiki link targets. It had no checks for orphan pages, six-chapter navigation, citation-to-evidence matches, or agreement between the two registries.
- The expanded checker passed with seven verified source records, six indexed chapters, 14 reachable Wiki pages, and 35 evidence pointers. It checks UTF-8, repository-local link targets in README, AGENTS, Wiki, docs, and logs, reciprocal evidence and citation pointers, and the chapter mapping for each complete source. It runs offline without the ignored PDFs. External URL availability and scientific accuracy are outside its checks.
- A temporary fixture confirmed that the checker rejects a broken link, missing chapter entry, orphan page, mismatched citation location, inconsistent registry status, and invalid UTF-8. A separate local check matched all seven PDF hashes to the ingestion records. `git diff --check` passed with line-ending conversion warnings.
- The first expanded-check run exposed two S01 chapter citations whose narrower locators had only a combined evidence row. Added precise rows for §2 and §2.1 and preserved the pilot table. That run also exposed an em dash replaced by an ASCII question mark when writing the checker. The checker now compares the Unicode code point explicitly. Both failures cleared on the first retry.

### Manual review

Reviewed all six chapters and seven source records against their evidence tables and ingestion history. Checked that the RAVDESS human identification figures, IEMOCAP annotation agreement, openSMILE extraction timing, and wav2vec 2.0 transcription WER describe distinct measurements. Reviewed the recorded S05 byline variation and S07 corpus-count discrepancies. Those remain documented, and the conflicting totals stay out of the teaching text. Literature proposals, hypothetical examples, and Wiki interpretation guidance are identified separately from research findings.

Consolidated duplicated MFCC and feature-pipeline explanations. Labeled the RAVDESS audio-only selection as an illustrative use. Added the spectrogram explanation from S01 §§3.2–3.4, accuracy and F1 from S01 §5 equations (1)–(4), and CNN and LSTM explanations from S07 §§5.1 and 5.2.1. The S01 audit additions are separate from the original pilot evidence table, and both registries now reflect the additional chapter references.

### Stage 3 readiness

| Chapter | Teaching coverage after audit |
|---|---|
| 1. SER fundamentals | SER versus ASR and an illustrative same-phrase example. |
| 2. Acoustic signals and features | Waveform, sample rate, frame, spectrogram, pitch, energy, and MFCC. |
| 3. Emotion representations | Categories and valence–arousal, with two annotation examples. |
| 4. Models and learned representations | Feature-based classification, CNN and LSTM, and original ASR versus downstream SER use of wav2vec 2.0. |
| 5. Datasets and evaluation | RAVDESS, IEMOCAP, a held-out session example, accuracy and F1. UAR averaging and the planned confusion-matrix example remain open. |
| 6. Applications and limitations | Uncertainty, speaker and recording variation, augmentation and noise, domain shift, privacy and consent. Evidence for specific noise-robustness performance remains open. |

Ready for claim-level storyboard mapping from the verified Wiki. The full evaluation objective still needs a checked UAR definition and an explicitly synthetic confusion-matrix example. The [storyboard](../docs/03_slide_map.md) is provisional. Each proposed slide needs exact Wiki paths and claim citations before HTML work.
