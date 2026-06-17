export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const path = url.pathname.replace(/^\/+/, '');

    // 密码验证
    function checkAuth(request) {
      const auth = request.headers.get('Authorization');
      const expected = `Bearer ${env.UPLOAD_PASSWORD}`;
      return auth === expected;
    }

    try {
      // GET / —— 文件列表
      if (request.method === 'GET' && (!path || path === '')) {
        const objects = [];
        const result = await env.FILES.list();
        const keys = result.objects;
        for (const obj of keys) {
          objects.push({
            name: obj.key,
            size: obj.size,
            uploaded: obj.uploaded,
          });
        }
        return Response.json({ files: objects });
      }

      // POST /upload —— 上传文件（需要密码）
      if (request.method === 'POST' && path === 'upload') {
        if (!checkAuth(request)) {
          return new Response('密码错误', { status: 401 });
        }
        const formData = await request.formData();
        const file = formData.get('file');
        if (!file || typeof file === 'string') {
          return new Response('没有文件', { status: 400 });
        }
        const name = file.name || `${Date.now()}.bin`;
        await env.FILES.put(name, file.stream(), {
          httpMetadata: { contentType: file.type || 'application/octet-stream' },
        });
        return Response.json({ ok: true, name });
      }

      // DELETE /:filename —— 删除文件（需要密码）
      if (request.method === 'DELETE' && path) {
        if (!checkAuth(request)) {
          return new Response('密码错误', { status: 401 });
        }
        await env.FILES.delete(path);
        return Response.json({ ok: true });
      }

      // GET /:filename —— 下载文件
      if (request.method === 'GET' && path) {
        const object = await env.FILES.get(path);
        if (!object) {
          return new Response('文件不存在', { status: 404 });
        }
        const headers = new Headers();
        object.writeHttpMetadata(headers);
        headers.set('etag', object.httpEtag);
        headers.set('Content-Disposition', `attachment; filename="${encodeURIComponent(path)}"`);
        return new Response(object.body, { headers });
      }

      return new Response('Not Found', { status: 404 });
    } catch (err) {
      return new Response(`Server Error: ${err.message}`, { status: 500 });
    }
  }
};
