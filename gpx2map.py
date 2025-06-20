import streamlit as st
import gpxpy
import folium
from streamlit_folium import st_folium

st.title("GPX軌跡マップ表示")

uploaded_file = st.file_uploader("GPXファイルをアップロードしてください", type=["gpx"])

if uploaded_file is not None:
    # GPXパース
    gpx = gpxpy.parse(uploaded_file)

    # 最初のポイントを地図の中心に
    first_point = gpx.tracks[0].segments[0].points[0]
    m = folium.Map(location=[first_point.latitude, first_point.longitude], zoom_start=14)

    # 軌跡を描画
    for track in gpx.tracks:
        for segment in track.segments:
            points = [(p.latitude, p.longitude) for p in segment.points]
            folium.PolyLine(points, color="blue", weight=3).add_to(m)

            # スタートとゴールにマーカー
            folium.Marker(points[0], tooltip="Start", icon=folium.Icon(color='green')).add_to(m)
            folium.Marker(points[-1], tooltip="Finish", icon=folium.Icon(color='red')).add_to(m)

    # folium地図をstreamlitに埋め込み表示
    st_folium(m, width=700, height=500)

else:
    st.info("GPXファイルをアップロードすると軌跡が表示されます。")
