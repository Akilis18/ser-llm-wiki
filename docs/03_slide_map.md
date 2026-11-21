# Stage 4 教學大綱與來源追溯

**AI 如何聽出情緒？從聲音特徵到深度學習的語音情緒辨識入門**

對象：沒有語音情緒辨識背景的初學者。主要語言為繁體中文。

完整學習目標、講解、重點、示意、檢索紀錄及證據文字收錄於 [slide-content.json](../data/slide-content.json)。

## 教學順序

| 張次 | 主題 | 學習重點 | 來源 |
|---|---|---|---|
| 1 | 課程導覽 | 用自己的話說明語音情緒辨識在做什麼。 預覽從聲音到模型評估的學習路線。 | [S01](../wiki/sources/S01.md) |
| 2 | 同一句話，兩種辨識任務 | 區分 SER 與 ASR 的輸出。 說明聲音線索為何需要合併解讀。 | [S01](../wiki/sources/S01.md) |
| 3 | 波形與取樣 | 說明波形、取樣率和音框的關係。 | [S02](../wiki/sources/S02.md) |
| 4 | 音高、能量、時間與 MFCC | 分辨常見的聲學特徵。 比較梅爾頻譜圖與 MFCC 所呈現的資訊。 | [S01](../wiki/sources/S01.md), [S02](../wiki/sources/S02.md), [S07](../wiki/sources/S07.md) |
| 5 | 用類別或尺度表示情緒 | 區分類別式與維度式標註。 用愉悅度與喚起度描述假想聲音。 | [S01](../wiki/sources/S01.md) |
| 6 | 傳統方法：先抽特徵，再分類 | 依序說出特徵擷取、摘要與分類。 辨認 openSMILE 與 SVM 的角色。 | [S01](../wiki/sources/S01.md), [S02](../wiki/sources/S02.md) |
| 7 | 深度學習：從輸入學特徵 | 用自己的話比較 CNN 與 LSTM。 辨認波形模型與人工特徵流程的輸入差異。 | [S07](../wiki/sources/S07.md) |
| 8 | wav2vec 2.0：先預訓練，再適配任務 | 說明遮蔽訓練的基本想法。 分辨原始 ASR 研究與下游 SER 用法。 | [S01](../wiki/sources/S01.md), [S05](../wiki/sources/S05.md) |
| 9 | RAVDESS 與 IEMOCAP | 比較兩個資料集如何產生語音。 說明為什麼要留出整組說話者做測試。 | [S03](../wiki/sources/S03.md), [S04](../wiki/sources/S04.md) |
| 10 | 評估：Accuracy、Precision、Recall 與 F1 | 用混淆矩陣讀出整體正確率與某類的召回率。 說明為什麼要同時看各類別表現。 | [S01](../wiki/sources/S01.md), [S06](../wiki/sources/S06.md) |
| 11 | 真實環境中的限制 | 指出說話者、錄音條件與資料偏差可能帶來的問題。 說明兒童語音資料蒐集的同意與隱私考量。 | [S01](../wiki/sources/S01.md), [S06](../wiki/sources/S06.md), [S07](../wiki/sources/S07.md) |
| 12 | 總結、小測驗與參考資料 | 回顧兩種語音辨識任務與線索的不確定性。 練習從重點追溯 Wiki 與原始來源編號。 | [S01](../wiki/sources/S01.md) |

## 逐項證據對照

「段落 ID」指向 Wiki 標題行，「區塊」是該標題下由 Stage 3 傳回的區塊序號。JSON 保留逐字證據與檢索排名。

