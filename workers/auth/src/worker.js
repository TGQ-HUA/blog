// 博客邮箱登录 — Cloudflare Workers
// 部署: npx wrangler deploy
// 配置: npx wrangler secret put RESEND_API_KEY

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname;

    // CORS 预检
    if (request.method === 'OPTIONS') {
      return cors({});
    }

    // 路由
    if (path === '/auth/login' && request.method === 'POST') {
      return handleLogin(request, env);
    }
    if (path === '/auth/verify' && request.method === 'GET') {
      return handleVerify(url, env);
    }
    if (path === '/auth/me' && request.method === 'GET') {
      return handleMe(request, env);
    }
    if (path === '/auth/logout' && request.method === 'POST') {
      return handleLogout();
    }

    return cors(new Response('Not Found', { status: 404 }));
  }
};

// ====== 发送验证邮件 ======
async function handleLogin(request, env) {
  const { email } = await request.json();
  if (!email || !email.includes('@')) {
    return cors(json({ error: '请输入有效邮箱' }, 400));
  }

  // 生成 6 位验证码
  const code = Math.floor(100000 + Math.random() * 900000).toString();
  const expiresAt = new Date(Date.now() + 10 * 60 * 1000).toISOString(); // 10 分钟有效

  // 存入 D1
  await env.DB.prepare(
    'INSERT INTO tokens (email, token, expires_at) VALUES (?, ?, ?)'
  ).bind(email, code, expiresAt).run();

  // 发送邮件
  await sendEmail(email, code, env);

  return cors(json({ ok: true, message: '验证码已发送，请查收邮件' }));
}

// ====== 验证码验证 + 登录 ======
async function handleVerify(url, env) {
  const code = url.searchParams.get('token');
  if (!code) {
    return cors(json({ error: '缺少验证码' }, 400));
  }

  // 查 token
  const row = await env.DB.prepare(
    "SELECT * FROM tokens WHERE token = ? AND used = 0 AND expires_at > datetime('now')"
  ).bind(code).first();

  if (!row) {
    return cors(json({ error: '验证码无效或已过期' }, 400));
  }

  // 标记 token 已用
  await env.DB.prepare('UPDATE tokens SET used = 1 WHERE id = ?').bind(row.id).run();

  // 新用户则创建
  const user = await env.DB.prepare('SELECT * FROM users WHERE email = ?').bind(row.email).first();
  let userId;
  if (!user) {
    const result = await env.DB.prepare('INSERT INTO users (email) VALUES (?)').bind(row.email).run();
    userId = result.meta.last_row_id;
  } else {
    userId = user.id;
  }

  // 生成 session token
  const session = crypto.randomUUID();
  await env.DB.prepare(
    "INSERT INTO tokens (email, token, expires_at) VALUES (?, ?, datetime('now', '+7 days'))"
  ).bind(row.email, session).run();

  // 设 cookie + 返回
  const response = cors(json({ ok: true, email: row.email, id: userId }));
  response.headers.set('Set-Cookie', `session=${session}; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=604800`);
  return response;
}

// ====== 获取当前用户 ======
async function handleMe(request, env) {
  const cookie = request.headers.get('Cookie') || '';
  const match = cookie.match(/session=([^;]+)/);
  if (!match) return cors(json({ user: null }));

  const row = await env.DB.prepare(
    "SELECT u.id, u.email, u.name FROM tokens t JOIN users u ON t.email = u.email WHERE t.token = ? AND t.expires_at > datetime('now')"
  ).bind(match[1]).first();

  if (!row) return cors(json({ user: null }));

  return cors(json({ user: { id: row.id, email: row.email, name: row.name } }));
}

// ====== 登出 ======
async function handleLogout() {
  const response = cors(json({ ok: true }));
  response.headers.set('Set-Cookie', 'session=; HttpOnly; Secure; SameSite=Lax; Path=/; Max-Age=0');
  return response;
}

// ====== 发邮件 ======
async function sendEmail(to, code, env) {
  await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${env.RESEND_API_KEY}`,
      'Content-Type': 'application/json',
    },
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
      </div>`,
    }),
  });
}

// ====== 工具函数 ======
function cors(response) {
  response.headers.set('Access-Control-Allow-Origin', 'https://tangguoqi.top');
  response.headers.set('Access-Control-Allow-Methods', 'GET,POST,OPTIONS');
  response.headers.set('Access-Control-Allow-Headers', 'Content-Type');
  response.headers.set('Access-Control-Allow-Credentials', 'true');
  return response;
}

function json(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { 'Content-Type': 'application/json' },
  });
}
