import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import platform
from sqlalchemy import create_engine
from utils.all_case import render_event_case
from utils.all_case import make_summary_table
from utils.regime_case import draw_regime_type_chart
from utils.icon import get_icon_name, case_color_map
from utils.mapfunc import all_map_markers

plt.rcParams['axes.unicode_minus']=False
if platform.system() == 'Windows':
    plt.rcParams['font.family']='Malgun Gothic' 
elif platform.system() == 'Darwin':
    plt.rcParams['font.family']='AppleGothic'
else:
    print('Unknown system...')

# 페이지 넓게
st.set_page_config(layout='wide')

# MySQL 연결 설정
username = 'first'
password = '1emddlwh'
db_name = 'att_db'
host = 'localhost' 
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}")

# 전체 도발 데이터 불러오기
provocation_df = pd.read_sql('SELECT * FROM provocation', con=engine)

# 오물풍선 도발만 필터링
balloon_df = provocation_df[provocation_df['type'].str.contains('오물풍선', na=False)].copy()
balloon_count = len(balloon_df)
balloon_df['Type'] = 'balloon'

# 사건명을 통해 메인에서 넘어오는 것과 라디오 버튼 선택을 위한 설정
view_mapping = {
    'balloon_case_1': '오물 풍선'
}
reverse_mapping = {v: k for k, v in view_mapping.items()}

# 지도에서 선택된 사건이 있으면 해당 서브뷰로 이동
selected_case = st.session_state.get('selected_case', None)
if selected_case and selected_case in reverse_mapping:
    expected_subview = reverse_mapping[selected_case]
    if st.session_state.get('subview') != expected_subview:
        st.session_state['subview'] = expected_subview
        st.rerun()

# 서브뷰 초기값 설정
valid_views = list(view_mapping.keys())
initial_view = st.session_state.get('subview', 'balloon_case_1')
if initial_view not in valid_views:
    initial_view = 'balloon_case_1'

# 사이드바 라디오 버튼으로 사건 선택
labels = list(view_mapping.values())
subview_label = st.sidebar.radio(
    "사건",
    labels,
    index=labels.index(view_mapping[initial_view])
)

# 위도, 경도 정보 추출
coords_balloon = balloon_df[['latitude', 'longitude']].dropna().values.tolist()

# 경도 위도 유효성 검사
def is_valid_coord(val):
    try:
        float_val = float(val)
        return not pd.isnull(float_val)
    except (ValueError, TypeError):
        return False

# 페이지 시작
subview = reverse_mapping[subview_label]
st.title("📰 뉴스기사 크롤링을 통한 북한 도발 징후 포착")
st.header('오물풍선 도발 징후 분석', divider=True)

# 아이콘 설정
m_icon = get_icon_name('오물풍선')
m_icon_color = case_color_map('오물풍선')

# 오물풍선 도발 상세 페이지 출력 (all_case.py의 render_event_case)사용
if subview == "balloon_case_1":
    render_event_case(
        case_title='오물풍선 살포 도발',
        date='2024년 5월 28일',
        content_lines=[
            "2024년 5월 28일, 북한은 남측의 대북 전단 살포에 맞대응하겠다며 오물풍선을 날려보냄",
            "대형 풍선에 묶인 비닐봉투에는 담배꽁초, 폐천 조각, 비료 등 각종 오물과 쓰레기가 포함됨",
            "오물풍선으로 인해 수도권에서만 약 1억 원 상당의 재산 피해가 발생함",
            "북한은 이 조치가 자유북한운동연합 등 탈북민 단체의 전단 살포에 대한 대응임을 명확히 하였음",
            "6월 2일에는 '잠정 중단'을 선언하며 전단 살포 중단 시 오물풍선도 멈출 것이라는 입장을 재확인함",
            "(이은기, 오늘도 또 왔네··· ‘오물 풍선’ 제대로 알기, 시사in, 2024.10.23.)"
        ],
        coords=[37.5665, 126.9780],
        casenum=14,
        event_type='오물풍선'
    )

st.header('전체 오물풍선 사건')
st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)

# 오물풍선 도발 사건 유형 공통 설명
with st.container():
    acol1, acol2, acol3 = st.columns(3, gap='medium')

    with acol1:
        # 도발지점 지도 표시 (mapfunc.py의 all_map_markers사용)
        st.subheader('🗺️ 도발지점')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        m = all_map_markers(balloon_df, m_icon_color)
        st_folium(m, width=550, height=550)

    with acol2:
        # 정권별 도발 횟수 차트 (regime_case의 draw_regime_type_chart함수 사용)
        st.subheader('정권별 오물풍선 도발 횟수')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        regime_choice = st.radio(
            "정권별 오물풍선 도발 횟수 보기",
            ('북한 정권 기준', '남한 정권 기준'),
            horizontal=True,
            key='balloon_radio',
            label_visibility="collapsed"
        )
        draw_regime_type_chart(
            df=balloon_df,
            regime_type='북한' if regime_choice == '북한 정권 기준' else '남한',
            attack_type='오물풍선'
        )

    with acol3:
        # 도발 설명 요약 표 (all_case의 make_summary_table함수 사용)
        st.subheader('오물풍선 도발')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        content_lines = [
            "2024년 5월 28일부터 7월 24일까지 수천 개의 오물풍선을 여러 차례에 걸쳐 살포함",
            "북한은 대북 전단을 보내는 남한 단체에 대응하기 위한 조치라 주장함",
            "풍선에는 담배꽁초, 폐종이, 헝겊, 인분 등 각종 오물과 쓰레기가 담겨 있었음",
            "내용물에는 꿰맨 양말과 헝겊 장갑 등 북한 주민의 열악한 생활이 드러남",
            "북한은 자신의 행위를 '표현의 자유'라고 주장하며 한국 정부를 조롱함",
            "우리 정부는 대북확성기 방송으로 대응했고, 탈북민 단체는 활동 지속 의사를 밝힘",
            "김정은 정권은 청년들의 사상 변질을 가장 큰 위협으로 인식하고 있음",
            "외부 콘텐츠 유입 차단을 위해 반동사상문화배격법 등 내부 통제를 강화함",
            "출처: 중앙일보, 국민일보, 통일뉴스, 통일부 자료 및 김정은 시정연설 발췌 정리"
        ]
        st.markdown(make_summary_table("오물풍선 도발", balloon_count, content_lines), unsafe_allow_html=True)

# 메인 페이지로 돌아가기 버튼
if st.button("🏠 메인 페이지로 돌아가기"):
    st.switch_page("main.py")