| 重點 | Wiki 段落 ID | 區塊 | 原文位置 |
|---|---|---:|---|
| 01.1 語音情緒辨識（Speech Emotion Recognition, SER）利用語音線索估計說話時表現出的情緒。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 1 | [S01](../wiki/sources/S01.md), §1, pp. 1–2 and §4, p. 8 |
| 02.1 自動語音辨識（Automatic Speech Recognition, ASR）辨識說出的語音與詞語序列。同一段錄音可以用於 SER 和 ASR。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 1 | [S01](../wiki/sources/S01.md), §1, pp. 1–2 and §4, p. 8 |
| 02.2 音高、訊號強度與說話的時間變化都可能提供線索。高音高可以伴隨不同的高喚起情緒，單靠音高無法判定情緒類別。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 2 | [S01](../wiki/sources/S01.md), §§2.2–2.3, pp. 3–4 |
| 03.1 數位波形是一串音訊樣本。取樣率是每秒的樣本數。音框（frame）把相鄰的樣本分成一小段供分析。 | [wiki/concepts/acoustic-features.md#L3](../wiki/concepts/acoustic-features.md) | 1 | [S02](../wiki/sources/S02.md), §§3 and 5, pp. 1460–1462 |
| 04.1 基頻（F0）與感知到的音高有關。均方根能量概括音框內的訊號幅度。 | [wiki/concepts/acoustic-features.md#L3](../wiki/concepts/acoustic-features.md) | 2 | [S02](../wiki/sources/S02.md), §4, pp. 1460–1461, Table 1 |
| 04.2 說話的時間變化也是情緒線索之一。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 2 | [S01](../wiki/sources/S01.md), §§2.2–2.3, pp. 3–4 |
| 04.3 梅爾頻譜圖（mel spectrogram）呈現各梅爾頻帶的訊號強度如何隨時間變化。 | [wiki/concepts/acoustic-features.md#L13](../wiki/concepts/acoustic-features.md) | 1 | [S01](../wiki/sources/S01.md), §§3.2–3.4, pp. 6–7 |
| 04.4 梅爾頻率倒譜係數（MFCCs）是對單一音框的梅爾頻譜進行轉換後得到的精簡表示。 | [wiki/concepts/acoustic-features.md#L13](../wiki/concepts/acoustic-features.md) | 2 | [S07](../wiki/sources/S07.md), §§2.1–2.2, pp. 5–6 |
| 05.1 類別式表示使用命名的標籤，例如生氣、喜悅或悲傷。資料集也可以設有中性類別。 | [wiki/concepts/emotion-representations.md#L1](../wiki/concepts/emotion-representations.md) | 1 | [S01](../wiki/sources/S01.md), §2, pp. 2–3 |
| 05.2 維度式表示使用尺度評分。愉悅度（valence）描述愉悅程度，喚起度（arousal）描述活化或強烈程度。 | [wiki/concepts/emotion-representations.md#L1](../wiki/concepts/emotion-representations.md) | 1 | [S01](../wiki/sources/S01.md), §2.1, p. 3 |
| 06.1 傳統流程先把語音轉成數值特徵，再由分類器判斷類別。支援向量機（SVM）可學習區隔情緒類別的邊界。 | [wiki/models/ser-models.md#L3](../wiki/models/ser-models.md) | 1 | [S01](../wiki/sources/S01.md), §4 and §4.3, p. 8 |
| 06.2 openSMILE 可以計算音框特徵與摘要，再輸出特徵或傳給後續元件。 | [wiki/models/ser-models.md#L15](../wiki/models/ser-models.md) | 1 | [S02](../wiki/sources/S02.md), §§3–5, pp. 1460–1462 |
| 06.3 統計摘要可以把一連串音高量測整理成平均值、最小值或最大值。 | [wiki/concepts/acoustic-features.md#L9](../wiki/concepts/acoustic-features.md) | 1 | [S02](../wiki/sources/S02.md), §§2–4, pp. 1460–1461, Fig. 1 and Table 2 |
| 07.1 波形模型可接收音訊樣本，由前面的網路層學習表示。 | [wiki/models/ser-models.md#L29](../wiki/models/ser-models.md) | 1 | [S07](../wiki/sources/S07.md), §§2–3, pp. 5–7 and §9, p. 22 |
| 07.2 卷積神經網路（CNN）用小型濾波器偵測局部模式。長短期記憶網路（LSTM）用記憶狀態和閘門在序列中傳遞資訊。 | [wiki/models/ser-models.md#L29](../wiki/models/ser-models.md) | 2 | [S07](../wiki/sources/S07.md), §§5.1 and 5.2.1, pp. 10–11 |
| 08.1 原始 wav2vec 2.0 先用卷積編碼器和 Transformer 建立含上下文的語音表示。預訓練會遮住部分編碼輸出，讓模型從候選項辨認正確的離散表示。 | [wiki/models/ser-models.md#L21](../wiki/models/ser-models.md) | 1 | [S05](../wiki/sources/S05.md), §2, Fig. 1 and §§3.1–3.2, pp. 2–3 |
| 08.2 原始研究以有文字標註的語音微調模型，目標是語音轉寫（ASR）。 | [wiki/models/ser-models.md#L21](../wiki/models/ser-models.md) | 2 | [S05](../wiki/sources/S05.md), §3.3, p. 4 |
| 08.3 Wiki 介紹的下游 SER 例子會用池化（pooling）把各音框的表示合成整段表示，再預測情緒標籤。 | [wiki/models/ser-models.md#L7](../wiki/models/ser-models.md) | 1 | [S01](../wiki/sources/S01.md), §7.3, pp. 14–15 |
| 09.1 RAVDESS 的演員以固定句子錄製說話及歌唱，提供影音、僅影像與僅音訊三種版本。 | [wiki/datasets/datasets-and-evaluation.md#L3](../wiki/datasets/datasets-and-evaluation.md) | 1 | [S03](../wiki/sources/S03.md), Description of RAVDESS files, p. 11 and Table 1 |
| 09.2 IEMOCAP 由演員兩兩錄音，包含照稿對話，也包含依情境提示即興的對話。 | [wiki/datasets/datasets-and-evaluation.md#L15](../wiki/datasets/datasets-and-evaluation.md) | 1 | [S04](../wiki/sources/S04.md), §§3.1–3.2, manuscript pp. 6–8 |
| 09.3 RAVDESS 的人類辨識測試中，僅音訊條件的整體正確率為 60%。這是聽者辨認演員意圖的表現。 | [wiki/datasets/datasets-and-evaluation.md#L3](../wiki/datasets/datasets-and-evaluation.md) | 3 | [S03](../wiki/sources/S03.md), Discussion, p. 21 |
| 10.1 正確率（accuracy）是全部測試樣本中預測正確的比例。精確率（precision）看某類預測中有多少是對的；召回率（recall）看該類實際樣本中有多少被找出。 | [wiki/datasets/datasets-and-evaluation.md#L29](../wiki/datasets/datasets-and-evaluation.md) | 1 | [S01](../wiki/sources/S01.md), §5, pp. 9–10, Eqs. (1)–(4) |
| 10.2 某一類的 F1 是精確率與召回率的調和平均。比較報告時需確認如何彙整各類別的分數。 | [wiki/datasets/datasets-and-evaluation.md#L29](../wiki/datasets/datasets-and-evaluation.md) | 1 | [S01](../wiki/sources/S01.md), §5, pp. 9–10, Eqs. (1)–(4) |
| 10.3 標註資料少或類別分布不均，可能讓模型更難學到可泛化的模式。 | [wiki/datasets/datasets-and-evaluation.md#L21](../wiki/datasets/datasets-and-evaluation.md) | 1 | [S06](../wiki/sources/S06.md), §1, pp. 110–111 |
| 11.1 研究綜述建議跨資料集、說話者與錄音條件測試，也要留意演出與自然語音之間的差異。 | [wiki/concepts/ser-limitations.md#L9](../wiki/concepts/ser-limitations.md) | 1 | [S01](../wiki/sources/S01.md), §6, pp. 10–11 and §9, p. 16 |
| 11.2 加入噪音、改變音高或拉伸時間可產生訓練變體，但這些改動可能保留原本的偏差，或掩蓋情緒線索。 | [wiki/datasets/datasets-and-evaluation.md#L21](../wiki/datasets/datasets-and-evaluation.md) | 2 | [S06](../wiki/sources/S06.md), §2.2, pp. 113–114, and §3.2, p. 120 |
| 11.3 成人模型轉用到兒童語音時，可能遇到資料領域差異。蒐集兒童語音時，綜述提醒應考量同意與隱私。 | [wiki/concepts/ser-limitations.md#L27](../wiki/concepts/ser-limitations.md) | 1 | [S07](../wiki/sources/S07.md), §8.1, p. 21 and §9, p. 22 |
| 11.4 S01 作者提出可在頻譜特徵之外加入基頻統計與語速等語調摘要。這是研究提案。 | [wiki/concepts/ser-limitations.md#L9](../wiki/concepts/ser-limitations.md) | 2 | [S01](../wiki/sources/S01.md), §9, p. 16 |
| 12.1 語音情緒辨識（Speech Emotion Recognition, SER）利用語音線索估計說話時表現出的情緒。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 1 | [S01](../wiki/sources/S01.md), §1, pp. 1–2 and §4, p. 8 |
| 12.2 自動語音辨識（Automatic Speech Recognition, ASR）辨識說出的語音與詞語序列。同一段錄音可以用於 SER 和 ASR。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 1 | [S01](../wiki/sources/S01.md), §1, pp. 1–2 and §4, p. 8 |
| 12.3 音高、訊號強度與說話的時間變化都可能提供線索。高音高可以伴隨不同的高喚起情緒，單靠音高無法判定情緒類別。 | [wiki/concepts/ser-fundamentals.md#L1](../wiki/concepts/ser-fundamentals.md) | 2 | [S01](../wiki/sources/S01.md), §§2.2–2.3, pp. 3–4 |

## 來源對照

| 來源 | 支援張次 |
|---|---|
| [S01](../wiki/sources/S01.md) | 1, 2, 4, 5, 6, 8, 10, 11, 12 |
| [S02](../wiki/sources/S02.md) | 3, 4, 6 |
| [S03](../wiki/sources/S03.md) | 9 |
| [S04](../wiki/sources/S04.md) | 9 |
| [S05](../wiki/sources/S05.md) | 8 |
| [S06](../wiki/sources/S06.md) | 10, 11 |
| [S07](../wiki/sources/S07.md) | 4, 7, 11 |

第 12 張的參考資料涵蓋上表所有來源；小測驗答案以重點 ID 回指證據。

第 10 張的 UAR 公式未核准。已改為有證據的指標，並以標示清楚的合成資料說明類別表現。

檢索、確定性檢查及語意審查結果載於 [驗證紀錄](../logs/slide-validation.md)。
