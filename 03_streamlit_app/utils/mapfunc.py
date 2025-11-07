# folium map 생성 함수
import folium 
import streamlit as st
from streamlit_folium import st_folium

# 사건별 첫번째 맵 그릴때 사용 함수
def create_folium_map_stop(lat, lon, 
                      width=420, height=420, 
                      zoom_start=6, 
                      icon_name='rocket', icon_color='darkred',
                      map_center=None,
                      tooltip=None, popup_text=None):
    if map_center is None:
        map_center = [lat, lon]
        
    m = folium.Map(
        location=map_center, 
        zoom_start=zoom_start, 
        scrollWheelZoom=False,
        dragging=False        
    )
    folium.Marker(
        [lat, lon],
        tooltip=tooltip,
        popup=popup_text,
        icon=folium.Icon(icon=icon_name, prefix='fa', color=icon_color)
    ).add_to(m)
    st.markdown('<div style="text-align:center">', unsafe_allow_html=True)
    st_data = st_folium(m, width=width, height=height)
    st.markdown('</div>', unsafe_allow_html=True)


# 사건별 공통 맵 함수
def all_map_markers(df, color, center=(36.53375, 127.82025), zoom=6):
    m = folium.Map(
        location=center,
        zoom_start=zoom,
        scrollWheelZoom=False,
        dragging=False
    )
    coords = df[['latitude', 'longitude', 'case_description']].dropna().values.tolist()
    for lat, lon, _ in coords:
        try:
            lat_f, lon_f = float(lat), float(lon)
            folium.CircleMarker(
                location=[lat_f, lon_f],
                radius=2,
                color=color,
                fill=True,
                fill_color=color,
                fill_opacity=0.8
            ).add_to(m)
        except (ValueError, TypeError):
            continue
    return m