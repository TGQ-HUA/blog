#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TangNotes 便签程序 —— Python 后端
液态玻璃桌面便签的 HTTP 服务器
端口: 8765
"""

import http.server
import json
import os
import time
import uuid
import urllib.parse
import socketserver
import logging

PORT = 8765
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, 'data.json')
LOG_FILE = os.path.join(ROOT, 'server.log')

# 日志同时输出到控制台和文件
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler(LOG_FILE, encoding='utf-8'),
        logging.StreamHandler()
    ]
)
log = logging.getLogger(__name__)

# 允许端口快速复用
socketserver.TCPServer.allow_reuse_address = True


def load_data():
    """读取 data.json"""
    if not os.path.exists(DATA_FILE):
        return {"memory": [], "task": []}
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)


def save_data(data):
    """写入 data.json（原子写入：先写临时文件再替换）"""
    tmp = DATA_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_FILE)


def gen_id():
    """生成短 ID"""
    return uuid.uuid4().hex[:8]


class TangHandler(http.server.SimpleHTTPRequestHandler):
    """自定义请求处理器"""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, format, *args):
        """精简日志"""
        log.info(f"[{time.strftime('%H:%M:%S')}] {args[0]}")

    def do_GET(self):
        """处理 GET 请求"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == '/api/data':
            self._json_response(load_data())
            return

        # 默认：静态文件服务
        if path == '/' or path == '':
            path = '/app.html'
            self.path = path
        super().do_GET()

    def do_POST(self):
        """处理 POST 请求"""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        # 读取请求体
        length = int(self.headers.get('Content-Length', 0))
        raw_body = self.rfile.read(length) if length else b'{}'
        # 尝试 UTF-8，失败则用 GBK（兼容 Windows git-bash curl）
        try:
            body_str = raw_body.decode('utf-8')
        except UnicodeDecodeError:
            body_str = raw_body.decode('gbk')
        try:
            params = json.loads(body_str)
        except json.JSONDecodeError:
            params = {}

        data = load_data()

        # ── 记忆类：添加标题 ──
        if path == '/api/memory/add_title':
            title = params.get('title', '').strip()
            if not title:
                self._json_response({'error': '标题不能为空'}, 400)
                return
            data['memory'].append({
                'id': gen_id(),
                'title': title,
                'items': []
            })
            save_data(data)
            log.info(f"  📝 记忆标题: {title}")
            self._json_response({'ok': True})

        # ── 记忆类：添加内容 ──
        elif path == '/api/memory/add_item':
            title_id = params.get('title_id', '')
            content = params.get('content', '').strip()
            if not title_id or not content:
                self._json_response({'error': '参数不完整'}, 400)
                return
            for group in data['memory']:
                if group['id'] == title_id:
                    group['items'].append({
                        'id': gen_id(),
                        'content': content,
                        'created': time.strftime('%Y-%m-%d %H:%M')
                    })
                    save_data(data)
                    log.info(f"  📝 +记忆: {content[:30]}...")
                    self._json_response({'ok': True})
                    return
            self._json_response({'error': '标题不存在'}, 404)

        # ── 任务类：添加标题 ──
        elif path == '/api/task/add_title':
            title = params.get('title', '').strip()
            if not title:
                self._json_response({'error': '标题不能为空'}, 400)
                return
            data['task'].append({
                'id': gen_id(),
                'title': title,
                'items': []
            })
            save_data(data)
            log.info(f"  ✅ 任务标题: {title}")
            self._json_response({'ok': True})

        # ── 任务类：添加待办 ──
        elif path == '/api/task/add_item':
            title_id = params.get('title_id', '')
            content = params.get('content', '').strip()
            if not title_id or not content:
                self._json_response({'error': '参数不完整'}, 400)
                return
            for group in data['task']:
                if group['id'] == title_id:
                    group['items'].append({
                        'id': gen_id(),
                        'content': content,
                        'created': time.strftime('%Y-%m-%d'),
                        'done': None
                    })
                    save_data(data)
                    log.info(f"  ✅ +任务: {content[:30]}...")
                    self._json_response({'ok': True})
                    return
            self._json_response({'error': '标题不存在'}, 404)

        # ── 任务类：标记完成/取消完成 ──
        elif path == '/api/task/toggle':
            item_id = params.get('item_id', '')
            if not item_id:
                self._json_response({'error': '缺少 item_id'}, 400)
                return
            for group in data['task']:
                for item in group['items']:
                    if item['id'] == item_id:
                        if item.get('done'):
                            item['done'] = None  # 取消完成
                        else:
                            item['done'] = time.strftime('%Y-%m-%d %H:%M')  # 标记完成
                        save_data(data)
                        status = '✅ 完成' if item['done'] else '🔄 待办'
                        log.info(f"  {status}: {item['content'][:30]}...")
                        self._json_response({'ok': True, 'done': item['done']})
                        return
            self._json_response({'error': '条目不存在'}, 404)

        else:
            self._json_response({'error': '未知 API'}, 404)

    def _json_response(self, data, code=200):
        """发送 JSON 响应"""
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self):
        """CORS 预检"""
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()


if __name__ == '__main__':
    os.chdir(ROOT)
    try:
        log.info(f"""
╔══════════════════════════════════════╗
║       TangNotes 便签服务已启动       ║
║   记忆类: http://localhost:{PORT}/memory.html  ║
║   任务类: http://localhost:{PORT}/task.html    ║
║   按 Ctrl+C 停止服务                ║
╚══════════════════════════════════════╝
""")
        server = http.server.HTTPServer(('127.0.0.1', PORT), TangHandler)
        server.serve_forever()
    except KeyboardInterrupt:
        log.info("\n👋 服务已停止")
        server.server_close()
    except Exception as e:
        log.error(f"服务启动失败: {e}", exc_info=True)
        import traceback
        traceback.print_exc()
