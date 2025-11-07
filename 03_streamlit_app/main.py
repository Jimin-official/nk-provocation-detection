import numpy as np
import pandas as pd
import streamlit as st
import folium
from streamlit_folium import st_folium
import matplotlib.pyplot as plt
from sqlalchemy import create_engine
import streamlit.components.v1 as components
from utils.icon import get_icon_name
from utils.regime_case import draw_regime_main_chart

plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['font.family'] = 'Malgun Gothic'

# 페이지 넓게
st.set_page_config(layout='wide')

st.title("📰 뉴스기사 크롤링을 통한 북한 도발 징후 포착 🚨")

# 구분선 html
st.markdown("<hr style='border: 1px solid #555; margin: 1px 0;'>", unsafe_allow_html=True)

# MySQL 데이터 불러오기
username = 'first'
password = '1emddlwh'
db_name = 'att_db'
host = 'localhost'
engine = create_engine(f"mysql+pymysql://{username}:{password}@{host}/{db_name}")
provocation_df = pd.read_sql('SELECT * FROM provocation', con=engine)

# 도발 유형별 필터링
attack_df = provocation_df[provocation_df['type'].str.contains('피습|연평|천안함|목함지뢰|공격|교전|침투', na=False)]
nuclear_df = provocation_df[provocation_df['type'].str.contains('핵', na=False)]
balloon_df = provocation_df[provocation_df['type'].str.contains('풍선|전단', na=False)]
missile_df = provocation_df[provocation_df['type'].str.contains('미사일', na=False)]

# 하나의 데이터프레임으로 합치기기
df_all = pd.concat([attack_df, balloon_df, missile_df, nuclear_df], ignore_index=True)

# 색상 및 레이블 정의
countries = ['피습 사건', '미사일','오물풍선', '핵실험']
color_map = {
    '피습 사건': '#FF6B6B',
    '핵실험': '#F0AD4E',
    '오물풍선': '#3CB371',
    '미사일': '#5BC0DE',
}

# 컬럼 나누기: 지도 / 차트
col1, col2 = st.columns([1, 1])

# 사건별별 아이콘 색상 지정
case_color_map = {
    '제2연평해전': 'darkred',
    '천안함 피격 사건': 'darkred',
    '연평도 무력공격': 'darkred',
    'DMZ 목함지뢰 도발': 'darkred',
    '북한의 1차 핵실험': 'orange',
    '북한의 2차 핵실험': 'orange',
    '북한의 3차 핵실험': 'orange',
    '북한의 4차 핵실험': 'orange',
    '북한의 5차 핵실험': 'orange',
    '북한의 6차 핵실험': 'orange',
    '오물풍선': 'green',
    '동해안 단거리 미사일': 'blue',
    '신형 단거리 탄도 미사일': 'blue',
    'NLL 이남 대륙간 탄도 미사일': 'blue'
}
 

#### 지도 시작 부분

