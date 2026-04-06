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

# --- 3. JR北海道コーナー（本番環境でのブロック対策版） ---
st.header("🚆 JR北海道 (札幌近郊)")
# 再び、通常の運行情報ページを表示用URLとして使います
url_jr = "https://www3.jrhokkaido.co.jp/webunkou/area_spo.html"

try:
    # ユーザー（人間）がブラウザでアクセスしているように見せかけるおまじない
    headers = {'User-Agent': 'Mozilla/5.0'}
    response_jr = requests.get(url_jr, headers=headers, timeout=10)
    response_jr.encoding = 'utf-8' # 文字化け防止
    
    soup_jr = BeautifulSoup(response_jr.text, 'html.parser')
    text_jr = soup_jr.get_text()

    # 「その他のエリア」を切り捨てて札幌近郊だけに絞る
    if "その他のエリアの運行情報" in text_jr:
        text_jr = text_jr.split("その他のエリアの運行情報")[0]

    # ★最終的な判定ロジック
    # 「情報はありません」という言葉があれば平常、なければ異常
    if "情報はありません" in text_jr:
        st.success("✅ 現在、目立った遅延情報は出ていないようです（平常運行）")
    else:
        st.warning("⚠️ 札幌近郊のJRに遅延や運休が発生している可能性があります！")

except Exception as e:
    st.error(f"情報を取得できませんでした。時間をおいて再度お試しください。")

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
