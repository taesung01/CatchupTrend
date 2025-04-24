from flask import Flask, render_template
import os
import json
import glob # 파일 경로 패턴으로 파일을 찾는 데 사용

# Flask 앱 초기화
app = Flask(__name__)

# 데이터 파일이 저장된 폴더 경로 설정 (app.py 기준 상대 경로)
DATA_FOLDER = 'data'

def find_latest_report(pattern):
    """주어진 패턴과 일치하는 가장 최신 파일을 찾습니다."""
    try:
        # data 폴더 내에서 패턴 검색
        full_pattern = os.path.join(DATA_FOLDER, pattern)
        files = glob.glob(full_pattern) # 패턴과 일치하는 모든 파일 경로 리스트 반환

        if not files:
            print(f"경고: 패턴 '{pattern}'과 일치하는 파일을 찾을 수 없습니다.")
            return None

        # 파일 이름 기준으로 정렬 (가장 최신 파일이 앞에 오도록 내림차순)
        # 파일명에 날짜/주차 정보가 YYYY-MM-DD 또는 월_주차 형식으로 일관되게 들어있다고 가정
        files.sort(reverse=True)
        print(f"패턴 '{pattern}' 검색 결과 (최신순): {files}")
        return files[0] # 가장 첫 번째 파일 (최신) 반환

    except Exception as e:
        print(f"오류: '{pattern}' 패턴 파일 검색 중 오류 발생 - {e}")
        return None

def load_json_file(filepath):
    """주어진 경로의 JSON 파일을 읽어서 파이썬 객체로 반환합니다."""
    if filepath is None:
        return None # 파일 경로가 없으면 None 반환

    if not os.path.exists(filepath):
         print(f"오류: 파일이 존재하지 않습니다 - {filepath}")
         return None

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            data = json.load(f)
            print(f"성공: JSON 파일 로드 완료 - {filepath}")
            return data
    except json.JSONDecodeError:
        print(f"오류: JSON 형식 오류 - {filepath}")
        return None
    except Exception as e:
        print(f"오류: 파일 로드 중 오류 발생 - {filepath}, {e}")
        return None

@app.route('/') # 웹사이트의 루트 URL ('/')에 접속했을 때 실행될 함수
def dashboard():
    """대시보드 페이지를 렌더링합니다."""
    print("대시보드 요청 접수됨.")

    # data 폴더에서 최신 뉴스 리포트와 SNS 리포트 파일 경로 찾기
    latest_news_file = find_latest_report('trend_report_*.json')
    latest_sns_file = find_latest_report('sns_report_*.json')

    # 찾은 경로의 JSON 파일 내용 읽기
    news_data = load_json_file(latest_news_file)
    sns_data = load_json_file(latest_sns_file)

    # HTML 템플릿('index.html')을 렌더링하면서 읽어온 데이터 전달
    return render_template('index.html',
                           news_data=news_data,       # 뉴스 데이터 전달
                           sns_data=sns_data,         # SNS 데이터 전달
                           # 파일 이름도 전달하여 화면에 표시
                           news_filename=os.path.basename(latest_news_file) if latest_news_file else "파일 없음",
                           sns_filename=os.path.basename(latest_sns_file) if latest_sns_file else "파일 없음")

# 앱 실행 (Render 환경에서는 gunicorn이 이 부분을 관리하지만 로컬 테스트용으로 유지)
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # 로컬에서 개발/테스트 시에는 debug=True 사용 가능
    # app.run(host='0.0.0.0', port=port, debug=True)
    # Render 배포 시에는 debug=False 또는 생략
    app.run(host='0.0.0.0', port=port)
