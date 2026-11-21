// Run with Node and a local Chromium-family browser executable.
import assert from "node:assert/strict";
import {spawn} from "node:child_process";
import {access, mkdtemp, readFile, rm} from "node:fs/promises";
import {tmpdir} from "node:os";
import {join} from "node:path";
import {once} from "node:events";
import {createServer} from "node:http";

const executable = process.argv[2] || process.env.CHROME_BIN;
assert(executable, "Pass a Chrome executable path or set CHROME_BIN.");
const page = new URL("../slides/index.html", import.meta.url);
const dataset = JSON.parse(await readFile(new URL("../data/slide-content.json", import.meta.url), "utf8"));
const registry = JSON.parse(await readFile(new URL("../docs/sources.json", import.meta.url), "utf8"));
const html = await readFile(page, "utf8");
const assets = [...html.matchAll(/<(?:script|link)\b[^>]*\b(?:src|href)="([^"]+)"/g)]
  .filter(([, value]) => !value.startsWith("data:"));
assert.equal(assets.length, 2);
for (const [, path] of assets) {
  const asset = new URL(path, page);
  assert(asset.href.startsWith(new URL("./", page).href));
  await access(asset);
}

const prefix = "/ser-llm-wiki/";
const files = new Map([
  ["index.html", ["text/html; charset=utf-8", html]],
  ["presentation.css", ["text/css; charset=utf-8", await readFile(new URL("presentation.css", page))]],
  ["presentation.js", ["text/javascript; charset=utf-8", await readFile(new URL("presentation.js", page))]],
]);
const requests = [];
const server = createServer((request, response) => {
  const pathname = new URL(request.url, "http://localhost").pathname;
  const file = pathname.startsWith(prefix) && files.get(pathname.slice(prefix.length) || "index.html");
  requests.push([pathname, Boolean(file)]);
  if (!file) return response.writeHead(404).end();
  response.writeHead(200, {"Content-Type": file[0]}).end(file[1]);
});
const profile = await mkdtemp(join(tmpdir(), "ser-slides-smoke-"));
const chrome = spawn(executable, [
  "--headless=new", "--disable-gpu", "--no-first-run", "--no-default-browser-check",
  "--disable-background-networking", "--disable-component-update", "--disable-sync",
  "--remote-debugging-pipe", `--user-data-dir=${profile}`,
], {stdio: ["ignore", "ignore", "ignore", "pipe", "pipe"]});
const pending = new Map();
const browserErrors = [];
let id = 0;
let incoming = "";
chrome.stdio[4].setEncoding("utf8");
chrome.stdio[3].on("error", () => {}); // Exit handling rejects outstanding commands.
chrome.stdio[4].on("data", (chunk) => {
  incoming += chunk;
  const parts = incoming.split("\0");
  incoming = parts.pop();
  for (const part of parts) {
    const response = JSON.parse(part);
    if (response.method === "Runtime.exceptionThrown") {
      browserErrors.push(response.params.exceptionDetails.exception?.description ||
                         response.params.exceptionDetails.text);
    }
    if (response.method === "Runtime.consoleAPICalled" && response.params.type === "error") {
      browserErrors.push(response.params.args.map((entry) => entry.value ?? entry.description).join(" "));
    }
    if (response.method === "Log.entryAdded" && response.params.entry.level === "error") {
      browserErrors.push(response.params.entry.text);
    }
    const callback = pending.get(response.id);
    if (callback) {
      pending.delete(response.id);
      callback(response);
    }
  }
});

function send(method, params = {}, sessionId) {
  const requestId = ++id;
  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      pending.delete(requestId);
      reject(new Error(`CDP timeout: ${method}`));
    }, 7000);
    pending.set(requestId, (response) => {
      clearTimeout(timeout);
      if (response.error) reject(new Error(response.error.message));
      else resolve(response.result);
    });
    chrome.stdio[3].write(JSON.stringify({id: requestId, method, params, sessionId}) + "\0");
  });
}
function failPending(reason) {
  for (const callback of pending.values()) callback({error: {message: reason}});
  pending.clear();
}
chrome.on("error", (error) => failPending(error.message));
chrome.on("exit", (code) => failPending(`Browser exited: ${code}`));

