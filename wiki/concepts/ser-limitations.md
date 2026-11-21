# 6. Applications and limitations

## Interpreting a prediction

The review mentions remote personal assistance as a possible application. It also notes that many experiments ask a system to choose from a fixed list of labels, which may poorly represent practical use. [S01](../sources/S01.md), §1, p. 1 and §8, p. 15.

**Wiki interpretation guideline.** Treat outputs as uncertain estimates of expressed emotion under a specific labeling scheme. Keep clinical diagnosis, deception detection, and inference of private mental states outside the scope of these teaching examples.

## Generalizing to new conditions

The review recommends testing across datasets, speakers, and recording conditions, with attention to differences between acted and spontaneous speech. It describes generalization of fine-tuned self-supervised representations across domains as an open concern. [S01](../sources/S01.md), §6, pp. 10–11 and §9, p. 16.

The author proposes adding explicit intonation summaries, such as F0 statistics and speaking rate, alongside spectral features. This is a research proposal in the review’s conclusion. [S01](../sources/S01.md), §9, p. 16.

See [SER fundamentals](ser-fundamentals.md) for the acoustic-cue example and [Emotion representations](emotion-representations.md) for annotator disagreement.

## What annotators could observe

IEMOCAP annotators watched videos and rated turns in sequence, so their judgments could draw on facial cues and preceding dialogue as well as speech. An audio-only model may receive less information than was available when the labels were assigned. [S04](../sources/S04.md), §5.2, manuscript pp. 12–13.

## When transfer can fail

Domain adaptation aims to use information learned in a source domain for a target domain with limited data. The scarcity review warns that mismatched domains can yield negative transfer, where the pretrained approach performs worse than training from scratch. It also flags overfitting when fine-tuning has very few target examples. [S06](../sources/S06.md), §2.3, pp. 114–115, and §3.2, p. 120.

See [Datasets and evaluation](../datasets/datasets-and-evaluation.md) for corpus design and held-out testing.

## Age and coverage

The adult-and-child review describes smaller, less diverse child-focused datasets in the work it compares, as well as developmental changes in articulation and emotional expression. It identifies adult-to-child transfer as a domain shift and highlights consent and privacy when collecting children’s speech. [S07](../sources/S07.md), §8.1, p. 21 and §9, p. 22.
