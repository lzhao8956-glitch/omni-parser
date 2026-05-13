# OmniParser - AI驱动的Windows GUI智能自动化框架

[在线体验](http://172.26.183.121:5000) · [GitHub](https://github.com/lzhao8956-glitch/omni-parser) · [Star⭐](https://github.com/lzhao8956-glitch/omni-parser/stargazers)

---

## 🎯 OmniParser是什么

**让AI长出眼睛和手，能看懂截图、能操作任意Windows程序。**

上传任意软件的截图，AI自动识别所有可交互元素（按钮、输入框、菜单），返回带坐标的JSON描述。配合ADB或PyAutoGUI，可以实现**完全自主的GUI自动化**——不需要模板、不需要坐标硬编码。

```
截图 → AI解析UI → 结构化JSON → 自动化执行
```

---

## ✨ 核心能力

| 能力 | 说明 |
|------|------|
| 🔍 视觉元素识别 | 用Vision模型解析截图，识别所有GUI元素 |
| 📍 精准坐标定位 | 返回每个元素的bounding box中心坐标 |
| 📋 结构化输出 | JSON格式：{element_type, text, bounds, clickable} |
| 🖱️ 支持多种操控 | ADB（安卓模拟器）、PyAutoGUI（Windows桌面） |
| 🌐 Web界面 | 上传截图、预览解析结果、直观可视化 |

---

## 🆚 对比传统自动化

| 方案 | 优点 | 缺点 |
|------|------|------|
| 坐标点击 | 简单 | 分辨率/窗口变化即失效 |
| 图像识别(Sikuli) | 抗分辨率变化 | 精确匹配，UI变化要重新截图 |
| **OmniParser** | **AI理解语义，抗UI变化** | **依赖Vision模型** |

---

## 🚀 快速开始

### 本地运行

```bash
git clone https://github.com/lzhao8956-glitch/omni-parser.git
cd omni-parser
pip install -r requirements.txt

# 设置API Key（MiniMax Vision或其他Vision模型）
export MINIMAX_API_KEY="your-key"

python app.py
# 访问 http://localhost:5000
```

### Docker运行

```bash
docker build -t omniparser .
docker run -p 5000:5000 -e MINIMAX_API_KEY="your-key" omniparser
```

---

## 📁 项目结构

```
omni-parser/
├── app.py                  # Flask后端 + Vision解析逻辑
├── requirements.txt        # 依赖
├── templates/
│   └── index.html         # Web界面
├── static/
│   ├── uploads/           # 用户上传的截图
│   └── results/           # 解析结果缓存
├── OmniParser-skills/     # OmniParser官方技能包
├── SKILL.md              # Agent技能配置
└── README.md
```

---

## 💡 适用场景

- 🤖 **AI Agent具身自动化**：给Agent装上"眼睛"看屏幕、"手"操作程序
- 📱 **安卓模拟器控制**：小红书、知乎、抖音的自动发帖/养号
- 🖥️ **Windows桌面自动化**：自动填表、自动测试、RPA场景
- 🔬 **软件UI测试**：自动发现UI回归问题

---

## 🔧 API调用示例

```python
import requests

# 上传截图
with open("screenshot.png", "rb") as f:
    resp = requests.post("http://localhost:5000/api/parse", 
        files={"image": f})
    
result = resp.json()
# {
#   "elements": [
#     {"type": "button", "text": "确定", "bounds": [680, 840, 728, 881], "clickable": true},
#     {"type": "input", "text": "用户名", "bounds": [300, 200, 500, 250], "clickable": true},
#   ]
# }
```

---

## 🔗 相关项目

| 项目 | GitHub | 说明 |
|------|--------|------|
| [auto-coder](https://github.com/lzhao8956-glitch/auto-coder) | ⭐ 正在建设 | AI驱动，自动写完整项目代码 |
| [daniu-niuma-game](https://github.com/lzhao8956-glitch/daniu-niuma-game) | ⭐ 36+ | 大厂牛马模拟器，11种结局 |
| [binance-tg-bot](https://github.com/lzhao8956-glitch/binance-tg-bot) | ⭐ 建设中 | 币安TG机器人，合约信号 |

---

## 📊 状态

![Status](https://img.shields.io/badge/status-running-brightgreen)
![Python](https://img.shields.io/badge/python-3.12+-blue)
![License](https://img.shields.io/badge/license-MIT-green)

**正在运行**: http://172.26.183.121:5000


## 💰 Support This Project

USDT (TRC20): `TN3W4H6rK2ce4vX9YnFQHwKENnH5u6q9TW`
爱发电: https://afdian.net/@omni-parser

Star ⭐ this repo if it helps you!
