#!/usr/bin/env python3
"""Render the verified slide dataset as progressively enhanced static HTML."""

import argparse
from html import escape
import json
from pathlib import Path
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "slides/index.html"

KIND = {
    "research_method": "研究方法", "research_finding": "研究結果",
    "research_proposal": "研究提案", "review_recommendation": "綜述建議",
}
VISUAL = {
    "diagram": "教學示意", "teaching_example": "假想情境",
    "synthetic_data": "合成資料", "quiz": "知識檢核",
}


def evidence_markup(claim: dict) -> str:
    rows = []
    for evidence in claim["evidence"]:
        sid = escape(evidence["source_id"])
        rows.append(
            f'<p><a href="#ref-{sid}">[{sid}]</a> {escape(evidence["location"])}</p>'
            f'<code>{escape(evidence["passage_id"])}</code>'
            f'<blockquote lang="en">{escape(evidence["excerpt"])}</blockquote>'
        )
    return '<details class="evidence"><summary>查看證據</summary>' + "".join(rows) + "</details>"


def range_control(name: str, label: str, low: int, high: int, value: int) -> str:
    return (
        f'<label class="range" for="{name}"><span>{label}</span>'
        f'<output id="{name}-value" for="{name}">{value}</output>'
        f'<input id="{name}" type="range" min="{low}" max="{high}" value="{value}" disabled></label>'
    )


def diagram(title: str, nodes: tuple[str, ...]) -> str:
    steps = "".join(f"<li>{node}</li>" for node in nodes)
    return f'<ol class="flow" aria-label="{title}">{steps}</ol>'


def visual_markup(slide: dict) -> str:
    number, visual = slide["number"], slide["visual"]
    if number == 1:
        body = '<div class="hero-wave" aria-hidden="true">' + "<i></i>" * 23 + "</div>"
        body += diagram("課程路線", ("音訊", "表示", "模型", "評估"))
    elif number == 3:
        body = (
            '<canvas id="waveform" role="img" aria-label="模擬波形示意圖">模擬波形：以樣本點表示訊號。</canvas>'
            '<div class="axis-caption">時間 →</div><div class="controls">'
            + range_control("frequency", "頻率（每視窗週期數）", 1, 8, 3)
            + range_control("amplitude", "振幅（相對值）", 10, 100, 65)
            + '</div><noscript><p>啟用 JavaScript 可操作波形控制。範例設定為 3 個週期，振幅 65%。</p></noscript>'
        )
    elif number == 5:
        body = (
            '<div class="affect-plot" role="img" aria-label="愉悅度與喚起度示意座標，示意點位於中心">'
            '<span class="affect-high">高喚起</span><span class="affect-low">低喚起</span>'
            '<span class="affect-left">較不愉悅</span><span class="affect-right">較愉悅</span>'
            '<i class="affect-example affect-example-left" aria-hidden="true"></i>'
            '<i class="affect-example affect-example-right" aria-hidden="true"></i>'
            '<i id="affect-point"></i></div>'
            '<p class="axis-caption">空心點是兩個示意位置。用滑桿移動實心點。</p><div class="controls">'
            + range_control("valence", "愉悅度（Valence）", -100, 100, 0)
            + range_control("arousal", "喚起度（Arousal）", -100, 100, 0)
            + "</div>"
        )
    elif number == 6:
        body = diagram("SER 流程", ("錄音", "音框特徵", "統計摘要", "SVM", "預測標籤"))
        body += '<div class="pipeline" aria-label="查看流程說明">'
        for label, index in (("特徵擷取", 1), ("統計摘要", 2), ("分類", 0)):
            claim = slide["key_points"][index]
            body += f'<details><summary>{label}</summary><p>{escape(claim["text"])}</p></details>'
        body += "</div>"
    elif number == 8:
        body = diagram("原始 ASR 研究", ("預訓練編碼器", "語音轉寫（ASR）"))
        body += diagram("下游 SER 示意", ("預訓練編碼器", "池化與分類", "情緒標籤（SER）"))
    elif number == 10:
        labels = [escape(label) for label in visual["data"]["labels"]]
        body = '<table class="matrix"><caption>合成混淆矩陣</caption><thead><tr><th scope="col">實際／預測</th>'
        body += "".join(f'<th scope="col">{label}</th>' for label in labels) + "</tr></thead><tbody>"
        for label, counts in zip(labels, visual["data"]["counts"], strict=True):
            body += f'<tr><th scope="row">{label}</th>' + "".join(f"<td>{value}</td>" for value in counts) + "</tr>"
        body += '</tbody></table><details class="exercise"><summary>核對正確率與乙類召回率</summary>'
        return body + f'<p>{escape(visual["description"])}</p></details>'
    elif number == 12:
        claims = {claim["id"]: claim for claim in slide["key_points"]}
        body = '<div class="quiz">'
        for item in slide["quiz"]:
            claim = claims[item["answer_claim_id"]]
            sources = " ".join(f'<a href="#ref-{escape(e["source_id"])}">[{escape(e["source_id"])}]</a>'
                               for e in claim["evidence"])
            body += (f'<details><summary>{escape(item["question"])}</summary>'
                     f'<p>{escape(claim["text"])} {sources}</p></details>')
        body += "</div>"
    else:
        body = ""
    return body + f'<p class="visual-note">{escape(visual["description"])}</p>'


