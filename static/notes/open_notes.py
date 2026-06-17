#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TangNotes 启动器 —— 打开两个无边框窗口 + API 后端
"""

import os
import sys
import time
import socket
import subprocess
import threading
import http.server
import json
import uuid
import socketserver

PORT_API = 8765
PORT_HUGO = 1313
ROOT = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(ROOT, 'data.json')
HUGO_EXE = r'C:\tools\hugo\hugo.exe'
BLOG_DIR = r'G:\blog'

socketserver.TCPServer.allow_reuse_address = True


# ═══════════════════════════════════════
# 数据操作
# ═══════════════════════════════════════

def load_data():
    with open(DATA_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_data(data):
    tmp = DATA_FILE + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    os.replace(tmp, DATA_FILE)


class APIHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=ROOT, **kwargs)

    def log_message(self, format, *args):
        pass

    def do_POST(self):
        from urllib.parse import urlparse
        path = urlparse(self.path).path
        length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(length) if length else b'{}'
        try:
            params = json.loads(body.decode('utf-8'))
        except:
            params = {}

        data = load_data()

        # ── 记忆：加标题 ──
        if path == '/api/memory/add_title':
            title = params.get('title', '').strip()
            if title:
                data['memory'].append({'id': uuid.uuid4().hex[:8], 'title': title, 'items': []})
                save_data(data)
            self._ok()

        # ── 记忆：加内容 ──
        elif path == '/api/memory/add_item':
            tid, content = params.get('title_id', ''), params.get('content', '').strip()
            if tid and content:
                for g in data['memory']:
                    if g['id'] == tid:
                        g['items'].append({
                            'id': uuid.uuid4().hex[:8],
                            'content': content,
                            'created': time.strftime('%Y-%m-%d %H:%M')
                        })
                        save_data(data)
                        break
            self._ok()

        # ── 任务：加标题 ──
        elif path == '/api/task/add_title':
            title = params.get('title', '').strip()
            if title:
                data['task'].append({'id': uuid.uuid4().hex[:8], 'title': title, 'items': []})
                save_data(data)
            self._ok()

        # ── 任务：加待办 ──
        elif path == '/api/task/add_item':
            tid, content = params.get('title_id', ''), params.get('content', '').strip()
            if tid and content:
                for g in data['task']:
                    if g['id'] == tid:
                        g['items'].append({
                            'id': uuid.uuid4().hex[:8],
                            'content': content,
                            'created': time.strftime('%Y-%m-%d'),
                            'done': None
                        })
                        save_data(data)
                        break
            self._ok()

        # ── 任务：标记完成 ──
        elif path == '/api/task/toggle':
            item_id = params.get('item_id', '')
            for g in data['task']:
                for item in g['items']:
                    if item['id'] == item_id:
                        item['done'] = None if item.get('done') else time.strftime('%Y-%m-%d %H:%M')
                        save_data(data)
                        self._json({'ok': True, 'done': item['done']})
                        return
            self._ok()

        else:
            self._ok()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def _ok(self):
        self._json({'ok': True})

    def _json(self, data, code=200):
        body = json.dumps(data, ensure_ascii=False).encode('utf-8')
        self.send_response(code)
        self.send_header('Content-Type', 'application/json; charset=utf-8')
        self.send_header('Content-Length', len(body))
        self.end_headers()
        self.wfile.write(body)


# ═══════════════════════════════════════
# 启动流程
# ═══════════════════════════════════════

def find_browser():
    for p in [
        r'C:\Program Files\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Google\Chrome\Application\chrome.exe',
        r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe',
        r'C:\Program Files\Microsoft\Edge\Application\msedge.exe',
    ]:
        if os.path.exists(p):
            return p
    return None


def is_port_open(port):
    try:
        s = socket.create_connection(('127.0.0.1', port), timeout=1)
        s.close()
        return True
    except:
        return False


def main():
    print("TangNotes 便签启动中...\n")

    # 1. Hugo
    if not is_port_open(PORT_HUGO):
        print("[1/3] 启动 Hugo 博客服务...")
        subprocess.Popen(
            [HUGO_EXE, 'server', '--noHTTPCache', '--bind', '127.0.0.1', '--port', str(PORT_HUGO)],
            cwd=BLOG_DIR,
            creationflags=subprocess.DETACHED_PROCESS | subprocess.CREATE_NO_WINDOW
        )
        for _ in range(15):
            time.sleep(1)
            if is_port_open(PORT_HUGO):
                break
    else:
        print("[1/3] Hugo 已在运行")

    # 2. API 后端
    if not is_port_open(PORT_API):
        print("[2/3] 启动 API 后端...")
        api_thread = threading.Thread(target=lambda: http.server.HTTPServer(('127.0.0.1', PORT_API), APIHandler).serve_forever(), daemon=True)
        api_thread.start()
        time.sleep(1)
    else:
        print("[2/3] API 后端已在运行")

    # 3. 打开窗口
    print("[3/3] 打开便签窗口...")
    browser = find_browser()
    urls = [
        f'http://localhost:{PORT_HUGO}/notes/memory.html',
        f'http://localhost:{PORT_HUGO}/notes/task.html',
    ]
    for url in urls:
        if browser:
            subprocess.Popen([browser, f'--app={url}'], creationflags=subprocess.DETACHED_PROCESS)
        else:
            import webbrowser
            webbrowser.open(url)
        time.sleep(0.5)

    print("\n✅ 完成！两个便签窗口已打开")
    print("   可以直接在窗口里添加笔记、标记任务")
    print("   关闭此窗口将停止 API 后端（便签变为只读）\n")
    input("   按回车停止服务...")


if __name__ == '__main__':
    main()
