---
title: "管件排版规范"
description: "暖通风管制造技术部内部规范文档——基础总则、管件分类、排版流程、设备操作、中国标准等"
categories:
  - 管件排版规范
weight: 1
---

> ⚠️ 本内容为风管厂技术部内部参考资料，仅供学习交流，不构成任何商业建议。

<div id="locked" style="text-align:center;padding:40px;">
  <h3>🔒 需要密码</h3>
  <input type="password" id="pwd" placeholder="请输入密码" style="padding:8px 16px;border-radius:8px;border:1px solid #ccc;font-size:16px;margin:8px;">
  <button onclick="unlock()" style="padding:8px 20px;border-radius:8px;background:var(--accent-color,#007AFF);color:#fff;border:none;font-size:16px;cursor:pointer;">确认</button>
  <p id="err" style="color:red;margin-top:8px;display:none;">密码错误</p>
</div>
<div id="content" style="display:none;">
{{ range .Pages.ByWeight }}
- [{{ .Title }}]({{ .RelPermalink }})
{{ end }}
</div>

<script>
// 密码哈希（部署前请告诉老唐设密码，我生成 hash 替换下面）
const PWD_HASH = '123456';

async function sha256(s) {
  const buf = new TextEncoder().encode(s);
  const hash = await crypto.subtle.digest('SHA-256', buf);
  return Array.from(new Uint8Array(hash)).map(b => b.toString(16).padStart(2, '0')).join('');
}

async function unlock() {
  const input = document.getElementById('pwd').value;
  const h = await sha256(input);
  if (h === PWD_HASH) {
    document.getElementById('locked').style.display = 'none';
    document.getElementById('content').style.display = 'block';
    sessionStorage.setItem('pipe_ok', '1');
  } else {
    document.getElementById('err').style.display = 'block';
  }
}

// 已登录则跳过
if (sessionStorage.getItem('pipe_ok') === '1') {
  document.getElementById('locked').style.display = 'none';
  document.getElementById('content').style.display = 'block';
}
</script>
