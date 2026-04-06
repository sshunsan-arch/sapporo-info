import streamlit as st
import requests
from bs4 import BeautifulSoup

# アプリのタイトル
st.set_page_config(page_title="札幌 交通・生活インフォ", page_icon="❄️")
st.title("❄️ 札幌 交通・生活インフォメーション")

# --- 1. 天気情報コーナー ---
st.header("🌤️ 今日の札幌の天気")
url_weather = "https://www.jma.go.jp/bosai/forecast/data/forecast/016000.json"
try:
    weather_data = requests.get(url_weather).json()
    today_weather = weather_data[0]['timeSeries'][0]['areas'][0]['weathers'][0]
    st.info(f"今日の天気: **{today_weather}**")
except:
    st.error("天気情報を取得できませんでした。")

# --- 2. 地下鉄情報コーナー ---
st.header("🚇 地下鉄の運行状況")
url_subway = "https://operationstatus.city.sapporo.jp/unkojoho/"
try:
    response = requests.get(url_subway)
    response.encoding = response.apparent_encoding
    soup = BeautifulSoup(response.text, 'html.parser')
    page_text = soup.get_text()

    if "10分以上の遅れは発生していません" in page_text:
        st.success("✅ 平常どおり運行しています")
    else:
        st.warning("⚠️ 何らかの運行情報（遅延・運休等）が出ています！")
except:
    st.error("情報を取得できませんでした。")

# --- 3. JR北海道コーナー（APIステータス判定の完璧版！） ---
st.header("🚆 JR北海道 (札幌近郊)")
url_jr = "https://www3.jrhokkaido.co.jp/webunkou/json/area/area_01.json"

try:
    response_jr = requests.get(url_jr)
    data_jr = response_jr.json()
    
    # ★大発見！JSONデータから今日の「札幌近郊(spo)」のステータス数字を直接抜き出します
    spo_status = data_jr['today']['areaStatus']['spo']

    # 2＝平常、それ以外（1など）＝異常あり
    if spo_status == 2:
        st.success("✅ 現在、平常どおり運行しています")
    else:
        st.warning("⚠️ 札幌近郊のJRに遅延や運休が発生している可能性があります！")

except Exception as e:
    st.error("情報を取得できませんでした。")

# --- 4. 札幌市電コーナー（新規追加！） ---
st.header("🚋 札幌市電")
url_shiden = "http://navi.stsp.or.jp/Densha/PC/AccidentInformation.aspx"
try:
    response_shiden = requests.get(url_shiden)
    response_shiden.encoding = response_shiden.apparent_encoding
    soup_shiden = BeautifulSoup(response_shiden.text, 'html.parser')
    text_shiden = soup_shiden.get_text()

    if "遅延" in text_shiden or "運休" in text_shiden or "見合わせ" in text_shiden:
        st.warning("⚠️ 市電に遅延などの運行情報が出ています！")
    else:
        st.success("✅ 現在、平常どおり運行しています")
except:
    st.error("情報を取得できませんでした。")
