# OmniParser OpenClaw Skill

## 功能
截图上传 → AI解析 → 结构化JSON + 可视化覆盖层

## 核心API
- `POST /upload` - 上传截图，返回结构化JSON + visual_url
- `GET /results/<filename>` - 访问标注结果图片
- `GET /health` - 健康检查

## 服务地址
- 本地：`http://localhost:5001`
- 生产：待部署

## 使用方法

### 上传截图进行解析
```
python OmniParser-skills/parse_screenshot.py <图片路径>
```

### 批量处理
```
python OmniParser-skills/batch_parse.py <文件夹路径>
```

## 输入格式
- 图片文件：PNG/JPG/JPEG，最大16MB

## 输出格式
```json
{
  "elements": [
    {"type": "button", "label": "登录", "bbox": {"x": 75, "y": 1, "width": 10, "height": 5}, "confidence": 0.95},
    {"type": "input", "label": "搜索框", "bbox": {"x": 20, "y": 2, "width": 40, "height": 4}}
  ],
  "layout": {"type": "网页", "structure": ["header", "content_area", "footer"]},
  "image_url": "/uploads/xxx.png",
  "visual_url": "/results/result_xxx.png"
}
```

## 依赖
- requests
- Pillow

## 模型
- 使用 MiniMax Qwen VL Plus（已验证通过）
- USE_MOCK=False（真实模式）