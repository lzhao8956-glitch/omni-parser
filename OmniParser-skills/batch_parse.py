"""
OmniParser Skill - 批量截图解析
Usage: python batch_parse.py <文件夹路径>
"""
import sys
import os
import json
import glob
import requests

OMNIPARSER_URL = os.environ.get('OMNIPARSER_URL', 'http://localhost:5001')

def parse_folder(folder_path):
    """批量处理文件夹中的所有图片"""
    if not os.path.isdir(folder_path):
        print(f'Error: Not a directory: {folder_path}')
        return
    
    extensions = ['*.png', '*.jpg', '*.jpeg', '*.PNG', '*.JPG', '*.JPEG']
    files = []
    for ext in extensions:
        files.extend(glob.glob(os.path.join(folder_path, ext)))
    
    if not files:
        print(f'No images found in {folder_path}')
        return
    
    print(f'Found {len(files)} images, processing...')
    
    results = []
    for i, filepath in enumerate(files, 1):
        print(f'[{i}/{len(files)}] Processing {os.path.basename(filepath)}...', end=' ')
        try:
            with open(filepath, 'rb') as f:
                resp = requests.post(f'{OMNIPARSER_URL}/upload', files={'image': f}, timeout=60)
            if resp.status_code == 200:
                result = resp.json()
                result['_source_file'] = os.path.basename(filepath)
                results.append(result)
                print('OK')
            else:
                print(f'HTTP {resp.status_code}')
        except Exception as e:
            print(f'Error: {e}')
    
    # 输出汇总
    output_file = os.path.join(folder_path, 'omni_parser_results.json')
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    print(f'\nResults saved to {output_file}')
    return results

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('Usage: python batch_parse.py <文件夹路径>')
        sys.exit(1)
    
    parse_folder(sys.argv[1])