@echo off
set MINIMAX_API_KEY=sk-5a3faad8dbab42018effcca630038ba9
set MINIMAX_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
set PORT=5001
cd /d E:\hermes-openclaw-shared\omni-parser
python -m waitress --host=0.0.0.0 --port=%PORT% app:app
