# Ingest log

| Date | Source | Pages updated | Evidence check | Outcome |
|---|---|---|---|---|
| 2026-11-21 | S01, `raw/S01.pdf` | Chapters 1, 3, 4, 6 and the [source record](../wiki/sources/S01.md) | Compared the local title, author, journal, year, article number, DOI and CC BY 4.0 notice with the registry and publisher; checked eight evidence entries against the PDF body and the publisher full text | Verified |

- Files updated outside the chapter and source pages include `wiki/index.md`, `docs/sources.json`, `docs/02_sources.md`, `README.md`, `logs/ingest.md`, and `logs/lint.md`.
- PDF SHA-256 is `576EE47BF77CA32E25D2194B0CB63080EDC09DBC0F6065727F95BB57A2505D6D`. The local file is ignored by Git.
- There was no available PDF text utility on PATH. A temporary `pypdf` install could not resolve the package on the configured index or PyPI, and Word automation failed with COM error `0x80070520`. Local text was recovered directly from the PDF page streams using Python and checked against the publisher’s readable full text. The publisher’s PDF endpoint returned a cache miss in the web reader.
- The scope follows the existing beginner teaching contract and S01's registered mapping. Chapters 2 and 5 and the primary-source account of wav2vec 2.0 remain pending. See the [lint log](lint.md) for validation results.

## 2026-11-21 · S02

| Field | Result |
|---|---|
| Full text accessible | Yes. Read `raw/S02.pdf` (4 PDF pages). |
| Evidence entries extracted | 4 |
| Wiki pages created | 2 (wiki/concepts/acoustic-features.md, wiki/sources/S02.md) |
| Wiki pages updated | 2 (wiki/models/ser-models.md, wiki/index.md) |
| Source validation | Passed. Compared title, author, venue, publication details and rights, then checked each evidence entry against its cited location. Local title and author names matched the proceedings record. |
| Lint | Passed. See [lint log](lint.md). |
| Retries | 0. The reader warned about fonts used in figures; the caption, surrounding text and tables were readable. |
| Unresolved issues | The benchmark does not establish downstream SER accuracy or timing on current hardware. |

Updated the canonical and human-readable registries, README status, and both logs.

## 2026-11-21 · S03

| Field | Result |
|---|---|
| Full text accessible | Yes. Read `raw/S03.pdf` (35 PDF pages). |
| Evidence entries extracted | 4 |
| Wiki pages created | 2 (wiki/datasets/datasets-and-evaluation.md, wiki/sources/S03.md) |
| Wiki pages updated | 2 (wiki/concepts/emotion-representations.md, wiki/index.md) |
| Source validation | Passed. Compared title, author, venue, publication details and rights, then checked each evidence entry against its cited location. The PLOS record confirmed the subtitle, authors, and article identifier. |
| Lint | Passed. See [lint log](lint.md). |
| Retries | 0. The PDF reader reported cross-reference warnings and recovered all 35 pages. |
| Unresolved issues | Controlled acting and fixed prompts limit transfer to everyday speech. The human aggregate modality scores do not provide an audio-only speech-model baseline. |

Updated the canonical and human-readable registries, README status, and both logs.

## 2026-11-21 · S04

| Field | Result |
|---|---|
| Full text accessible | Yes. Read `raw/S04.pdf` (30 PDF pages). |
| Evidence entries extracted | 4 |
| Wiki pages created | 1 (wiki/sources/S04.md) |
| Wiki pages updated | 4 (wiki/datasets/datasets-and-evaluation.md, wiki/concepts/emotion-representations.md, wiki/concepts/ser-limitations.md, wiki/index.md) |
| Source validation | Passed. Compared title, author, venue, publication details and rights, then checked each evidence entry against its cited location. Local manuscript title and author list match the Springer and USC records; publication metadata refers to the 2008 journal article. |
| Lint | Passed. See [lint log](lint.md). |
| Retries | 0. |
| Unresolved issues | The manuscript and publisher pagination differ. Improvised actor dialogue and multimodal annotation constrain audio-only interpretation. |

Updated the canonical and human-readable registries, README status, and both logs.

## 2026-11-21 · S05

| Field | Result |
|---|---|
| Full text accessible | Yes. Read `raw/S05.pdf` (12 PDF pages). |
| Evidence entries extracted | 3 |
| Wiki pages created | 1 (wiki/sources/S05.md) |
| Wiki pages updated | 2 (wiki/models/ser-models.md, wiki/index.md) |
| Source validation | Passed. Compared title, author, venue, publication details and rights, then checked each evidence entry against its cited location. The official PDF matches the local byline; the proceedings landing page gives a different form for Zhou’s name. |
| Lint | Passed. See [lint log](lint.md). |
| Retries | 1 full-text extraction retry. pypdf stopped on a content-stream parser limit. PyMuPDF recovered all 12 pages. Source claim validation and lint each required 0 retries. |
| Unresolved issues | Author-name variation across proceedings surfaces is documented. The paper reports no SER benchmark used by this Wiki. |

Updated the canonical and human-readable registries, README status, and both logs.

## 2026-11-21 · S06

| Field | Result |
|---|---|
| Full text accessible | Yes. Read `raw/S06.pdf` (14 PDF pages). |
| Evidence entries extracted | 4 |
| Wiki pages created | 1 (wiki/sources/S06.md) |
| Wiki pages updated | 3 (wiki/datasets/datasets-and-evaluation.md, wiki/concepts/ser-limitations.md, wiki/index.md) |
| Source validation | Passed. Compared title, author, venue, publication details and rights, then checked each evidence entry against its cited location. The local DOI, author names and issue details match the university record. ScienceDirect returned HTTP 403 to the web reader; all relevant full text was available in the local PDF. |
| Lint | Passed. See [lint log](lint.md). |
| Retries | 0. The alternate reader was used for the first S06 extraction. |
| Unresolved issues | The review reports heterogeneous metrics and protocols. The Wiki leaves formula-level UAR coverage and cross-study score comparisons open. |

Updated the canonical and human-readable registries, README status, and both logs.

## 2026-11-21 · S07

| Field | Result |
|---|---|
| Full text accessible | Yes. Read `raw/S07.pdf` (26 PDF pages). |
| Evidence entries extracted | 3 |
| Wiki pages created | 1 (wiki/sources/S07.md) |
| Wiki pages updated | 4 (wiki/concepts/acoustic-features.md, wiki/models/ser-models.md, wiki/concepts/ser-limitations.md, wiki/index.md) |
| Source validation | Passed. Compared title, author, venue, publication details and rights, then checked each evidence entry against its cited location. The local byline, DOI, 2026 publication date and license matched the Springer record. |
| Lint | Passed. See [lint log](lint.md). |
| Retries | 0. The alternate reader was used for the first S07 extraction. |
| Unresolved issues | Child-BESD totals differ between the review’s sections. Its IEMOCAP count in §8.1 also differs from the full turn count reported in S04 §5.1. Neither count was adopted from the review. Cross-study comparisons remain protocol-specific. |

Updated the canonical and human-readable registries, README status, and both logs.
