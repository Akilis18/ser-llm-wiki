"use strict";

const slides = Array.from(document.querySelectorAll(".slide"));
const previous = document.querySelector("#previous");
const next = document.querySelector("#next");
const counter = document.querySelector("#counter");
const progress = document.querySelector("#progress");
const contents = document.querySelector(".contents");
const menuLinks = Array.from(contents.querySelectorAll("a"));
let active = -1;

function showSlide(index) {
  active = index;
  slides.forEach((slide, position) => {
    slide.hidden = position !== index;
    if (position === index) menuLinks[position].setAttribute("aria-current", "page");
    else menuLinks[position].removeAttribute("aria-current");
  });
  previous.disabled = index === 0;
  next.disabled = index === slides.length - 1;
  counter.textContent = `${index + 1} / ${slides.length}`;
  progress.value = index + 1;
  if (index === 2) drawWaveform();
}

function resolveHash(focus) {
  const target = document.getElementById(location.hash.slice(1));
  const slide = target?.closest(".slide");
  if (slide) {
    const index = slides.indexOf(slide);
    if (index !== active) showSlide(index);
    if (focus) {
      const destination = target === slide ? slide.querySelector("h1, h2") : target;
      destination.focus({preventScroll: true});
      destination.scrollIntoView({block: "start", behavior: "instant"});
    }
  } else if (active === -1 || !location.hash) {
    showSlide(0);
  }
}

function goTo(hash) {
  if (location.hash !== hash) history.pushState(null, "", hash);
  resolveHash(true);
}

function move(offset) {
  const index = active + offset;
  if (index >= 0 && index < slides.length) goTo(`#${slides[index].id}`);
}

previous.addEventListener("click", () => move(-1));
next.addEventListener("click", () => move(1));
window.addEventListener("hashchange", () => resolveHash(true));

document.addEventListener("click", (event) => {
  const link = event.target.closest("a[href^='#slide-'], a[href^='#ref-']");
  if (!link || event.defaultPrevented || event.button !== 0 || event.altKey ||
      event.ctrlKey || event.metaKey || event.shiftKey) return;
  event.preventDefault();
  contents.open = false;
  goTo(link.getAttribute("href"));
});

document.addEventListener("keydown", (event) => {
  if (event.defaultPrevented || event.altKey || event.ctrlKey || event.metaKey ||
      event.shiftKey || event.target.closest("input, select, textarea, [contenteditable]")) return;
  const offset = {"ArrowLeft": -1, "ArrowRight": 1}[event.key];
  if (offset) {
    event.preventDefault();
    move(offset);
  }
});

const canvas = document.querySelector("#waveform");
const frequency = document.querySelector("#frequency");
const amplitude = document.querySelector("#amplitude");

function drawWaveform() {
  const width = canvas.clientWidth;
  const height = canvas.clientHeight;
  const context = canvas.getContext("2d");
  if (!width || !height || !context) return;
  const scale = window.devicePixelRatio || 1;
  canvas.width = Math.round(width * scale);
  canvas.height = Math.round(height * scale);
  context.scale(scale, scale);
  const center = height / 2;
  const peak = center * .82 * Number(amplitude.value) / 100;
  const yAt = (x) => center - peak * Math.sin(x * Math.PI * 2 * Number(frequency.value));
  context.strokeStyle = "#476277";
  context.lineWidth = 1;
  context.beginPath();
  context.moveTo(0, center);
  context.lineTo(width, center);
  context.stroke();
  context.strokeStyle = "#87efd5";
  context.lineWidth = 2;
  context.beginPath();
  for (let x = 0; x <= width; x++) {
    if (x === 0) context.moveTo(x, yAt(0));
    else context.lineTo(x, yAt(x / width));
  }
  context.stroke();
  context.fillStyle = "#e5fff7";
  for (let sample = 1; sample < 40; sample++) {
    const ratio = sample / 40;
    context.beginPath();
    context.arc(ratio * width, yAt(ratio), 1.8, 0, Math.PI * 2);
    context.fill();
  }
  canvas.setAttribute("aria-label", `模擬波形，每視窗 ${frequency.value} 個週期，振幅 ${amplitude.value}%`);
}

const valence = document.querySelector("#valence");
const arousal = document.querySelector("#arousal");
const point = document.querySelector("#affect-point");

function drawAffect() {
  point.style.left = `${50 + Number(valence.value) * .34}%`;
  point.style.top = `${50 - Number(arousal.value) * .34}%`;
  point.parentElement.setAttribute("aria-label", `假想座標，愉悅度 ${valence.value}，喚起度 ${arousal.value}`);
}

for (const [inputs, update] of [[[frequency, amplitude], drawWaveform], [[valence, arousal], drawAffect]]) {
  for (const input of inputs) {
    input.disabled = false;
    input.addEventListener("input", () => {
      document.getElementById(`${input.id}-value`).textContent = input.value;
      update();
    });
  }
}

if ("ResizeObserver" in window) new ResizeObserver(drawWaveform).observe(canvas);
else window.addEventListener("resize", drawWaveform);
drawAffect();
resolveHash(Boolean(location.hash));
document.documentElement.classList.add("enhanced");
document.querySelector(".navigation").hidden = false;
