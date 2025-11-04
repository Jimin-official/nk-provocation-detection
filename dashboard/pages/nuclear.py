import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import platform
from sqlalchemy import create_engine
from utils.regime_case import draw_regime_type_chart
from utils.icon import get_icon_name, case_color_map
from utils.all_case import make_summary_table
from utils.all_case import render_event_case
from utils.mapfunc import all_map_markers

plt.rcParams['axes.unicode_minus']=False 
if platform.system() == 'Windows':
    plt.rcParams['font.family']='Malgun Gothic' 
elif platform.system() == 'Darwin':
    # rc('font', family='AppleGothic')
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

# 전체 도발 데이터 중 '핵실험'만 필터링
provocation_df = pd.read_sql('SELECT * FROM provocation', con=engine)
nuclear_df = provocation_df[provocation_df['type'].str.contains('핵실험', na=False)].copy()
nuclear_count = len(nuclear_df)
nuclear_df['Type'] = 'Nuclear'

# 사건명을 통해 메인에서 넘어오는 것과 라디오 버튼 선택을 위한 설정
view_mapping = {
    'nuclear_case_1': '북한의 1차 핵실험',
    'nuclear_case_2': '북한의 2차 핵실험',
    'nuclear_case_3': '북한의 3차 핵실험',
    'nuclear_case_4': '북한의 4차 핵실험',
    'nuclear_case_5': '북한의 5차 핵실험',
    'nuclear_case_6': '북한의 6차 핵실험',
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
initial_view = st.session_state.get('subview', 'nuclear_case_1')
if initial_view not in valid_views:
    initial_view = 'nuclear_case_1'

# 사이드바 라디오 버튼으로 사건 선택
labels = list(view_mapping.values())
subview_label = st.sidebar.radio(
    "사건",
    labels,
    index=labels.index(view_mapping[initial_view])
)

# 사건별 날짜 기반 이름 매핑
nuclear_case_names = {
    '2006-10-09' : '1차 핵실험',
    '2009-05-25' : '2차 핵실험',
    '2013-02-12' : '3차 핵실험',
    '2016-01-06' : '4차 핵실험',
    '2016-09-09' : '5차 핵실험',
    '2017-09-03' : '6차 핵실험'
}

# 핵실험 사건 좌표 리스트 추출
selected_dates = list(nuclear_case_names.keys())
coords_nuclear = nuclear_df[['latitude', 'longitude', 'case_description']].dropna().values.tolist()

# 위도 경도 있는지 검사 함수
def is_valid_coord(val):
    try:
        float_val = float(val)
        return not pd.isnull(float_val)
    except (ValueError, TypeError):
        return False

# 페이지 시작
subview = reverse_mapping[subview_label]

st.title("📰 뉴스기사 크롤링을 통한 북한 도발 징후 포착")
st.header('핵실험 도발 징후 분석', divider=True)

# 아이콘 및 색상 설정
m_icon = get_icon_name('핵실험')
m_icon_color = case_color_map('핵실험')

# 사건별 상세 페이지 출력 (all_case.py의 render_event_case 함수 사용)
if subview == "nuclear_case_1":
    render_event_case(
        case_title="1. 1차 핵실험",
        date="2006년 10월 9일",
        content_lines=[
            "4.3 규모의 인공지진이 발생",
            "1kt 이하의 폭발위력",
            "플루토늄이 원료로 사용됨",
            "북한은 안보위협을 이유로 핵무기를 개발하였다는 것이 일반적인 분석이며, 외세에 의한 체제위협이 핵프로그램 개발의 원인이었음을 강조함",
            "1993년 3월 북한은 핵확산금지조약 탈퇴를 선언하며 북핵위기가 시작됨",
            "사회주의권 분열과 외교적 고립으로 인한 생존위협 인식이 핵개발 원인으로 풀이됨",
            "(통일정책연구, 북한 핵프로그램의 시작과 성장: 1950-1960년대를 중심으로)"
        ],
        coords=coords_nuclear[0],
        casenum=1,
        event_type='핵실험'
    )

elif subview == "nuclear_case_2":
    render_event_case(
        case_title="2. 2차 핵실험",
        date="2009년 5월 25일",
        content_lines=[
            "4.7규모의 인공지진 발생",
            "3kt ~ 4kt의 폭발위력을 보여줌",
            "플루토늄이 원료로 사용됨",
            "이명박 정부 출범 이후 북한은 대북정책과 한미동맹을 강하게 비난하며 핵 억제력 강화를 주장함",
            "유엔 안보리의 대북제재 결의안 1718호 복원 의장성명 발표 이후 더욱 격화됨",
            "2009년 4월 14일 북한은 의장성명을 비난하며 핵시설을 복구하고 2차 핵실험 감행",
            "(통일부 북한정보 포털)"
        ],
        coords=coords_nuclear[1],
        casenum=2,
        event_type='핵실험'
    )

elif subview == "nuclear_case_3":
    render_event_case(
        case_title="3. 3차 핵실험",
        date="2013년 2월 12일",
        content_lines=[
            "5.1 규모의 인공지진이 발생",
            "6kt ~ 7kt의 폭발위력을 보여줌",
            "고농축 우라늄이 원료로 사용됨",
            "김정일 유훈 관철: '핵, 장거리미사일, 생화학무기 발전' 강조",
            "군사적 위대성 과시와 핵능력 제고 필요성",
            "주민 자긍심 고양 및 대미 협상 수단으로서의 실험",
            "(통일연구원, 북한의 제3차 핵실험 위협 배경 분석, 전현준)"
        ],
        coords=coords_nuclear[2],
        casenum=3,
        event_type='핵실험'
    )

elif subview == "nuclear_case_4":
    render_event_case(
        case_title="4. 4차 핵실험",
        date="2016년 1월 6일",
        content_lines=[
            "5.1 규모의 인공지진 발생",
            "6kt의 폭발위력을 보여줌",
            "수소탄을 원료로 사용함",
            "3차 핵실험 이후 축적한 핵기술을 검증하기 위해 계획된 실험 가능성",
            "2016년 5월 제7차 당대회 앞두고 내부결속 및 정권 기반 강화 목적",
            "미국을 대상으로 한 핵 능력 과시 의도",
            "(정성윤, 북한 4차 핵실험의 의미와 파장, 통일연구원, 2016.1.11.)"
        ],
        coords=coords_nuclear[3],
        casenum=4,
        event_type='핵실험'
    )

elif subview == "nuclear_case_5":
    render_event_case(
        case_title="5. 5차 핵실험",
        date="2016년 9월 9일",
        content_lines=[
            "5.3 규모의 인공지진이 발생",
            "10kt의 폭발위력을 보여줌",
            "국제사회가 G20, 동아시아 정상회의를 통해 경고를 보냈음에도 ",
            "북한이 유엔 안보리 결의를 위반하며 2016년 두번째로 감행한 핵실험",
            "핵탄두 제조 기술력 확인 및 핵고도화 프로그램 진전 확인",
            "핵보유국 지위 확보 노선의 재천명",
            "국제사회의 제재에도 핵개발 의지를 꺾지 않겠다는 결기 표현",
            "(정성윤, 북한 5차 핵실험의 의미와 파장, 통일연구원, 2016.9.13.)"
        ],
        coords=coords_nuclear[4],
        casenum=5,
        event_type='핵실험'
    )

elif subview == "nuclear_case_6":
    render_event_case(
        case_title="6. 6차 핵실험",
        date="2017년 9월 3일",
        content_lines=[
            "6.3 규모의 인공지진이 발생",
            "140kt 이상의 폭발 위력을 보여줌",
            "수소탄 실험 성공 발표, 핵 고도화 완성 목표",
            "대미 강압 및 정세 주도권 강화 목적",
            "핵보유국 지위 인정 기대와 대북제재 무용론 확산 목적",
            "(정성윤, 북한의 6차 핵실험[1]: 평가와 정세전망, 통일연구원, 2017.09.11.)"
        ],
        coords=coords_nuclear[5],
        casenum=6,
        event_type='핵실험'
    )

st.header('전체 핵실험 사건')
st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)

