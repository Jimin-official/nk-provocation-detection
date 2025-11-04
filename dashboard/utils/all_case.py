import streamlit as st
from mapfunc import create_folium_map_stop
from utils.make_wc import wordcloud
from utils.icon import get_icon_name, case_color_map

# 사건별 지맵 및 사건 내용html 함수
def render_event_case(case_title, date, content_lines, coords, casenum, event_type):
    m_icon = get_icon_name(event_type)
    m_icon_color = case_color_map(event_type)

    st.header(case_title)
    col1, col2 = st.columns([1, 2], gap='medium')

    with col1:
        with st.container():
            create_folium_map_stop(
                lat=coords[0], lon=coords[1],
                width=550, height=400,
                zoom_start=5.5,
                icon_name=m_icon, icon_color=m_icon_color,
                tooltip=None, popup_text=None
            )

    with col2:
        table_html = (
            '<table border="1" style="width:100%; border-collapse:collapse;">'
            '<tr>'
            f'<td style="width:20%; font-weight:bold; vertical-align:top;">일시</td>'
            f'<td>{date}</td>'
            '</tr>'
        )

        if content_lines:
            table_html += (
                f'<tr>'
                f'<td style="width:20%; font-weight:bold; vertical-align:top; border-right:1px solid #444;" '
                f'rowspan="{len(content_lines)}">내용</td>'
                f'<td style="padding:5px; word-wrap:break-word; overflow-wrap:break-word; '
                f'white-space:normal; border-bottom:1px solid #444;">{content_lines[0]}</td>'
                f'</tr>'
            )

            for line in content_lines[1:]:
                table_html += (
                    f'<tr>'
                    f'<td style="padding:5px; word-wrap:break-word; overflow-wrap:break-word; '
                    f'white-space:normal; border-bottom:1px solid #444;">{line}</td>'
                    f'</tr>'
                )

        table_html += '</table>'
        st.markdown(table_html, unsafe_allow_html=True)

    st.markdown("<hr style='border:2px dashed #aaa;'>", unsafe_allow_html=True)
    st.header('📰 웹 크롤링을 통한 도발전/ 평온 시기 비교')
    st.subheader('1) 뉴스기사 선정 시기')
    st.markdown(
        """
        <div style='width:35%;'>  
            <table style='font-size:18px; border-collapse:collapse; width:100%; table-layout:fixed;'>
                <tr>
                    <td style='font-weight:bold; padding:8px; border:1px solid #444; text-align:center;'>도발전 수집기간</td>
                    <td style='padding:8px; border:1px solid #444;'>도발일 기준 1개월 전</td>
                </tr>
                <tr>
                    <td style='font-weight:bold; padding:8px; border:1px solid #444; text-align:center;'>비교군 수집기간</td>
                    <td style='padding:8px; border:1px solid #444;'>2011-03-01 ~ 2011-09-30</td>
                </tr>
                <tr>
                    <td style='font-weight:bold; padding:8px; border:1px solid #444; text-align:center;'>비교 방법</td>
                    <td style='padding:8px; border:1px solid #444;'>워드 클라우드</td>
                </tr>
            </table>
        </div>
        """,
        unsafe_allow_html=True
    )
    st.subheader('2) 뉴스기사 비교')

    wordcloud(casenum)

# 공통부분 사건 정보html 함수
def make_summary_table(title: str, count: int, content_lines: list[str]) -> str:
    table_html = (
        f'<table border="1" style="width:100%; border-collapse:collapse;">'
        f'<tr>'
            f'<td style="width:20%; font-weight:bold; vertical-align:top;">{title} 횟수</td>'
            f'<td>{count}회</td>'
        f'</tr>'
    )
    table_html += (
        f'<tr>'
        f'<td style="width:20%; font-weight:bold; vertical-align:top;" rowspan="{len(content_lines)}">내용</td>'
        f'<td style="padding:5px; word-wrap:break-word; overflow-wrap:break-word; white-space:normal;">{content_lines[0]}</td>'
        f'</tr>'
    )
    for line in content_lines[1:]:
        table_html += (
            f'<tr>'
            f'<td style="padding:5px; word-wrap:break-word; overflow-wrap:break-word; white-space:normal;">{line}</td>'
            f'</tr>'
        )
    table_html += '</table>'
    return table_html