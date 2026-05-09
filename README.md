# OmniParser - 截图智能解析工具

## 项目介绍
用户上传截图 → AI解析UI元素 → 返回结构化JSON + 可视化覆盖层

## 技术栈
- **后端**: Flask + Python
- **前端**: 纯HTML/JS（无框架）
- **AI解析**: 开发阶段用 MiniMax-M2.7 Vision API
- **生产切换**: OmniParser官方API（当云服务可用时）

## 快速启动

### 开发阶段
```bash
cd omni-parser
pip install -r requirements.txt
python app.py
```
访问 http://localhost:5000

### 生产阶段
```bash
# 设置OmniParser API
export OMNIPARSER_API_URL=https://your-omniparser-api.com
export OMNIPARSER_API_KEY=your_api_key

# 使用gunicorn运行
gunicorn app:app -b 0.0.0.0:5000 -w 4
```

## 目录结构
```
omni-parser/
├── app.py              # Flask主程序
├── requirements.txt     # 依赖
├── templates/
│   └── index.html      # 前端页面
└── static/
    ├── uploads/        # 上传图片
    └── results/        # 解析结果
```

## 开发进度
- [x] 项目架构搭建
- [x] 前端UI（截图上传+预览+可视化）
- [x] 后端API（Flask + MiniMax Vision）
- [ ] 解析结果可视化覆盖层
- [ ] 部署到Railway/Vercel
- [ ] 爱发电变现页面

## 目标
10天内完成MVP并上线爱发电开始变现