# 핵실험 도발 사건 공통 설명
with st.container(): 
    acol1, acol2, acol3 = st.columns(3, gap='medium')

    with acol1:
        # 도발지점 지도 시각화 (mapfunc.py의 all_map_markers 함수 사용)
        st.subheader('🗺️ 도발지점')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        m = all_map_markers(nuclear_df, m_icon_color, center=(41.43375, 129.82025))
        st_folium(m, width=550, height=550)

    with acol2:
        # 정권별 도발 횟수 시각화 (regime_case.py의 draw_regime_type_chart 함수 사용)
        st.subheader('정권별 핵실험 도발 횟수')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        regime_choice = st.radio(
            "##### 정권별 핵실험 도발 횟수 보기",
            ('북한 정권 기준', '남한 정권 기준'),
            horizontal=True,
            key='nuclear_radio',
            label_visibility="collapsed"
        )
        draw_regime_type_chart(
            df=nuclear_df,
            regime_type='북한' if regime_choice == '북한 정권 기준' else '남한',
            attack_type='핵실험'
        )

    with acol3:
        # 사건 요약 테이블 출력 (all_case.py의 make_summary_table 함수 사용)
        st.subheader('핵실험 도발')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        content_lines = [
            "북한이 안보위협을 이유로 핵무기를 개발하였다는 것이 일반적인 분석",
            "북한은 외세에 의한 체제위협이 핵프로그램의 개발에 있어 결정적 원인임을 강조",
            "6번의 핵실험은 모두 풍계리 핵실험장에서 이루어짐 "
            "(풍계리는 산지로 둘러싸여 있고, 암반 대부분이 화강암이라 핵실험 장소로 좋은 지형 조건)"
        ]
        st.markdown(make_summary_table("핵실험 도발", nuclear_count, content_lines), unsafe_allow_html=True)

# 메인 페이지로 돌아가기 버튼
if st.button("🏠 메인 페이지로 돌아가기"):
    st.switch_page("main.py")