with col1:
    # 지도 제목, i 아이콘 위치
    col_title, col_icon = st.columns([20, 1])

    with col_title:
        st.markdown("##### 🗺️도발 위치 지도")

    # HTML로 i 아이콘 생성
    with col_icon:
        st.markdown(
            """
            <div style="position: relative; display: inline-block; cursor: pointer;">
                <i class="fa fa-info-circle" style="font-size: 26px; text-shadow: 0 0 5px black;"></i>
                <div style="
                    visibility: hidden;
                    width: 120px;
                    background-color: rgba(50, 50, 50, 0.95);
                    color: #fff;
                    border: 1px solid #ccc;
                    text-align: left;
                    border-radius: 6px;
                    padding: 10px;
                    position: absolute;
                    z-index: 99999;
                    top: 50%;
                    right: 100%;  /* 오른쪽에 붙었으니 왼쪽으로 뜨게 */
                    margin-right: 10px;
                    transform: translateY(-50%);
                    opacity: 0;
                    transition: opacity 0.3s ease-in-out;
                    font-size: 13px;
                    box-shadow: 0 0 10px rgba(0,0,0,0.7);
                ">
                    <div style="margin-bottom: 6px;">
                        <i class="fa fa-user" style="color: red; font-size: 16px;"></i> : 피습 사건
                    </div>
                    <div style="margin-bottom: 6px;">
                        <i class="fa fa-bomb" style="color: orange; font-size: 16px;"></i> : 핵실험
                    </div>
                    <div style="margin-bottom: 6px;">
                        <i class="fa fa-circle" style="color: green; font-size: 16px;"></i> : 오물풍선
                    </div>
                    <div>
                        <i class="fa fa-rocket" style="color: blue; font-size: 16px;"></i> : 미사일
                    </div>
                </div>
                <style>
                    div:hover > div {
                        visibility: visible !important;
                        opacity: 1 !important;
                    }
                </style>
            </div>
            <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet">
            """,
            unsafe_allow_html=True
        )

    m = folium.Map(location=[38.5, 127.9], zoom_start=6)

    # 좌표가 있는지 없는지 판단하기 위해 float으로 바꿔보는 함수
    def is_valid_coord(val):
        try:
            float_val = float(val)
            return not pd.isnull(float_val)
        except (ValueError, TypeError):
            return False
        
    # 마커 저장용 맵
    marker_category_map = {}

    # 마커 추가 함수        
    def add_markers(coords_list, category, color_fallback, name_map=None, case_name=None, limit_one=False, is_date=False):
        for lat, lon, case_or_date in coords_list:
            # 오물풍선같은 단일 사건이면 해당사건명 사용 / 아니면 리스트에 있는 값 사용
            base_name = case_name if case_name else case_or_date
            # 미사일같이 사건일로 사건명 지정시 사용하기 위한 함수
            if name_map:
                if is_date:
                    # 날짜 포맷으로 변환 후 매핑
                    date_str = pd.to_datetime(base_name).strftime('%Y-%m-%d')
                    # 사건명 받기기
                    actual_case_name = name_map.get(date_str, base_name)
                else:
                    actual_case_name = name_map.get(base_name, base_name)
            else:
                actual_case_name = base_name
            
            # 마커 툴팁과 팝업에 사용할 텍스트 설정
            tooltip_text = actual_case_name
            popup_text = actual_case_name

            # 위도/경도가 있는 경우만 마커 추가
            if is_valid_coord(lat) and is_valid_coord(lon):
                # 색상 및 아이콘 설정
                color = case_color_map.get(actual_case_name, color_fallback)
                icon_name = get_icon_name(actual_case_name)
                # Folium 마커 추가
                folium.Marker(
                    [float(lat), float(lon)],
                    tooltip=tooltip_text,
                    icon=folium.Icon(color=color, icon=icon_name, prefix='fa'),
                    popup=folium.Popup(f"<b>{popup_text}</b><br>위도: {lat}<br>경도: {lon}", max_width=300)
                ).add_to(m)
                # 선택된 마커에 따라 페이지 이동을 위해 카테고리 맵에 저장
                marker_category_map[actual_case_name] = category

                # limit_one이 True이면 마커 하나만 추가하고 종료 / 미사일 동일날짜 한번만 찍기 위함
                if limit_one:
                    break

    # attack 마커 표시
    attack_filter = attack_df[attack_df['case_description'].isin(['제2연평해전', '천안함 피격 사건', '연평도 무력공격', 'DMZ 목함지뢰 도발'])]
    coords_attack = attack_filter[['latitude', 'longitude', 'case_description']].dropna().values.tolist()
    add_markers(coords_attack, category='attack', color_fallback='blue')

    # nuclear 마커 표시
    nuclear_case_names = {
        full_name: full_name[15:]
        for full_name in nuclear_df['case_description'].dropna().unique()
    }
    coords_nuclear = nuclear_df[['latitude', 'longitude', 'case_description']].dropna().values.tolist()
    add_markers(
        coords_nuclear,
        category='nuclear',
        color_fallback='red',
        name_map=nuclear_case_names
    )

    # balloon 마커 표시
    coords_balloon = balloon_df[['latitude', 'longitude', 'case_description']].dropna().values.tolist()
    add_markers(
        coords_balloon,
        category='balloon',
        color_fallback='orange',
        case_name='오물풍선',
        limit_one=True
    )

    # missile 마커 표시
    missile_case_names = {
        '2014-03-26': '동해안 단거리 미사일',
        '2019-05-09': '신형 단거리 탄도 미사일',
        '2022-11-02': 'NLL 이남 대륙간 탄도 미사일'
    }
    selected_dates = list(missile_case_names.keys())
    filtered_df = (
        missile_df[missile_df['date'].astype(str).isin(selected_dates)]
        .drop_duplicates(subset=['date'])
    )
    coords_missile = filtered_df[['latitude', 'longitude', 'date']].dropna().values.tolist()
    add_markers(
        coords_missile,
        category='missile',
        color_fallback='green',
        name_map=missile_case_names,
        is_date=True                  
    )

    map_data = st_folium(m, width=800, height=700)
    
    # 지도 아래 마커 클릭 안내 메시지
    st.markdown(
        """
        <style>
            .map-explanation {
                margin-top: -30px;
                font-size: 13px;
                color: gray;
            }
        </style>
        <div class='map-explanation'>
            💡 <b>안내:</b> 지도 위 마커를 <b>클릭</b>하면 아래에 사건 페이지로 이동할 수 있는 버튼이 표시됩니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    # 클릭된 마커 정보를 세션에 저장
    if 'selected_case' not in st.session_state:
        st.session_state.selected_case = None

    selected_case = None
    if map_data and map_data.get("last_object_clicked_tooltip"):
        selected_case = map_data["last_object_clicked_tooltip"]
        st.session_state.selected_case = selected_case

    if selected_case:
        st.session_state.selected_case = selected_case

    current_case = st.session_state.selected_case

    # 선택된 사건에 따라 해당 페이지로 이동 버튼 표시
    if current_case:
        st.markdown(f"선택된 사건: {current_case}", unsafe_allow_html=True)
        category = marker_category_map.get(current_case)
        if category == 'attack':
            if st.button("Attack 사건 페이지로 이동"):
                st.switch_page("pages/attack.py")
        elif category == 'nuclear':
            if st.button("Nuclear 사건 페이지로 이동"):
                st.switch_page("pages/nuclear.py")
        elif category == 'balloon':
            if st.button("Balloon 사건 페이지로 이동"):
                st.switch_page("pages/balloon.py")
        elif category == 'missile':
            if st.button("Missile 사건 페이지로 이동"):
                st.switch_page("pages/missile.py")
        else:
            st.info("카테고리를 찾을 수 없습니다.")

#### 오른쪽 차트
with col2:
    st.markdown("##### 정권별 도발 유형")
    regime_tabs = ['북한 정권별', '남한 정권별']
    tab1, tab2 = st.tabs(regime_tabs)

    # 북한 정권 차트
    with tab1:
        regime_order_n = ['임시정부', '김일성', '김정일', '김정은']
        draw_regime_main_chart(df_all, 'n_gov', regime_order_n, "북한 정권별 도발 유형")
    # 남한 정권 차트
    with tab2:
        regime_order_s = ['임시정부', '이승만', '윤보선', '박정희', '최규하', '전두환', '노태우', '김영삼', '김대중', '노무현', '이명박', '박근혜', '문재인', '윤석열']
        draw_regime_main_chart(df_all, 's_gov', regime_order_s, "남한 정권별 도발 유형")


    st.markdown("##### 도발 비율 차트")
    chart_tabs = ['연도별 누적 비율', '도발 유형 비율']
    tab1, tab2 = st.tabs(chart_tabs)

    with tab1:
        # 연도별 누적 비율 선그래프
        fig_left, ax_left = plt.subplots(figsize=(4.5, 1.5), facecolor='none') 
        total_overall = len(df_all)

        for t in countries:
            df_type = df_all[df_all['type'] == t].groupby('year').size()
            cumulative = df_type.cumsum()
            frequency = (cumulative / total_overall).fillna(0)
            ax_left.plot(frequency.index, frequency.values, marker='o', markersize=1.5, label=t, color=color_map[t])

        ax_left.set_xlabel('연도', color='white', fontsize=7)
        ax_left.set_ylabel('누적 비율', color='white', fontsize=7)
        ax_left.tick_params(axis='x', colors='white', labelsize=6)
        ax_left.tick_params(axis='y', colors='white', labelsize=6)
        ax_left.grid(True, linestyle='--', alpha=0.4)
        fig_left.patch.set_alpha(0.0)
        ax_left.set_facecolor('none')
        fig_left.tight_layout(pad=0.5) 
        st.pyplot(fig_left)

    with tab2:
        # 도발 유형 비율 파이 차트
        counts = {
            '피습 사건': len(attack_df),
            '미사일': len(missile_df),
            '오물풍선': len(balloon_df),
            '핵실험': len(nuclear_df)
        }
        total = sum(counts.values())

        def func(pct):
            absolute = int(round(pct/100 * total))
            return f"{absolute}건\n({pct:.1f}%)"

        fig_pie, ax_pie = plt.subplots(figsize=(4.5, 1.5), facecolor='none')
        wedges, texts, autotexts = ax_pie.pie(
            counts.values(),
            autopct=lambda pct: func(pct),
            startangle=220,
            wedgeprops={'edgecolor': 'k'},
            pctdistance=0.70,
            textprops={'fontsize': 7, 'color': 'white'},
            colors=[color_map[k] for k in counts.keys()]
        )
        centre_circle = plt.Circle((0, 0), 0.45, fc='black')
        fig_pie.gca().add_artist(centre_circle)
        ax_pie.axis('equal')
        ax_pie.set_facecolor('none')

        labels = list(counts.keys())
        for i, (wedge, autotext) in enumerate(zip(wedges, autotexts)):
            label = labels[i]
            if label == '핵실험':
                angle = (wedge.theta2 + wedge.theta1) / 2.
                x = 1.2 * np.cos(np.deg2rad(angle))
                y = 1.2 * np.sin(np.deg2rad(angle))
                autotext.set_position((x, y))
                autotext.set_fontsize(7)
                autotext.set_color('white')

        legend_labels = list(counts.keys())
        legend = ax_pie.legend(
            wedges,
            legend_labels,
            fontsize=8,
            handlelength=1.0,
            borderpad=0.5,
            labelspacing=0.7,
            loc='center',
            bbox_to_anchor=(0.75, 0.5),
            frameon=False
        )

        for text in legend.get_texts():
            text.set_color("white")

        fig_pie.tight_layout(pad=0.5)
        st.pyplot(fig_pie)