# North Korea Provocation Dashboard
이 폴더는 북한 도발 데이터 기반 Streamlit 대시보드 실행 환경을 포함합니다.

## 1. 환경설정
```bash
# 가상환경 생성 (선택)
python -m venv venv
source venv/bin/activate   # Mac / Linux
venv\Scripts\activate      # Windows

# 패키지 설치
pip install -r requirements.txt
```

## 2. MySQL 데이터베이스 연결
```python
# main.py 내부 DB 연결 설정
username = 'first'
password = '1emddlwh'
db_name = 'att_db'
host = 'localhost'

engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}")
provocation_df = pd.read_sql('SELECT * FROM provocation', con=engine)
```
* DB 초기 세팅은 `../docs/mysql_setup.md` 파일을 참고하세요.

## 3. 실행방법
```bash
# Streamlit 서버 실행
python -m streamlit run main.py
```
- 브라우저 자동 실행: http://localhost:8501
- 메인 화면: 지도 + 정권별 도발 차트
- 페이지 이동: 왼쪽 사이드바에서 사건별 상세 페이지 선택 가능

## 4. 폴더 구조
dashboard/
├─ main.py                 # 메인 페이지
├─ pages/                  # 서브 페이지 (사건별 상세 분석)
├─ utils/                  # 공통 함수 (지도, 차트, 워드클라우드 등)
├─ images/                 # 시각화 결과 이미지
├─ requirements.txt        # 패키지 목록
└─ README.md               # 대시보드 실행 가이드
