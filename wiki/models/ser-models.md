# 4. Models and learned representations

## Features and a classifier

In the traditional pipeline described by the review, a front end turns speech into numerical features and a back end classifies the resulting representation. A support vector machine (SVM), for example, can learn a boundary between examples of one emotion class and the remaining classes. [S01](../sources/S01.md), §4 and §4.3, p. 8.

## Pretrained speech encoder

The review describes learning general speech representations from unlabeled audio through self-supervised pretraining and then adapting the model to labeled SER examples. In one wav2vec 2.0 downstream example, pooling combines the encoder’s frame-level outputs into a representation of the whole clip, which a classifier uses to predict an emotion label. [S01](../sources/S01.md), §7.3, pp. 14–15.

The original study below explains the pretraining objective and its ASR experiments.

See [Emotion representations](../concepts/emotion-representations.md) for prediction targets and [Applications and limitations](../concepts/ser-limitations.md) for generalization concerns.

## Example feature extractor

openSMILE uses configurable components to read audio, compute frame-level descriptors and summaries, and export features or pass data to a downstream component. The paper’s benchmark times feature extraction itself. [S02](../sources/S02.md), §§3–5, pp. 1460–1462.

See [Acoustic signals and features](../concepts/acoustic-features.md) for the distinction between a frame descriptor and a summary.

## Original wav2vec 2.0 study

A convolutional encoder turns raw audio into short-time representations, and a Transformer builds representations using sequence context. During pretraining, some encoder outputs are masked and the model learns to select the matching discrete representation from distractors. [S05](../sources/S05.md), §2, Fig. 1 and §§3.1–3.2, pp. 2–3.

The authors fine-tuned for transcription on labeled speech using connectionist temporal classification (CTC). [S05](../sources/S05.md), §3.3, p. 4.

For the large model pretrained on LibriVox audio, fine-tuned on 960 hours of labeled LibriSpeech and decoded with a Transformer language model, the authors report word error rates of 1.8% on test-clean and 3.3% on test-other. These evaluate transcription. The downstream SER example above has a different target. [S05](../sources/S05.md), §5.2 and Table 2, p. 7.

## Handcrafted and waveform inputs

A waveform model takes audio samples as input and learns its own representation in its early layers. Gudivaka and colleagues propose combining learned waveform representations with structured features for children’s speech, where labeled data are scarce. [S07](../sources/S07.md), §§2–3, pp. 5–7 and §9, p. 22.

A convolutional neural network (CNN) uses small filters to detect local patterns in inputs such as a waveform or spectrogram. A long short-term memory network (LSTM) uses a memory state and gates to pass information along a sequence. [S07](../sources/S07.md), §§5.1 and 5.2.1, pp. 10–11.