try {
  server.listen(0, "127.0.0.1");
  await once(server, "listening");
  const local = `http://127.0.0.1:${server.address().port}${prefix}`;
  const {targetId} = await send("Target.createTarget", {url: "about:blank"});
  const {sessionId} = await send("Target.attachToTarget", {targetId, flatten: true});
  const call = (method, params = {}) => send(method, params, sessionId);
  await call("Runtime.enable");
  await call("Log.enable");
  const evaluate = async (expression) => {
    const {result, exceptionDetails} = await call("Runtime.evaluate", {expression, returnByValue: true});
    assert(!exceptionDetails, exceptionDetails?.exception?.description);
    return result.value;
  };
  const wait = async (expression) => {
    for (let i = 0; i < 60; i++) {
      if (await evaluate(expression)) return;
      await new Promise((resolve) => setTimeout(resolve, 50));
    }
    assert.fail(`Browser did not reach: ${expression}`);
  };
  const viewport = (width, height, mobile = false) => call("Emulation.setDeviceMetricsOverride", {
    width, height, mobile, deviceScaleFactor: 1,
  });
  await viewport(1440, 900);
  await call("Page.navigate", {url: local});
  await wait("document.documentElement.classList.contains('enhanced')");
  const current = () => evaluate("document.querySelector('.slide:not([hidden])').id");
  const click = (selector) => evaluate(`document.querySelector(${JSON.stringify(selector)}).click()`);
  const key = async (name, code, modifiers = 0) => {
    const params = {key: name, windowsVirtualKeyCode: code, modifiers};
    await call("Input.dispatchKeyEvent", {type: "keyDown", ...params, ...(name === "Enter" ? {text: "\r"} : {})});
    await call("Input.dispatchKeyEvent", {type: "keyUp", ...params});
  };
  const expectPosition = async (n) => {
    assert.equal(await current(), `slide-${n}`);
    assert.equal(await evaluate("document.querySelectorAll('.slide:not([hidden])').length"), 1);
    assert.equal(await evaluate("document.querySelector('#progress').value"), n);
    assert.equal(await evaluate("document.querySelector('#counter').textContent"), `${n} / 12`);
    assert.equal(await evaluate("document.querySelector('.contents a[aria-current]').hash"), `#slide-${n}`);
  };
  assert.equal(await current(), "slide-1");
  assert.equal(await evaluate("getComputedStyle(document.body).backgroundColor"), "rgb(11, 17, 25)");
  assert.equal(await evaluate("document.querySelector('#previous').disabled"), true);
  await click("#next");
  assert.equal(await current(), "slide-2");
  assert.equal(await evaluate("document.activeElement.id"), "heading-2");
  await key("ArrowRight", 39);
  assert.equal(await current(), "slide-3");
  assert.equal(await evaluate("document.querySelector('#progress').value"), 3);
  const waveform = await evaluate("document.querySelector('#waveform').toDataURL()");
  await evaluate("document.querySelector('#frequency').focus()");
  await key("ArrowRight", 39);
  assert.equal(await current(), "slide-3");
  assert.equal(await evaluate("document.querySelector('#frequency-value').textContent"), "4");
  assert.notEqual(await evaluate("document.querySelector('#waveform').toDataURL()"), waveform);
  await key("Tab", 9);
  assert.equal(await evaluate("document.activeElement.id"), "amplitude");
  await key("ArrowLeft", 37);
  assert.equal(await evaluate("document.querySelector('#amplitude-value').textContent"), "64");
  await click("#previous");
  assert.equal(await current(), "slide-2");
  await click(".contents a[href='#slide-5']");
  assert(await evaluate(`(() => {
    const plot = document.querySelector(".affect-plot").getBoundingClientRect();
    const points = [...document.querySelectorAll(".affect-example")].map(e => e.getBoundingClientRect());
    const middle = plot.left + plot.width / 2;
    return points.length === 2 && points.every(p => p.bottom < plot.top + plot.height / 2)
      && points[0].right < middle && points[1].left > middle;
  })()`));
  await evaluate(`(() => {
    const input = document.querySelector("#valence");
    input.value = "70"; input.dispatchEvent(new Event("input"));
  })()`);
  assert.equal(await evaluate("document.querySelector('#valence-value').textContent"), "70");
  assert.notEqual(await evaluate("document.querySelector('#affect-point').style.left"), "50%");
  await evaluate("document.querySelector('#valence').focus()");
  await key("Tab", 9);
  assert.equal(await evaluate("document.activeElement.id"), "arousal");
  await key("ArrowRight", 39);
  assert.equal(await evaluate("document.querySelector('#arousal-value').textContent"), "1");
  assert.notEqual(await evaluate("document.querySelector('#affect-point').style.top"), "50%");
  await click(".contents a[href='#slide-6']");
  await click(".pipeline summary");
  assert(await evaluate("document.querySelector('.pipeline details').open"));
  await click(".contents a[href='#slide-10']");
  await click(".exercise summary");
  assert(await evaluate("document.querySelector('.exercise').open"));
  await click(".contents a[href='#slide-12']");
  for (const [index, question] of dataset.slides.at(-1).quiz.entries()) {
    const item = `.quiz details:nth-child(${index + 1})`;
    await evaluate(`document.querySelector("${item} summary").focus()`);
    await key("Enter", 13);
    assert(await evaluate(`document.querySelector("${item}").open`));
    const claim = dataset.slides.at(-1).key_points.find((point) => point.id === question.answer_claim_id);
    assert((await evaluate(`document.querySelector("${item} p").textContent`)).startsWith(claim.text));
  }
  assert(await evaluate("document.querySelector('#next').disabled"));
  assert.equal(await evaluate("document.querySelector('#counter').textContent"), "12 / 12");

  const claims = await evaluate(`Array.from(document.querySelectorAll(".claim"), item => ({
    id: item.id.slice(6), text: item.querySelector(".statement").textContent,
    sources: Array.from(item.querySelectorAll(".source"), link => link.hash.slice(5)),
    passageIds: Array.from(item.querySelectorAll(".evidence code"), block => block.textContent),
    locations: Array.from(item.querySelectorAll(".evidence p"), block => block.textContent),
    excerpts: Array.from(item.querySelectorAll(".evidence blockquote"), block => block.textContent)
  }))`);
  assert.deepEqual(claims, dataset.slides.flatMap((slide) => slide.key_points.map((claim) => ({
    id: claim.id, text: claim.text,
    sources: [...new Set(claim.evidence.map((entry) => entry.source_id))],
    passageIds: claim.evidence.map((entry) => entry.passage_id),
    locations: claim.evidence.map((entry) => `[${entry.source_id}] ${entry.location}`),
    excerpts: claim.evidence.map((entry) => entry.excerpt),
  }))));
  const outlines = await evaluate(`Array.from(document.querySelectorAll(".slide"), item => ({
    title: item.querySelector("h1,h2").textContent,
    explanation: item.querySelector(".slide-header p").textContent,
    objectives: Array.from(item.querySelectorAll(".objectives li"), entry => entry.textContent)
  }))`);
  assert.deepEqual(outlines, dataset.slides.map((slide, index) => ({
    title: index === 0 ? dataset.title : slide.title,
    explanation: slide.explanation, objectives: slide.learning_objectives,
  })));
  const refs = await evaluate(`Array.from(document.querySelectorAll(".references li"), entry => ({
    id: entry.id.slice(4), url: entry.querySelector("a").getAttribute("href")
  }))`);
  assert.deepEqual(refs, dataset.slides.at(-1).reference_sources.map((id) => {
    const source = registry.find((entry) => entry.id === id && entry.status === "verified");
    return {id, url: source.url};
  }));
  await click(".contents a[href='#slide-4']");
  await click("#slide-4 .source");
  assert.equal(await current(), "slide-12");
  assert.equal(await evaluate("document.activeElement.id"), "ref-S02");
  await evaluate("history.back()");
  await wait("document.querySelector('.slide:not([hidden])').id === 'slide-4'");
  await evaluate("history.forward()");
  await wait("document.activeElement.id === 'ref-S02'");
  await click(".wordmark");
  await expectPosition(1);
  for (let n = 2; n <= 12; n++) {
    await click("#next");
    await expectPosition(n);
  }
  await key("ArrowRight", 39);
  await expectPosition(12);
  for (let n = 11; n >= 1; n--) {
    await key("ArrowLeft", 37);
    await expectPosition(n);
  }
  await key("ArrowLeft", 37);
  await expectPosition(1);

  for (const [width, height, mobile] of [[1440, 900, false], [390, 844, true], [320, 700, true]]) {
    await viewport(width, height, mobile);
    for (let i = 1; i <= dataset.slides.length; i++) {
      await click(`.contents a[href='#slide-${i}']`);
      assert.equal(await current(), `slide-${i}`);
      assert(await evaluate("document.documentElement.scrollWidth <= innerWidth"),
        `Horizontal overflow on slide ${i} at ${width}px`);
      assert(await evaluate(`[...document.querySelector(".slide:not([hidden])").querySelectorAll("h1,h2,p,summary,th,td,label")]
        .filter(e => e.getClientRects().length).every(e => parseFloat(getComputedStyle(e).fontSize) >= 14)`));
      const contrast = await evaluate(`(() => {
        function luminance(color) {
          const rgb = color.match(/[0-9]+(?:[.][0-9]+)?/g).slice(0, 3).map(Number);
          const channels = rgb.map(n => (n /= 255) <= .04045 ? n / 12.92 : ((n + .055) / 1.055) ** 2.4);
          return .2126 * channels[0] + .7152 * channels[1] + .0722 * channels[2];
        }
        function background(element) {
          for (let node = element; node; node = node.parentElement) {
            const style = getComputedStyle(node);
            if (style.backgroundImage.startsWith("linear-gradient")) {
              const stops = Array.from(style.backgroundImage.matchAll(/rgb[(][^)]*[)]/g), m => luminance(m[0]));
              return Math.max(...stops);
            }
            if (style.backgroundColor !== "rgba(0, 0, 0, 0)") return luminance(style.backgroundColor);
          }
          return 0;
        }
        const scope = document.querySelector(".slide:not([hidden])");
        const items = [...scope.querySelectorAll("h1,h2,h3,p,summary,th,td,label,output,.citation a,.affect-plot span")];
        return Math.min(...items.filter(e => e.getClientRects().length).map(e => {
          const fg = luminance(getComputedStyle(e).color);
          const bg = background(e);
          return (Math.max(fg, bg) + .05) / (Math.min(fg, bg) + .05);
        }));
      })()`);
      assert(contrast >= 4.5, `Text contrast ${contrast} on slide ${i} at ${width}px`);
    }
  }
  await call("Emulation.setEmulatedMedia", {features: [{name: "prefers-reduced-motion", value: "reduce"}]});
  assert.equal(await evaluate("getComputedStyle(document.querySelector('.slide:not([hidden])')).animationName"), "none");
  await call("Page.navigate", {url: local + "#slide-8"});
  await wait("document.activeElement.id === 'heading-8'");
  await expectPosition(8);
  await call("Page.navigate", {url: local + "#ref-S07"});
  await wait("document.activeElement.id === 'ref-S07'");
  await click(".skip");
  assert.equal(await evaluate("document.activeElement.id"), "presentation");
  await call("Emulation.setScriptExecutionDisabled", {value: true});
  await call("Page.navigate", {url: local + "?fallback"});
  await wait("document.querySelectorAll('.slide:not([hidden])').length === 12");
  assert(await evaluate("document.querySelector('#frequency').disabled"));
  assert.deepEqual(browserErrors, [], `Browser errors; HTTP requests: ${JSON.stringify(requests)}`);
  assert.deepEqual(requests.filter(([, ok]) => !ok), [], "Unexpected or missing web assets");
  for (const asset of ["presentation.css", "presentation.js"]) {
    assert(requests.some(([path, ok]) => path === prefix + asset && ok), `No request for ${asset}`);
  }
  console.log("PASS: Pages-style HTTP subpath, no console errors or missing assets, 31 claims, 7 references, all navigation paths, keyboard demos and quiz, 36 layout/contrast checks, and reduced-motion/no-JS fallbacks.");
} finally {
  if (chrome.exitCode === null && chrome.pid) {
    const exited = once(chrome, "exit");
    chrome.kill();
    await exited;
  }
  await rm(profile, {recursive: true, force: true, maxRetries: 3, retryDelay: 100});
  await new Promise((resolve) => server.close(resolve));
}