def references(slide: dict, registry: dict) -> str:
    rows = []
    for sid in slide["reference_sources"]:
        source = registry[sid]
        url = source["url"]
        if urlsplit(url).scheme != "https":
            raise ValueError(f"Expected an HTTPS publication link for {sid}")
        rows.append(f'<li id="ref-{escape(sid)}" tabindex="-1"><a href="{escape(url)}">'
                    f'[{escape(sid)}] <span lang="en">{escape(source["title"])}</span></a></li>')
    return '<section class="references"><h3>參考資料</h3><ul>' + "".join(rows) + "</ul></section>"


def render_slide(slide: dict, title: str, registry: dict) -> str:
    n = slide["number"]
    heading = title if n == 1 else slide["title"]
    objectives = "".join(f"<li>{escape(point)}</li>" for point in slide["learning_objectives"])
    claims = []
    for claim in slide["key_points"]:
        tag = KIND.get(claim["kind"])
        badge = f'<span class="claim-kind">{tag}</span>' if tag else ""
        ids = dict.fromkeys(ref["source_id"] for ref in claim["evidence"])
        sources = " ".join(f'<a class="source" href="#ref-{escape(sid)}">[{escape(sid)}]</a>' for sid in ids)
        claims.append(f'<li class="claim" id="claim-{escape(claim["id"])}">{badge}'
                      f'<p class="statement">{escape(claim["text"])}</p>'
                      f'<div class="citation">{sources}{evidence_markup(claim)}</div></li>')
    refs = references(slide, registry) if "reference_sources" in slide else ""
    visual_name = VISUAL[slide["visual"]["kind"]]
    if n == 3:
        visual_name = "模擬波形"
    return f"""
    <article class="slide{' opening' if n == 1 else ''}" id="slide-{n}" aria-labelledby="heading-{n}">
      <header class="slide-header">
        <h{1 if n == 1 else 2} id="heading-{n}" tabindex="-1">{escape(heading)}</h{1 if n == 1 else 2}>
        <p>{escape(slide["explanation"])}</p>
      </header>
      <div class="slide-grid">
        <section class="lesson" aria-label="投影片重點">
          <details class="objectives"{' open' if n == 1 else ''}><summary>學習目標</summary><ul>{objectives}</ul></details>
          <ul class="claims">{''.join(claims)}</ul>
        </section>
        <section class="visual" aria-label="{visual_name}">
          <h3>{visual_name}</h3>{visual_markup(slide)}
        </section>
      </div>{refs}
    </article>"""


def render() -> str:
    data = json.loads((ROOT / "data/slide-content.json").read_text(encoding="utf-8"))
    sources = json.loads((ROOT / "docs/sources.json").read_text(encoding="utf-8"))
    registry = {source["id"]: source for source in sources if source["status"] == "verified"}
    slides = data["slides"]
    contents = "".join(f'<li><a href="#slide-{s["number"]}">{escape(s["title"])}</a></li>' for s in slides)
    articles = "".join(render_slide(s, data["title"], registry) for s in slides)
    return f"""<!doctype html>
<!-- Generated from data/slide-content.json using scripts/build_presentation.py. -->
<html lang="{escape(data["language"])}">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <meta name="color-scheme" content="dark">
  <title>{escape(data["title"])}</title>
  <link rel="icon" href="data:,">
  <link rel="stylesheet" href="presentation.css">
  <script defer src="presentation.js"></script>
</head>
<body>
  <a class="skip" href="#presentation">跳至簡報內容</a>
  <header class="site-header">
    <a class="wordmark" href="#slide-1"><span aria-hidden="true">◈</span> 語音情緒辨識入門</a>
    <details class="contents"><summary>投影片目錄</summary><ol>{contents}</ol></details>
  </header>
  <main id="presentation" tabindex="-1">{articles}
  </main>
  <nav class="navigation" aria-label="投影片導覽" hidden>
    <button type="button" id="previous">上一張</button>
    <div class="progress">
      <span id="counter" role="status" aria-live="polite" aria-atomic="true">1 / {len(slides)}</span>
      <progress id="progress" value="1" max="{len(slides)}" aria-label="簡報進度"></progress>
    </div>
    <button type="button" id="next">下一張</button>
  </nav>
</body>
</html>
"""


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check sync without writing")
    args = parser.parse_args()
    html = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != html:
            print("Generated presentation is out of date.")
            return 1
        print("Generated presentation matches the validated content artifact.")
    else:
        OUTPUT.write_text(html, encoding="utf-8", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
