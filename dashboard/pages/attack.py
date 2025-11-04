import pandas as pd
import streamlit as st
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
import platform
from sqlalchemy import create_engine
from utils.all_case import render_event_case, make_summary_table
from utils.regime_case import draw_regime_type_chart
from utils.icon import get_icon_name, case_color_map
from utils.mapfunc import all_map_markers

plt.rcParams['axes.unicode_minus']=False 
if platform.system() == 'Windows':
    #윈도우즈 인 경우
    # rc('font', family='Malgun Gothic')
    plt.rcParams['font.family']='Malgun Gothic' 
elif platform.system() == 'Darwin':
    # rc('font', family='AppleGothic')
    plt.rcParams['font.family']='AppleGothic'
else:
    print('Unknown system...')

# 페이지 넓게
st.set_page_config(layout='wide')

# MySQL 데이터 불러오기
username = 'first'
password = '1emddlwh'
db_name = 'att_db'
host = 'localhost'
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}")

# attack 필터링
provocation_df = pd.read_sql('SELECT * FROM provocation', con=engine)
attack_df = provocation_df[provocation_df['type'].str.contains('피습|연평|천안함|목함지뢰|공격|교전|침투', na=False)].copy()
filtered_df = attack_df[attack_df['case_description'].isin([
    '제2연평해전', '천안함 피격 사건', '연평도 무력공격', 'DMZ 목함지뢰 도발'
])]


attack_count = len(attack_df)
attack_df['Type'] = 'attack'

# 사건명을 통해 메인에서 넘어오는것과 라디오 버튼 선택을 위한 설정
view_mapping = {
    'attack_case_1': '제2연평해전',
    'attack_case_2': '천안함 피격 사건',
    'attack_case_3': '연평도 무력공격',
    'attack_case_4': 'DMZ 목함지뢰 도발'
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
initial_view = st.session_state.get('subview', 'attack_case_1')
if initial_view not in valid_views:
    initial_view = 'attack_case_1'

# 사이드바 라디오 버튼으로 사건 선택
labels = list(view_mapping.values())
subview_label = st.sidebar.radio(
    "사건",
    labels,
    index=labels.index(view_mapping[initial_view])
)

# 경도, 위도 가져오기위함함 
coords_attack = filtered_df[['latitude', 'longitude']].dropna().values.tolist()

# 경도 위도 맞는지 실수형으로 만들어서 확인하는 함수
def is_valid_coord(val):
    try:
        float_val = float(val)
        return not pd.isnull(float_val)
    except (ValueError, TypeError):
        return False
    

# 페이지 시작
subview = reverse_mapping[subview_label]

st.title("📰 뉴스기사 크롤링을 통한 북한 도발 징후 포착")
st.header('피습 도발 사건 징후 분석', divider=True)

# 아이콘 설정
m_icon = get_icon_name('피습')
m_icon_color = case_color_map('피습')

# 각 사건별 상세 페이지 출력 (all_case.py의 render_event_case)사용
if subview == "attack_case_1":
    render_event_case(
        case_title='1. 제2연평해전',
        date='2002년 6월 29일',
        content_lines=[
            "북방한계선 남쪽의 연평도 인근에서 대한민국 해군 함정과 북한 경비정 간 발생한 해상전투",
            "북한이 북방한계선을 인정하지 않고 어선을 보호한다는 명분으로 침범 및 철수를 반복하던 중 발생함",
            "대한민국 해군은 연평해전을 계기로 교전규칙을 소극적 대응에서 적극적인 응전 개념으로 수정함",
            "북한 경비정의 북방한계선 침범시 '경고방송 · 시위기동 · 차단기동(밀어내기 작전) · 경고사격 · 조준격파사격'의 5단계 대응에서 '시위기동 · 경고사격 · 조준격파사격'의 3단계 대응으로 개정되었음",
            ("출처: 한국민족문화대백과사전")
        ],
        coords=coords_attack[0],
        casenum=1,
        event_type='피습'
    )

elif subview == "attack_case_2":
    render_event_case(
        case_title='2. 천안함(PCC-772) 피격',
        date='2010년 3월 26일',
        content_lines=[
            "오후 21시 22분경 백령도 서남방 2.5km 해상에서 경계 임무 수행중인 천안함이 북한 잠수정의 기습 어뢰공격으로 침몰",
            "승조원 104명 중 46명 전사",
            "북한이 제조한 고성능 폭약 250kg 규모 어뢰의 근접 수중폭발로 침몰했다는 것이 민관합동조사단의 공식적인 최종결론",
            "그러나 북한은 자신들의 소행임을 완강하게 부인함",
            "여러 음모론이 난무하는 가운데 '수중폭발 충격응답 시뮬레이션' 기술을 통해 천안함의 침몰 원인이 '(어뢰) 비접촉 폭발'에 의한 것이라는 점이 밝혀짐",
            "(홍재화, '천안함 일부 음모론 잠재운 건 대덕 과학자'···30년 함정 생존성 외길 연구로 '명예 해군준장', 헬로디디, 2024.10.15)"
        ],
        coords=coords_attack[1],
        casenum=4,
        event_type='피습'
    )

elif subview == "attack_case_3":
    render_event_case(
        case_title='3. 연평도 포격',
        date='2010년 11월 23일',
        content_lines=[
            "연평도 내의 군부대 뿐만 아니라 민가를 구별하지 않고 무차별적으로 170여발의 포격을 자행",
            "우리군은 이에 K-9 자주포로 즉각 대응 사격",
            "6.25 전쟁 이후 한국 영토에 대한 북한의 첫 공격이며 민간인을 가리지 않고 무차별적으로 공격한 사건",
            "이 사건으로 해병 2명이 전사하고 16명이 중경상을 입음",
            "이 사건으로 민간인 2명이 사망하고 다수의 부상자가 발생",
            "연평도 피격은 김정은의 업적 쌓기의 일환으로 벌인 대남도발이라는 것이 전문가들의 주장임",
            "우리의 정례적 해상사격훈련을 구실로 훈련 종료 후 10분 뒤 포격을 시작함",
            "(김주원, [김씨 일가의 숨겨진 진실] 연평도 포격전, 자유아시아방송, 2023.01.11.)"
        ],
        coords=coords_attack[2],
        casenum=5,
        event_type='피습'
    )

elif subview == "attack_case_4":
    render_event_case(
        case_title='4. DMZ 목함지뢰 매설',
        date='2015년 8월 4일',
        content_lines=[
            "오후 7시 35분과 40분 두 차례에 걸쳐 경기도 파주시 인근 DMZ 남측 GP 추진철책 통문하단에 북한측이 설치한 목함지뢰가 폭발",
            "GP 추진철책 통문하단 북측 40cm 지점과 남측 25cm 지점에 매설됨",
            "두 차례의 폭발로 인한 한국군 하사 2명이 다리가 절단되는 심각한 부상 입음",
            "폭발물은 북한군이 사용하는 목함지뢰로 확인됨",
            "북한이 의도적으로 우리 병력을 해칠 목적으로 매설한 것으로 판단됨",
            "(한겨레신문, [속보] DMZ 지뢰 폭발, 북한이 설치한 ‘목함지뢰’가 원인)"
        ],
        coords=coords_attack[3],
        casenum=8,
        event_type='피습'
    )

st.header('전체 피습 사건')
st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)


