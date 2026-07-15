// 博客邮箱登录 — 无数据库方案（token 签名验证）
export async function onRequest(context) {
  const { request, env } = context;
  const url = new URL(request.url);
  const path = url.pathname.replace('/auth', '');

  if (request.method === 'OPTIONS') return cors(new Response(null, { status: 204 }));

  if (path === '/login' && request.method === 'POST') return handleLogin(request, env);
  if (path === '/verify' && request.method === 'GET') return handleVerify(url, env);
  if (path === '/me' && request.method === 'GET') return handleMe(request, env);
  if (path === '/logout' && request.method === 'POST') return handleLogout();

  return cors(new Response('Not Found', { status: 404 }));
}

// ====== 登录：发验证码 ======
async function handleLogin(request, env) {
  let body;
  try { body = await request.json(); } catch(e) { return cors(json({error:'无效请求'},400)); }
  const email = body.email;
  if (!email || !email.includes('@')) return cors(json({error:'请输入有效邮箱'},400));

  const code = Math.floor(100000 + Math.random() * 900000).toString();

  // 生成签名 token（email+code+过期时间，HMAC 签名防篡改）
  const expires = Date.now() + 10 * 60 * 1000;
  const payload = `${email}|${code}|${expires}`;
  const sig = await sign(payload, env.SECRET || 'blog-secret-key');
  const token = `${payload}|${sig}`;

  await sendEmail(email, code, env);

  return cors(json({ ok: true, message: '验证码已发送，请查收邮件', _t: token }));
}

// ====== 验证：检查 token → 登录 ======
async function handleVerify(url, env) {
  const code = url.searchParams.get('token');
  const fullToken = url.searchParams.get('t') || '';
  if (!code) return cors(json({error:'缺少验证码'},400));

  let email;
  // 验证 token 签名
  if (fullToken) {
    const parts = fullToken.split('|');
    if (parts.length === 4) {
      const [em, cd, exp, sig] = parts;
      const valid = await verify(`${em}|${cd}|${exp}`, sig, env.SECRET || 'blog-secret-key');
      const expired = Date.now() > parseInt(exp);
      if (valid && !expired && cd === code) email = em;
    }
  }
  if (!email) return cors(json({error:'验证码无效或已过期'},400));

  // 生成 session
  const sessionPayload = `${email}|${Date.now() + 7*24*3600*1000}`;
  const sessionSig = await sign(sessionPayload, env.SECRET || 'blog-secret-key');
  const session = `${sessionPayload}|${sessionSig}`;

  const res = cors(json({ ok: true, email, id: 1 }));
  res.headers.set('Set-Cookie', `session=${encodeURIComponent(session)}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=604800`);
  return res;
}

// ====== 获取当前用户 ======
async function handleMe(request, env) {
  const cookie = request.headers.get('Cookie') || '';
  const m = cookie.match(/session=([^;]+)/);
  if (!m) return cors(json({ user: null }));

  const decoded = decodeURIComponent(m[1]);
  const parts = decoded.split('|');
  if (parts.length !== 3) return cors(json({ user: null }));

  const [email, exp, sig] = parts;
  const valid = await verify(`${email}|${exp}`, sig, env.SECRET || 'blog-secret-key');
  const expired = Date.now() > parseInt(exp);
  if (!valid || expired) return cors(json({ user: null }));

  return cors(json({ user: { id: 1, email, name: email.split('@')[0] } }));
}

// ====== 登出 ======
function handleLogout() {
  const res = cors(json({ ok: true }));
  res.headers.set('Set-Cookie', 'session=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0');
  return res;
}

// ====== 发邮件 ======
async function sendEmail(to, code, env) {
  if (!env.RESEND_API_KEY) return;
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { 'Authorization': `Bearer ${env.RESEND_API_KEY}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({
      from: '奇美星暖通风管制作 <noreply@tangguoqi.top>',
      to: [to],
      subject: '登录验证码 - 奇美星的技术博客',
      html: `<div style="font-family:sans-serif;max-width:480px;margin:0 auto">
        <h2 style="color:#2563eb">奇美星的技术博客</h2>
        <p>你的登录验证码：</p>
        <div style="background:#f0f4ff;padding:20px;border-radius:12px;text-align:center;margin:16px 0">
          <span style="font-size:36px;font-weight:900;color:#2563eb;letter-spacing:6px">${code}</span>
        </div>
        <p style="color:#6b7280;font-size:14px">10 分钟内有效，请勿转发给他人。</p>
      </div>`
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
  const expected = await sign(payload, secret);
  return expected === sig;
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
