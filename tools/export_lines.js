const fs = require("fs"), vm = require("vm");
const html = fs.readFileSync(process.argv[2], "utf8");
const code = [...html.matchAll(/<script>([\s\S]*?)<\/script>/g)].map(m => m[1]).find(c => c.includes("function voiceLines"));
const el = () => ({ addEventListener(){}, set innerHTML(v){}, querySelector: () => null, classList: { toggle(){} }, setAttribute(){} });
const ctx = { console, setTimeout: () => 0, clearTimeout(){}, setInterval: () => 0, clearInterval(){}, Promise,
  fetch: () => Promise.reject(new Error("offline")),
  localStorage: { getItem: () => null, setItem(){}, removeItem(){} },
  document: { getElementById: el, addEventListener(){}, querySelectorAll: () => [] } };
ctx.window = ctx; vm.createContext(ctx);
vm.runInContext(code + "\n;globalThis.__lines = voiceLines();", ctx);
const lines = ctx.__lines;
fs.writeFileSync(process.argv[3], JSON.stringify(lines, null, 2));
const chars = lines.reduce((n, l) => n + l.tts.length, 0);
const files = new Set(lines.map(l => l.file));
console.log(JSON.stringify({ lines: lines.length, uniqueFiles: files.size, ttsChars: chars }));
console.log(lines.filter(l => l.tts !== l.text).map(l => l.tts).join("\n"));
