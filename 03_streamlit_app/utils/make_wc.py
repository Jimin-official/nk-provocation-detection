import streamlit as st


def wordcloud(casenum, ):
    direc = 'images/'+ str(casenum)

    tab_title = ['🇰🇵 북한 뉴스', '🇰🇷 남한 뉴스']
    [tab1, tab2] = st.tabs(tab_title)
    # 북한 기사 워드 클라우드
    with tab1:
        with st.container():
            st.markdown("#### 전체 뉴스기사")
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.image(direc + '_북한기사_전체_wordcloud.png')
                    st.markdown(
                        "<div style='text-align: center; font-size: 28px; font-weight: bold;'>도발 전</div>",
                        unsafe_allow_html=True
                    )

                with col2:
                    st.image('images/15_북한기사_전체_wordcloud.png')
                    st.markdown(
                        "<div style='text-align: center; font-size: 28px; font-weight: bold;'>평온 시기</div>",
                        unsafe_allow_html=True
                    )

            st.markdown("#### 검색어 뉴스기사(북한뉴스)")
            row = st.columns(4)
            with row[0]:
                with st.container(border=True):
                    st.write('검색어 : 한국, 남조선')
                    st.image(direc + '_북한기사_한국_wordcloud.png')
                    st.image('images/15_북한기사_한국_wordcloud.png')

            with row[1]:
                with st.container(border=True):
                    st.write('검색어 : 미국')
                    st.image(direc + '_북한기사_미국_wordcloud.png')
                    st.image('images/15_북한기사_미국_wordcloud.png')

            with row[2]:
                with st.container(border=True):
                    st.write('검색어 : 중국')
                    st.image(direc + '_북한기사_중국_wordcloud.png')
                    st.image('images/15_북한기사_중국_wordcloud.png')

            with row[3]:
                with st.container(border=True):
                    st.write('검색어 : 로씨야')
                    st.image(direc + '_북한기사_러시아_wordcloud.png')
                    st.image('images/15_북한기사_러시아_wordcloud.png')
            

    # 한국 기사 워드 클라우드
    with tab2:
        with st.container():
            st.markdown("#### 전체 뉴스기사")
            with st.container(border=True):
                col1, col2 = st.columns(2)
                with col1:
                    st.image(direc + '_남한기사_전체_wordcloud.png')
                    st.markdown(
                        "<div style='text-align: center; font-size: 28px; font-weight: bold;'>도발 전</div>",
                        unsafe_allow_html=True
                    )

                with col2:
                    st.image('images/15_남한기사_전체_wordcloud.png')
                    st.markdown(
                        "<div style='text-align: center; font-size: 28px; font-weight: bold;'>평온 시기</div>",
                        unsafe_allow_html=True
                    )
            
            st.markdown("#### 검색어 뉴스기사(남한뉴스)")
            row = st.columns(4)
            with row[0]:
                with st.container(border=True):
                    st.write('검색어 : 북한')
                    st.image(direc + '_남한기사_북한_wordcloud.png')
                    st.image('images/15_남한기사_북한_wordcloud.png')

            with row[1]:
                with st.container(border=True):
                    st.write('검색어 : 미국')
                    st.image(direc + '_남한기사_미국_wordcloud.png')
                    st.image('images/15_남한기사_미국_wordcloud.png')

            with row[2]:
                with st.container(border=True):
                    st.write('검색어 : 중국')
                    st.image(direc + '_남한기사_중국_wordcloud.png')
                    st.image('images/15_남한기사_중국_wordcloud.png')

            with row[3]:
                with st.container(border=True):
                    st.write('검색어 : 로씨야')
                    st.image(direc + '_남한기사_러시아_wordcloud.png')
                    st.image('images/15_남한기사_러시아_wordcloud.png') 