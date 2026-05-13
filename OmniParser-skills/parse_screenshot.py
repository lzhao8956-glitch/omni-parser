"""
OmniParser Skill - 截图解析
Usage: python parse_screenshot.py <图片路径>
"""
import sys
import os
import json
import base64
import requests

OMNIPARSER_URL = os.environ.get('OMNIPARSER_URL', 'http://localhost:5001')

def parse_screenshot(image_path):
    """上传截图到 OmniParser，返回解析结果"""
    if not os.path.exists(image_path):
        print(f'Error: File not found: {image_path}')
        return None
    
    with open(image_path, 'rb') as f:
        files = {'image': f}
        resp = requests.post(f'{OMNIPARSER_URL}/upload', files=files, timeout=60)
    
    if resp.status_code != 200:
        print(f'Error: HTTP {resp.status_code} - {resp.text}')
        return None
    
    return resp.json()

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python parse_screenshot.py <图片路径>')
        sys.exit(1)
    
    image_path = sys.argv[1]
    result = parse_screenshot(image_path)
    
    if result:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        sys.exit(1)