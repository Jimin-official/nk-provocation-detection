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

plt.rcParams['axes.unicode_minus'] = False
if platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Malgun Gothic' 
elif platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'AppleGothic'
else:
    print('Unknown system...')

# 페이지 넓게 설정
st.set_page_config(layout='wide')

# MySQL 연결 설정
username = 'first'
password = '1emddlwh'
db_name = 'att_db'
host = 'localhost'
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}")

# 전체 도발 데이터 불러오기
provocation_df = pd.read_sql('SELECT * FROM provocation', con=engine)

# 미사일 도발만 필터링
missile_df = provocation_df[provocation_df['type'].str.contains('미사일', na=False)].copy()
missile_count = len(missile_df)
missile_df['Type'] = 'Missile'

# 사건명을 통해 메인에서 넘어오는 것과 라디오 버튼 선택을 위한 설정
view_mapping = {
    'missile_case_1': '동해안 단거리 미사일',
    'missile_case_2': '신형 단거리 탄도 미사일',
    'missile_case_3': 'NLL 이남 대륙간 탄도 미사일'
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
initial_view = st.session_state.get('subview', 'missile_case_1')
if initial_view not in valid_views:
    initial_view = 'missile_case_1'

# 사이드바 라디오 버튼으로 사건 선택
labels = list(view_mapping.values())
subview_label = st.sidebar.radio(
    "사건",
    labels,
    index=labels.index(view_mapping[initial_view])
)

# 날짜로 필터링하여 위도, 경도 추출
missile_case_names = {
    '2014-03-26': '동해안 단거리 미사일 발사',
    '2019-05-09': '신형 단거리 탄도 미사일',
    '2022-11-02': 'NLL 이남 대륙간 탄도 미사일'
}
selected_dates = list(missile_case_names.keys())
filtered_df = (
    missile_df[missile_df['date'].astype(str).isin(selected_dates)]
    .drop_duplicates(subset=['date'])
)
coords_missile = filtered_df[['latitude', 'longitude', 'date']].dropna().values.tolist()

# 경도 위도 있는지 검사 함수
def is_valid_coord(val):
    try:
        float_val = float(val)
        return not pd.isnull(float_val)
    except (ValueError, TypeError):
        return False

# 페이지 시작
subview = reverse_mapping[subview_label]

# 제목 출력
st.title("📰 뉴스기사 크롤링을 통한 북한 도발 징후 포착")
st.header('미사일 도발 징후 분석', divider=True)

# 아이콘 설정
m_icon = get_icon_name('미사일')
m_icon_color = case_color_map('미사일')

# 각 사건별 상세 페이지 출력 (all_case.py의 render_event_case 사용)
if subview == "missile_case_1":
    render_event_case(
        case_title='1. 동해안 단거리 미사일',
        date='2014년 3월 28일',
        content_lines=[
            "2014년 한미연합훈련 '키 리졸브'와 '독수리'에 대한 반발로 미사일을 발사함",
            "해당 미사일은 scud 계열의 단거리 탄도미사일로 추정됨"
        ],
        coords=coords_missile[0],
        casenum=1,
        event_type='미사일'
    )

elif subview == "missile_case_2":
    render_event_case(
        case_title='2. 신형 단거리 탄도 미사일',
        date='2019년 5월 9일',
        content_lines=[
            "오후 4시 29분과 4시 49분경 평안북도 구성 지역에서 불상의 발사체를 각각 동쪽으로 발사함",
            "군 당국은 이를 지난 2017년 화성-15형 이후 1년 5개월 만에 발사된 미사일로 규정함",
            "코로나19로 국제사회 관심이 분산된 틈을 타 체제 건재함을 과시하려는 의도가 있음",
            "미국 및 한국 정부를 대상으로 한 외교적·군사적 압박 목적도 내포됨",
            "정밀도와 신뢰성 향상을 위해 반복 실험을 수행한 것으로 분석됨",
            "통상적인 군사훈련의 일환으로 무기 성능 실험을 진행한 것으로 보임",
            "(김보미, 북한 단거리 미사일 시험발사의 배경과 함의, INSS 전략보고, 2020.09.)"
        ],
        coords=coords_missile[1],
        casenum=2,
        event_type='미사일'
    )

elif subview == "missile_case_3":
    render_event_case(
        case_title='3. NLL 이남 대륙간 탄도 미사일',
        date='2022년 11월 2일',
        content_lines=[
            "북한은 오전 8시 51분 강원도 원산 일대에서 SRBM 3발을 동해상으로 발사함",
            "그 중 한 발은 분단 이후 처음으로 동해 NLL 이남 공해상에 낙하하여 실질적 영토 침해로 간주됨",
            "해당 도발은 한미 연합공중훈련 '비질런트 스톰'에 대한 강력한 반발로 분석됨",
            "훈련에는 미국의 최신 스텔스기 F-35B가 참가하고 있었으며, 이에 대한 대응성 도발임",
            "(BBC뉴스 코리아, 북한, 한국 겨냥 탄도미사일 발사… '변화 바라지 말라'는 시그널, 2022.11.02.)"
        ],
        coords=coords_missile[2],
        casenum=3,
        event_type='미사일'
    )

st.header('전체 미사일 사건')
st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)

# 미사일 도발 공통 설명
with st.container():
    acol1, acol2, acol3 = st.columns(3, gap='medium')

    with acol1:
        # 도발지점 지도 표시 (mapfunc의 all_map_markers 함수 사용)
        st.subheader('🗺️ 도발지점')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        m = all_map_markers(missile_df, m_icon_color, center=(39.9642135, 127.0016985))
        st_folium(m, width=550, height=550)

    with acol2:
        # 정권별 도발 횟수 차트 (regime_case의 draw_regime_type_chart 함수 사용)
        st.subheader('정권별 미사일 도발 횟수')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        regime_choice = st.radio(
            "##### 정권별 미사일 도발 횟수 보기",
            ('북한 정권 기준', '남한 정권 기준'),
            horizontal=True,
            key='missile_radio',
            label_visibility="collapsed"
        )
        draw_regime_type_chart(
            df=missile_df,
            regime_type='북한' if regime_choice == '북한 정권 기준' else '남한',
            attack_type='미사일'
        )

    with acol3:
        # 도발 개요 설명 요약 (all_case의 make_summary_table 함수 사용)
        st.subheader('미사일 도발')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        content_lines = [
            "대량살상 무기인 ICBM 발사, 다종다양의 잠수함 발사탄도미사일(SLBM), "
            "극초음속 미사일, 초대형 방사포 등을 통한 위협을 의미",
            "공식적인 북한의 첫 미사일 도발은 1984년 4월 9일(전두환 정권)으로 기록됨",
            "현재까지 미사일 도발이 가장 많았던 해는 2022년 임"
        ]
        st.markdown(make_summary_table("미사일 도발", missile_count, content_lines), unsafe_allow_html=True)

# 메인 페이지로 돌아가기 버튼
if st.button("🏠 메인 페이지로 돌아가기"):
    st.switch_page("main.py")
