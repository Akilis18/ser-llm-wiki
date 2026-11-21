# 2. Acoustic signals and features

## From samples to frame measurements

A digital waveform is a sequence of audio samples. A frame groups adjacent samples for analysis. The sampling rate gives the number of samples per second. The paper illustrates how the toolkit groups samples into frames for pitch estimation. [S02](../sources/S02.md), §§3 and 5, pp. 1460–1462.

Examples of frame descriptors include fundamental frequency (F0), which relates to perceived pitch, and root-mean-square energy, which summarizes signal magnitude over a frame. The toolkit also computes mel-frequency cepstral coefficients (MFCCs). [S02](../sources/S02.md), §4, pp. 1460–1461, Table 1.

## Summarizing a feature over time

A functional turns a sequence of measurements into a summary, such as a mean, minimum, or maximum. In the toolkit’s example, a pitch descriptor is computed on frames and then summarized across frames. [S02](../sources/S02.md), §§2–4, pp. 1460–1461, Fig. 1 and Table 2.

## Spectral and cepstral measurements

A spectrogram shows how the distribution of signal strength across frequencies changes over time. Each short frame contributes a spectrum. A mel-spectrogram groups frequencies into bands on the mel scale. [S01](../sources/S01.md), §§3.2–3.4, pp. 6–7.

A spectral descriptor summarizes some aspect of energy across frequencies. For example, spectral spread describes how widely spectral components are distributed. Cepstral descriptors such as MFCCs give a transformed view of the short-term spectrum. [S07](../sources/S07.md), §§2.1–2.2, pp. 5–6.

See [Models and learned representations](../models/ser-models.md) for how acoustic features can feed a classifier.
