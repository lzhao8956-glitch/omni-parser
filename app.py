"""
OmniParser Web App - Main Entry Point
截图上传 → AI解析 → 结构化JSON + 可视化覆盖层
"""

import os
import uuid
import base64
import json
from datetime import datetime

from flask import Flask, request, jsonify, render_template, send_from_directory, send_file
import requests
from PIL import Image, ImageDraw, ImageFont

app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Ensure folders exist
os.makedirs('static/uploads', exist_ok=True)
os.makedirs('static/results', exist_ok=True)

# ── Parser Config ────────────────────────────────────────────────────
# 开发模式：USE_MOCK=True 时返回模拟数据，不调任何外部API
USE_MOCK = False  # 已切换真实模型

# MiniMax API Config (USE_MOCK=False时使用)
import os
MINIMAX_API_KEY = os.environ.get('MINIMAX_API_KEY', '')
if not MINIMAX_API_KEY:
    raise RuntimeError('MINIMAX_API_KEY environment variable not set')
MINIMAX_BASE_URL = os.environ.get('MINIMAX_BASE_URL', 'https://dashscope.aliyuncs.com/compatible-mode/v1')
MINIMAX_MODEL = 'qwen-vl-plus'

# ── Routes ─────────────────────────────────────────────────────

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload():
    """Handle screenshot upload and parsing."""
    if 'image' not in request.files:
        return jsonify({'error': 'No image provided'}), 400
    
    file = request.files['image']
    if file.filename == '':
        return jsonify({'error': 'No filename'}), 400
    
    # Save uploaded file
    ext = file.filename.rsplit('.', 1)[-1].lower()
    filename = f"{uuid.uuid4().hex}.{ext}"
    filepath = os.path.join('static/uploads', filename)
    file.save(filepath)
    
    # Parse with AI
    try:
        result = parse_screenshot(filepath)
        result['image_url'] = f'/uploads/{filename}'
        result['timestamp'] = datetime.now().isoformat()
        
        # 生成可视化标注图
        elements = result.get('elements', [])
        layout = result.get('layout', {})
        if elements:
            result['visual_url'] = draw_element_boxes(filepath, elements, layout)
        
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory('static/uploads', filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory('static/results', filename)

# ── Parser Logic ─────────────────────────────────────────────────

def parse_screenshot(image_path: str) -> dict:
    """
    Parse screenshot.
    USE_MOCK=True  → 返回模拟数据（开发阶段）
    USE_MOCK=False → 调用 MiniMax Vision 或 OmniParser API
    """
    if USE_MOCK:
        return mock_parse_result(image_path)
    else:
        return call_minimax_vision(image_path)

def mock_parse_result(image_path: str) -> dict:
    """开发阶段：返回模拟解析数据，不调任何外部API"""
    import random
    
    # 随机生成UI元素，模拟真实解析结果
    element_templates = [
        {"type": "header", "label": "导航栏", "bbox": {"x": 0, "y": 0, "width": 100, "height": 8}},
        {"type": "button", "label": "登录", "bbox": {"x": 75, "y": 1, "width": 10, "height": 5}},
        {"type": "button", "label": "注册", "bbox": {"x": 86, "y": 1, "width": 10, "height": 5}},
        {"type": "input", "label": "搜索框", "bbox": {"x": 20, "y": 2, "width": 40, "height": 4}},
        {"type": "image", "label": "轮播图", "bbox": {"x": 5, "y": 10, "width": 90, "height": 30}},
        {"type": "container", "label": "内容区域", "bbox": {"x": 5, "y": 42, "width": 60, "height": 50}},
        {"type": "button", "label": "了解更多", "bbox": {"x": 10, "y": 50, "width": 20, "height": 6}},
        {"type": "button", "label": "立即试用", "bbox": {"x": 35, "y": 50, "width": 20, "height": 6}},
        {"type": "sidebar", "label": "侧边栏", "bbox": {"x": 0, "y": 10, "width": 4, "height": 88}},
        {"type": "text", "label": "版权信息 © 2026", "bbox": {"x": 30, "y": 95, "width": 40, "height": 4}},
    ]
    
    return {
        "elements": element_templates,
        "layout": {
            "type": "网页",
            "structure": ["header", "content_area", "footer"],
            "confidence": 0.95
        },
        "dev_mode": True,
        "mock": True,
        "note": "开发模式模拟数据，发布前切换至真实AI解析API"
    }

def call_minimax_vision(image_path: str) -> dict:
    """开发期间：使用MiniMax视觉API解析截图"""
    with open(image_path, 'rb') as f:
        img_base64 = base64.b64encode(f.read()).decode('utf-8')
    
    prompt = (
        "You are an expert UI/UX analyst. Analyze this screenshot and identify:\n"
        "1. UI elements (buttons, inputs, images, text blocks)\n"
        "2. Layout structure (header, sidebar, content area, footer)\n"
        "3. Element positions (bounding box x, y, width, height as percentages)\n"
        "4. Element types and labels\n\n"
        "Return a JSON object with 'elements' array. Each element has:\n"
        "- type: button|input|image|text|container|header|footer|sidebar\n"
        "- label: readable text or description\n"
        "- bbox: {x: 0-100, y: 0-100, width: 0-100, height: 0-100} (percentages)\n"
        "- confidence: 0-1\n\n"
        "Also provide 'layout' with the overall page structure."
    )
    
    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{img_base64}"}},
                {"type": "text", "text": prompt}
            ]
        }
    ]
    
    payload = {
        "model": MINIMAX_MODEL,
        "messages": messages,
        "temperature": 0.3
    }
    
    headers = {
        "Authorization": f"Bearer {MINIMAX_API_KEY}",
        "Content-Type": "application/json"
    }
    
    resp = requests.post(f"{MINIMAX_BASE_URL}/chat/completions", 
                        headers=headers, json=payload, timeout=60)
    resp.raise_for_status()
    
    data = resp.json()
    content = data['choices'][0]['message']['content']
    
    # Parse JSON from response
    try:
        # Try to extract JSON block
        if '```json' in content:
            json_str = content.split('```json')[1].split('```')[0].strip()
        elif '```' in content:
            json_str = content.split('```')[1].split('```')[0].strip()
        else:
            json_str = content.strip()
        
        result = json.loads(json_str)
        result['raw_response'] = content[:500]
        return result
    except json.JSONDecodeError:
        return {
            'elements': [],
            'layout': {},
            'raw_response': content[:1000],
            'error': 'Failed to parse JSON from model response'
        }

