// 博客邮箱登录 + 评论系统 — Cloudflare Workers
let tablesReady = false;

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    if (request.method === 'OPTIONS') return cors(new Response(null, { status: 204 }));
    
    try {
      // 登录
      if (path === '/auth/login' && request.method === 'POST') return await handleLogin(request, env);
      if (path === '/auth/verify' && request.method === 'GET') return await handleVerify(url, env);
      if (path === '/auth/me' && request.method === 'GET') return await handleMe(request, env);
      if (path === '/auth/logout') return handleLogout();

      // 评论
      if (path === '/auth/comment' && request.method === 'POST') return await handleComment(request, env);
      if (path === '/auth/comment' && request.method === 'GET') return await getComments(url, env);

      return cors(new Response('Not Found', { status: 404 }));
    } catch(e) {
      return cors(json({ error: e.message }, 500));
    }
  }
};

// ====== 确保表存在 ======
async function ensureTables(env) {
  if (tablesReady) return;
  await env.DB.prepare(`CREATE TABLE IF NOT EXISTS comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_email TEXT NOT NULL,
    article_slug TEXT NOT NULL,
    content TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
  )`).run();
  await env.DB.prepare(`CREATE INDEX IF NOT EXISTS idx_comments_slug ON comments(article_slug)`).run();
  tablesReady = true;
}

// ====== 发布评论 ======
async function handleComment(request, env) {
  await ensureTables(env);

  // 验证登录
  const user = await getSession(request, env);
  if (!user) return cors(json({ error: '请先登录' }, 401));

  let body;
  try { body = await request.json(); } catch(e) { return cors(json({error:'无效请求'},400)); }

  const { slug, content } = body;
  if (!slug || !content) return cors(json({ error: '缺少参数' }, 400));
  if (content.length > 500) return cors(json({ error: '评论不能超过500字' }, 400));
  if (content.length < 2) return cors(json({ error: '评论太短' }, 400));

  // 今天是否已评论过这篇文章
  const today = new Date().toISOString().slice(0, 10); // YYYY-MM-DD
  const existing = await env.DB.prepare(
    "SELECT id FROM comments WHERE user_email=? AND article_slug=? AND created_at>=? AND created_at<?"
  ).bind(user.email, slug, today + ' 00:00:00', today + ' 23:59:59').first();
  if (existing) return cors(json({ error: '今天已经评论过这篇文章了，明天再来吧' }, 429));

  await env.DB.prepare(
    'INSERT INTO comments (user_email, article_slug, content) VALUES (?,?,?)'
  ).bind(user.email, slug, content).run();

  return cors(json({ ok: true, message: '评论发布成功' }));
}

// ====== 获取评论 ======
async function getComments(url, env) {
  await ensureTables(env);

  const slug = url.searchParams.get('slug');
  if (!slug) return cors(json({ error: '缺少文章标识' }, 400));

  const { results } = await env.DB.prepare(
    "SELECT id, user_email, content, created_at FROM comments WHERE article_slug=? ORDER BY created_at DESC LIMIT 50"
  ).bind(slug).all();

  return cors(json({ comments: results.map(r => ({
    id: r.id,
    email: r.user_email.replace(/(.{3}).*(@.*)/, '$1***$2'), // 邮箱脱敏
    content: r.content,
    time: r.created_at
  })) }));
}

// ====== Session 验证 ======
async function getSession(request, env) {
  const cookie = request.headers.get('Cookie') || '';
  const m = cookie.match(/session=([^;]+)/);
  if (!m) return null;

  const decoded = decodeURIComponent(m[1]);
  const parts = decoded.split('|');
  if (parts.length !== 3) return null;

  const [email, exp, sig] = parts;
  const valid = await verify(`${email}|${exp}`, sig, env.SECRET || 'blog-secret');
  if (!valid || Date.now() > parseInt(exp)) return null;

  return { id: 1, email, name: email.split('@')[0] };
}

