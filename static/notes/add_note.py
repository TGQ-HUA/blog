#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
TangNotes 快捷添加脚本
用法:
  python add_note.py memory "标题名" "笔记内容（支持 Markdown）"
  python add_note.py task  "标题名" "待办内容"
  python add_note.py task-done "条目ID"       # 标记任务完成

Hermes 用这个脚本给老唐添加便签，无需打开浏览器。
"""

import sys
import json
import urllib.request

BASE = 'http://localhost:8765'


def api_post(endpoint, data):
    url = f'{BASE}{endpoint}'
    body = json.dumps(data, ensure_ascii=False).encode('utf-8')
    req = urllib.request.Request(url, data=body,
        headers={'Content-Type': 'application/json'}, method='POST')
    resp = urllib.request.urlopen(req)
    return json.loads(resp.read())


def find_title_id(category, title_name):
    """根据标题名查找 ID"""
    resp = urllib.request.urlopen(f'{BASE}/api/data')
    data = json.loads(resp.read())
    for g in data.get(category, []):
        if g['title'] == title_name:
            return g['id']
    return None


def main():
    if len(sys.argv) < 2:
        print("用法: add_note.py <memory|task|task-done> [标题] [内容]")
        sys.exit(1)

    cmd = sys.argv[1]

    if cmd == 'memory':
        if len(sys.argv) < 4:
            print("用法: add_note.py memory \"标题名\" \"笔记内容\"")
            sys.exit(1)
        title, content = sys.argv[2], sys.argv[3]
        tid = find_title_id('memory', title)
        if not tid:
            # 标题不存在，先创建
            api_post('/api/memory/add_title', {'title': title})
            tid = find_title_id('memory', title)
        result = api_post('/api/memory/add_item', {'title_id': tid, 'content': content})
        print(f"✅ 记忆笔记已添加: {content[:40]}...")

    elif cmd == 'task':
        if len(sys.argv) < 4:
            print("用法: add_note.py task \"标题名\" \"待办内容\"")
            sys.exit(1)
        title, content = sys.argv[2], sys.argv[3]
        tid = find_title_id('task', title)
        if not tid:
            api_post('/api/task/add_title', {'title': title})
            tid = find_title_id('task', title)
        result = api_post('/api/task/add_item', {'title_id': tid, 'content': content})
        print(f"✅ 待办已添加: {content[:40]}...")

    elif cmd == 'task-done':
        if len(sys.argv) < 3:
            print("用法: add_note.py task-done \"条目ID\"")
            sys.exit(1)
        item_id = sys.argv[2]
        result = api_post('/api/task/toggle', {'item_id': item_id})
        status = '✅ 完成' if result.get('done') else '🔄 待办'
        print(f"{status}: {item_id}")

    else:
        print(f"未知命令: {cmd}")
        sys.exit(1)


if __name__ == '__main__':
    main()