def call_omniparser_api(image_path: str) -> dict:
    """产品阶段：调用OmniParser官方API"""
    with open(image_path, 'rb') as f:
        files = {'image': f}
        data = {'api_key': OMNIPARSER_API_KEY}
        resp = requests.post(
            f"{OMNIPARSER_API_URL}/parse",
            files=files,
            data=data,
            timeout=30
        )
    resp.raise_for_status()
    return resp.json()

def draw_element_boxes(image_path: str, elements: list, layout: dict) -> str:
    """在截图上画框标注元素，返回结果图片路径"""
    img = Image.open(image_path).convert('RGB')
    w, h = img.size
    draw = ImageDraw.Draw(img)
    
    # 颜色映射
    colors = {
        'button': '#FF6B6B',
        'input': '#4ECDC4',
        'image': '#45B7D1',
        'text': '#96CEB4',
        'container': '#FFEAA7',
        'header': '#DDA0DD',
        'footer': '#98D8C8',
        'sidebar': '#F7DC6F',
        'default': '#FF9F43'
    }
    
    # 画元素框
    for el in elements:
        bbox = el.get('bbox', {})
        x = bbox.get('x', 0) / 100 * w
        y = bbox.get('y', 0) / 100 * h
        ew = bbox.get('width', 0) / 100 * w
        eh = bbox.get('height', 0) / 100 * h
        color = colors.get(el.get('type', 'default'), colors['default'])
        
        # 画矩形框
        draw.rectangle([x, y, x+ew, y+eh], outline=color, width=3)
        # 画标签
        label = el.get('label', el.get('type', ''))
        draw.text((x+5, y+5), f"{el.get('type','')}: {label}", fill=color)
    
    # 保存结果
    result_filename = f"result_{uuid.uuid4().hex}.png"
    result_path = os.path.join('static/results', result_filename)
    img.save(result_path)
    return f'/results/{result_filename}'

@app.route('/visualize/<filename>')
def visualize(filename):
    """对已上传的图片进行可视化标注"""
    filepath = os.path.join('static/uploads', filename)
    if not os.path.exists(filepath):
        return jsonify({'error': 'File not found'}), 404
    
    # 从请求参数获取elements和layout
    elements = request.args.get('elements', '[]')
    layout = request.args.get('layout', '{}')
    try:
        elements = json.loads(elements)
        layout = json.loads(layout)
    except:
        elements = []
        layout = {}
    
    result_url = draw_element_boxes(filepath, elements, layout)
    return jsonify({'result_url': result_url})

@app.route('/health')
def health():
    return jsonify({
        'status': 'ok',
        'use_mock': USE_MOCK,
        'version': '0.1.0',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5001))
    app.run(host='0.0.0.0', port=port, debug=False)