// ====== 登录相关 ======
async function handleLogin(request, env) {
  let body;
  try { body = await request.json(); } catch(e) { return cors(json({error:'无效请求'},400)); }
  const email = body.email;
  if (!email || !email.includes('@')) return cors(json({error:'请输入有效邮箱'},400));

  const code = Math.floor(100000 + Math.random() * 900000).toString();
  const expires = Date.now() + 10 * 60 * 1000;
  const payload = `${email}|${code}|${expires}`;
  const sig = await sign(payload, env.SECRET || 'blog-secret');
  const token = `${payload}|${sig}`;

  try { await sendEmail(email, code, env); } catch(e) {
    return cors(json({ ok: true, message: '验证码：'+code, _t: token }));
  }
  return cors(json({ ok: true, message: '验证码已发送，请查收邮件', _t: token }));
}

async function handleVerify(url, env) {
  const code = url.searchParams.get('token');
  const fullToken = decodeURIComponent(url.searchParams.get('t') || '');
  if (!code) return cors(json({error:'缺少验证码'},400));

  let email;
  if (fullToken) {
    const parts = fullToken.split('|');
    if (parts.length === 4) {
      const [em, cd, exp, sig] = parts;
      const valid = await verify(`${em}|${cd}|${exp}`, sig, env.SECRET || 'blog-secret');
      if (valid && Date.now() <= parseInt(exp) && cd === code) email = em;
    }
  }
  if (!email) return cors(json({error:'验证码无效或已过期'},400));

  const sessionPayload = `${email}|${Date.now() + 7*24*3600*1000}`;
  const sessionSig = await sign(sessionPayload, env.SECRET || 'blog-secret');
  const session = `${sessionPayload}|${sessionSig}`;

  const res = cors(json({ ok: true, email, id: 1 }));
  res.headers.set('Set-Cookie', `session=${encodeURIComponent(session)}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=604800`);
  return res;
}

async function handleMe(request, env) {
  const user = await getSession(request, env);
  return cors(json({ user }));
}

function handleLogout() {
  return new Response(null, {
    status: 302,
    headers: {
      'Location': '/',
      'Set-Cookie': 'session=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0'
    }
  });
}

// ====== 邮件 ======
async function sendEmail(to, code, env) {
  if (!env.RESEND_API_KEY) return;
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: '奇美星暖通风管制作 <noreply@tangguoqi.top>',
      to: [to],
      subject: '登录验证码 - 奇美星的技术博客',
      html: `<!DOCTYPE html><html><head><meta charset="utf-8"></head><body style="font-family:sans-serif;max-width:480px;margin:0 auto">
        <h2 style="color:#2563eb">奇美星的技术博客</h2>
        <p>你的登录验证码：</p>
        <div style="background:#f0f4ff;padding:20px;border-radius:12px;text-align:center;margin:16px 0">
          <span style="font-size:36px;font-weight:900;color:#2563eb;letter-spacing:6px">${code}</span>
        </div>
        <p style="color:#6b7280;font-size:14px">10分钟内有效</p>
      </body></html>`
    })
  });
}

// ====== HMAC 签名 ======
async function sign(payload, secret) {
  const key = await crypto.subtle.importKey('raw', new TextEncoder().encode(secret),
    { name: 'HMAC', hash: 'SHA-256' }, false, ['sign']);
  const sig = await crypto.subtle.sign('HMAC', key, new TextEncoder().encode(payload));
  return btoa(String.fromCharCode(...new Uint8Array(sig)));
}
async function verify(payload, sig, secret) {
  return await sign(payload, secret) === sig;
}

// ====== 工具 ======
function cors(r) {
  r.headers.set('Access-Control-Allow-Origin', 'https://tangguoqi.top');
  r.headers.set('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  r.headers.set('Access-Control-Allow-Headers', 'Content-Type');
  r.headers.set('Access-Control-Allow-Credentials', 'true');
  return r;
}
function json(d, s = 200) {
  return new Response(JSON.stringify(d), { status: s, headers: { 'Content-Type': 'application/json' } });
}
