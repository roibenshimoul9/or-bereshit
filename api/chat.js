// POST /api/chat — the assistant "ארי", answered by Gemini.
// The API key is read from the GEMINI_API_KEY environment variable in Vercel
// and never reaches the browser.
import { SYSTEM_PROMPT, FUNCTION_DECLARATIONS, CATALOG, PAGES } from '../lib/assistant-rules.js';

const MODEL = process.env.GEMINI_MODEL || 'gemini-2.5-flash';
const ENDPOINT = `https://generativelanguage.googleapis.com/v1beta/models/${encodeURIComponent(MODEL)}:generateContent`;

const MAX_MESSAGES = 20;
const MAX_CHARS = 1500;
const MAX_ROUNDS = 3;            // model turns per request, including tool rounds

// Best-effort rate limit per visitor. It lives in one server instance's memory,
// so it slows down abuse rather than guaranteeing a hard cap.
const WINDOW_MS = 10 * 60 * 1000;
const MAX_PER_WINDOW = 30;
const hits = new Map();
function rateLimited(ip) {
  const now = Date.now();
  const entry = hits.get(ip);
  if (!entry || now > entry.reset) {
    hits.set(ip, { count: 1, reset: now + WINDOW_MS });
    if (hits.size > 5000) for (const [k, v] of hits) if (now > v.reset) hits.delete(k);
    return false;
  }
  entry.count += 1;
  return entry.count > MAX_PER_WINDOW;
}

function readMessages(body) {
  const list = body && Array.isArray(body.messages) ? body.messages : null;
  if (!list || !list.length || list.length > MAX_MESSAGES) return null;
  const clean = [];
  for (const m of list) {
    if (!m || (m.role !== 'user' && m.role !== 'assistant') || typeof m.content !== 'string') return null;
    const text = m.content.trim().slice(0, MAX_CHARS);
    if (!text) return null;
    clean.push({ role: m.role === 'assistant' ? 'model' : 'user', parts: [{ text }] });
  }
  while (clean.length && clean[0].role !== 'user') clean.shift();
  if (!clean.length || clean[clean.length - 1].role !== 'user') return null;
  return clean;
}

// Checks a tool call from the model; returns a browser action or an error for the model.
function checkCall(call) {
  const args = call.args || {};
  if (call.name === 'add_to_cart') {
    const product = CATALOG.find(p => p.id === String(args.product_id));
    if (!product) return { error: 'unknown product_id' };
    if (!product.price) return { error: 'this product is priced on request; point the shopper to WhatsApp' };
    return { action: { name: 'add_to_cart', args: { product_id: product.id } }, result: `added ${product.name} to the cart` };
  }
  if (call.name === 'open_page') {
    const page = String(args.page);
    if (!PAGES.includes(page)) return { error: 'unknown page' };
    return { action: { name: 'open_page', args: { page } }, result: `opened page ${page}` };
  }
  return { error: 'unknown tool' };
}

async function callGemini(contents, key) {
  const generationConfig = { temperature: 0.6, maxOutputTokens: 700 };
  // Flash models answer faster without extended thinking; other models keep their defaults.
  if (/flash/i.test(MODEL)) generationConfig.thinkingConfig = { thinkingBudget: 0 };
  const res = await fetch(ENDPOINT, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'x-goog-api-key': key },
    body: JSON.stringify({
      systemInstruction: { parts: [{ text: SYSTEM_PROMPT }] },
      contents,
      tools: [{ functionDeclarations: FUNCTION_DECLARATIONS }],
      generationConfig,
    }),
    signal: AbortSignal.timeout(25000),
  });
  if (!res.ok) {
    const err = new Error('gemini_http_' + res.status);
    err.status = res.status;
    throw err;
  }
  return res.json();
}

export default async function handler(req, res) {
  res.setHeader('Cache-Control', 'no-store');
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST');
    return res.status(405).json({ error: 'method_not_allowed' });
  }

  const key = process.env.GEMINI_API_KEY;
  if (!key) return res.status(503).json({ error: 'not_configured' });

  const ip = String(req.headers['x-forwarded-for'] || '').split(',')[0].trim() || 'unknown';
  if (rateLimited(ip)) return res.status(429).json({ error: 'rate_limited' });

  let body = req.body;
  if (typeof body === 'string') { try { body = JSON.parse(body); } catch { body = null; } }
  const contents = readMessages(body);
  if (!contents) return res.status(400).json({ error: 'bad_request' });

  const actions = [];
  const textParts = [];
  try {
    for (let round = 0; round < MAX_ROUNDS; round++) {
      const data = await callGemini(contents, key);
      const candidate = data && data.candidates && data.candidates[0];
      const parts = (candidate && candidate.content && candidate.content.parts) || [];
      for (const p of parts) if (typeof p.text === 'string' && p.text.trim() && !p.thought) textParts.push(p.text.trim());
      const calls = parts.filter(p => p.functionCall).map(p => p.functionCall);
      if (!calls.length) break;

      // Tools run in the shopper's browser; tell the model what happened so it can wrap up.
      contents.push({ role: 'model', parts });
      contents.push({
        role: 'user',
        parts: calls.map(call => {
          const checked = checkCall(call);
          if (checked.action) actions.push(checked.action);
          return { functionResponse: { name: call.name, response: checked.action ? { result: checked.result } : { error: checked.error } } };
        }),
      });
    }
  } catch (err) {
    const status = err && err.status === 429 ? 429 : 502;
    return res.status(status).json({ error: status === 429 ? 'rate_limited' : 'upstream_error' });
  }

  const text = textParts.join('\n\n').trim();
  if (!text && !actions.length) return res.status(502).json({ error: 'empty' });
  return res.status(200).json({ text: text || 'בוצע.', actions });
}
