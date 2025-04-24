from flask import Flask
import os

app = Flask(__name__)

@app.route('/')
def hello_world():
    # 나중에는 여기서 JSON 파일을 읽어서 보여주는 코드가 들어갑니다.
    return 'Hello, CatchupTrend! 앱이 성공적으로 배포되었습니다.'

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)