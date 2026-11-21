# 5. Datasets and evaluation

## RAVDESS

Twenty-four actors performed two fixed statements in a controlled speech-and-song dataset. The same performance was exported in audio-video, video-only, and audio-only forms. [S03](../sources/S03.md), Description of RAVDESS files, p. 11 and Table 1.

**Illustrative dataset selection.** For an audio-only speech task, select the speech channel and audio-only modality.

In the human validity task, raters identified the intended emotion. Across stimulus types, the authors report 60% correct for audio-only, 75% for video-only, and 80% for audio-video. These are aggregate human identification scores for this study. [S03](../sources/S03.md), Discussion, p. 21.

The authors discuss the trade-off between controlling words and recording conditions and capturing the variation of naturally occurring speech. [S03](../sources/S03.md), Discussion, pp. 23–24.

See [Emotion representations](../concepts/emotion-representations.md) for the difference between intended labels and listener ratings.

## IEMOCAP

Ten actors were recorded in five paired sessions. The design included scripted dialogue and improvisation prompted by hypothetical scenarios. [S04](../sources/S04.md), §§3.1–3.2, manuscript pp. 6–8.

**Illustrative split.** To ask whether a model can handle unseen speakers in this corpus, put all turns from one whole session aside for testing and use other sessions for training. This is a teaching example based on the session structure, with no benchmark result attached. [S04](../sources/S04.md), §3.2, manuscript pp. 7–8.

## Data scarcity and evaluation

Small or imbalanced labeled datasets can make it harder to learn patterns that generalize. In the review, class imbalance is one of the consequences of limited labeled speech. [S06](../sources/S06.md), §1, pp. 110–111.

Data augmentation creates training variants. The review gives examples such as adding noise, shifting pitch, and stretching time. It warns that modifications can preserve existing biases or obscure cues that matter for the emotion label. [S06](../sources/S06.md), §2.2, pp. 113–114, and §3.2, p. 120.

The review summarizes prior results using weighted and unweighted accuracy and records the datasets alongside the scores. When interpreting a score, check the original experiment for the metric definition and test setup. [S06](../sources/S06.md), §3.1, pp. 117–119, Tables 1–3.

## Reading classification scores

Accuracy is the share of test examples assigned the correct label. For a given class, precision is the share of predictions of that class that were correct. Recall is the share of actual examples of that class that the system found. The class F1 score is the harmonic mean of precision and recall. When comparing F1 across reports, check how each report combines the classes. [S01](../sources/S01.md), §5, pp. 9–10, Eqs. (1)–(4).
