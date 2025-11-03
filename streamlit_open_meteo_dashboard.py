import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
import folium

st.title("🌦️ Open-Meteo Interactive Weather Dashboard")
st.write("지도에서 위치를 클릭하면 해당 지역의 시간별 기온 데이터를 불러옵니다.")

# ---- 지도 생성 ----
st.subheader("1️⃣ 지역 선택 (지도를 클릭하세요)")
m = folium.Map(location=[37.5665, 126.9780], zoom_start=5)

# folium 클릭 이벤트 등록
clicked = st_folium(m, width=700, height=500)

# ---- 클릭된 좌표 처리 ----
if clicked and clicked["last_clicked"]:
    lat = clicked["last_clicked"]["lat"]
    lon = clicked["last_clicked"]["lng"]

    st.success(f"📍 선택된 위치: 위도 {lat:.4f}, 경도 {lon:.4f}")

    # ---- Open-Meteo API 요청 ----
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": "temperature_2m",
        "timezone": "auto"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        # ---- JSON → DataFrame 변환 ----
        df = pd.DataFrame({
            "time": data["hourly"]["time"],
            "temperature (°C)": data["hourly"]["temperature_2m"]
        })

        # ---- 시각화 ----
        st.subheader("2️⃣ 시간별 기온 변화 그래프")
        fig = px.line(
            df,
            x="time",
            y="temperature (°C)",
            title=f"{lat:.2f}, {lon:.2f} 지역의 시간별 기온",
            labels={"time": "시간", "temperature (°C)": "기온(℃)"}
        )
        st.plotly_chart(fig, use_container_width=True)

        # ---- 표로 보기 ----
        st.subheader("3️⃣ 원시 데이터 보기 (상위 24개)")
        st.dataframe(df.head(24))

    except Exception as e:
        st.error(f"데이터 요청 중 오류 발생: {e}")

else:
    st.info("지도를 클릭하면 해당 지역의 날씨 데이터를 가져옵니다.")
