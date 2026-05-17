import os
os.environ['MINIMAX_API_KEY'] = 'sk-5a3faad8dbab42018effcca630038ba9'
os.environ['MINIMAX_BASE_URL'] = 'https://dashscope.aliyuncs.com/compatible-mode/v1'
os.environ['PORT'] = '5001'

from waitress import serve
import app
serve(app.app, host='0.0.0.0', port=5001)