# 피습 도발 사건 유형 공통 설명

with st.container():
    acol1, acol2, acol3 = st.columns(3, gap='medium')
    with acol1:
        # 도발 지도 시각화 (mapfunc.py의 all_map_markers사용)
        st.subheader('🗺️ 도발지점')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        m = all_map_markers(attack_df, m_icon_color, center=(36.4642135, 128.0016985))
        st_folium(m, width=550, height=550)

    with acol2:
        # 정권별 피습 도발 횟수 (regime_case의 draw_regime_type_chart함수 사용)
        st.subheader('정권별 피습 도발 횟수')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        regime_choice = st.radio(
            "##### 정권별 피습 도발 횟수 보기",
            ('북한 정권 기준', '남한 정권 기준'),
            horizontal=True,
            key='attack_radio',
            label_visibility="collapsed"
        )
        draw_regime_type_chart(
            df=attack_df,
            regime_type='북한' if regime_choice == '북한 정권 기준' else '남한',
            attack_type='피습'
        )

    with acol3:
        # 피습사건 개요 설명 (all_case의 make_summary_table함수 사용)
        st.subheader('피습 사건')
        st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)
        content_lines = [
            "북한의 피습 사건은 군사적 긴장 조성과 체제 내부 결속을 위한 주요 수단으로 반복되어 왔음",
            "대표적인 사건으로는 1976년 판문점 도끼 만행 사건, 2010년 천안함 피격, 연평도 포격, 2020년 연평도 해역 공무원 피격 등이 있음",
            "이들 사건은 군인을 비롯한 민간인의 희생을 초래하였고, 한반도 안보 위기를 심화시키는 계기가 되었음",
            "특히 천안함 사건과 연평도 포격은 한국 해군과 민간인을 대상으로 한 직접적인 무력 도발로 국제 사회의 강한 비판을 받았음",
            "북한은 이러한 도발의 책임을 부인하거나 외부 요인으로 전가하며 내부 결속과 외부 협상력을 강화하는 전략적 수단으로 활용해옴",
            "출처: 국가정보원, 통일부 북한정보포털"
        ]
        st.markdown(make_summary_table("피습 사건", attack_count, content_lines), unsafe_allow_html=True)


# 메인페이지로 돌아가기 버튼
if st.button("🏠 메인 페이지로 돌아가기"):
    st.switch_page("main.py")

