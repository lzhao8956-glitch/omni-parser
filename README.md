# OmniParser - 视觉GUI自动化框架

> 上传截图 → AI解析UI元素 → 返回结构化JSON + 可视化标注

[Live Demo](http://172.26.183.121:5001) · [GitHub](https://github.com/lzhao8956-glitch/omni-parser) · [Sponsor](https://afdian.com/omni-parser)

## 核心功能

- **截图解析**: 上传任意App/网页截图，AI识别所有UI元素（按钮、输入框、图片、文本等）
- **结构化JSON**: 返回每个元素的类型、标签、坐标（百分比bbox）
- **可视化标注**: 在截图上画框标注，一目了然
- **GUI自动化**: 解析结果可对接自动化脚本，自动点击/输入

## 工作原理

1. 上传截图
2. MiniMax Vision AI 分析画面
3. 返回结构化JSON + 可视化标注图

## 快速开始

### Web界面

访问 http://172.26.183.121:5001 或自己部署：

```bash
pip install -r requirements.txt
python app.py
```

### API调用

```bash
curl -X POST http://localhost:5001/upload \
  -F "image=@screenshot.png"
```

返回：

```json
{
  "elements": [
    {"type": "button", "label": "登录", "bbox": {"x": 75, "y": 1, "width": 10, "height": 5}},
    {"type": "input", "label": "搜索框", "bbox": {"x": 20, "y": 2, "width": 40, "height": 4}}
  ],
  "layout": {"type": "网页", "structure": ["header", "content_area", "footer"]}
}
```

## 技术栈

- **Flask** - 轻量级Web框架
- **MiniMax Vision** - qwen-vl-plus 视觉理解
- **Pillow** - 图片处理和可视化标注

## 应用场景

- 国产App自动化（微信、淘宝、拼多多）
- 网页元素定位
- UI测试辅助
- 无障碍辅助

## License

MIT
