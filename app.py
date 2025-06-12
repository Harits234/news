import streamlit as st
import requests
from bs4 import BeautifulSoup
import plotly.express as px
import pandas as pd
import random

# ------------------ CONFIG ------------------ #
st.set_page_config(page_title="📰 Real-Time Market News", layout="wide")

# ------------------ STYLING ------------------ #
light_mode_css = """
<style>
body {
    background-color: white;
    color: black;
}
.news-card {
    background-color: #f8f9fa;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
    transition: 0.3s;
}
.news-card:hover {
    transform: scale(1.01);
}
</style>
"""

dark_mode_css = """
<style>
body {
    background-color: #0e1117;
    color: white;
}
.news-card {
    background-color: #1c1e26;
    border-radius: 10px;
    padding: 15px;
    margin-bottom: 15px;
    box-shadow: 0 4px 6px rgba(255,255,255,0.05);
    transition: 0.3s;
}
.news-card:hover {
    transform: scale(1.01);
}
</style>
"""

# Toggle Theme
mode = st.sidebar.radio("🎨 Theme Mode", ["Light", "Dark"])
if mode == "Light":
    st.markdown(light_mode_css, unsafe_allow_html=True)
else:
    st.markdown(dark_mode_css, unsafe_allow_html=True)

# ------------------ HEADER ------------------ #
st.title("📰 Real-Time Market News")
st.markdown("Pantau berita Forex, Saham, dan Crypto terbaru dari berbagai sumber terpercaya.")
st.divider()

# ------------------ INPUT ------------------ #
kategori = st.selectbox("📊 Pilih kategori berita:", ["Semua", "Forex", "Crypto", "Saham"])
search_query = st.text_input("🔍 Cari berita berdasarkan keyword:")

if st.button("🔄 Refresh Berita"):
    st.experimental_rerun()

# ------------------ FETCH DATA ------------------ #
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

@st.cache_data(show_spinner=False)
def get_newsapi_data():
    url = f"https://newsapi.org/v2/top-headlines?language=en&pageSize=100&apiKey={API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        articles = response.json()["articles"]
        return articles
    else:
        return []

news = get_newsapi_data()

# ------------------ FUNCTION ------------------ #
def detect_impact(title):
    title = title.lower()
    impacts = []
    if any(word in title for word in ["dollar", "eur", "usd", "inflation", "interest"]):
        impacts.append("Forex")
    if any(word in title for word in ["bitcoin", "crypto", "ethereum", "bnb"]):
        impacts.append("Crypto")
    if any(word in title for word in ["stock", "shares", "nasdaq", "s&p", "dow"]):
        impacts.append("Saham")
    return impacts if impacts else ["Umum"]

# ------------------ FILTER, SEARCH, PAGINATION ------------------ #
filtered_news = []
for item in news:
    impact = detect_impact(item['title'])
    item['impact'] = impact
    
    # Kategori filter
    if kategori != "Semua" and kategori not in impact:
        continue
    
    # Search keyword
    if search_query and search_query.lower() not in item['title'].lower():
        continue

    filtered_news.append(item)

# Pagination
items_per_page = 5
total_pages = (len(filtered_news) - 1) // items_per_page + 1
page = st.slider("📑 Halaman", 1, total_pages, 1)
start_idx = (page - 1) * items_per_page
end_idx = start_idx + items_per_page

# ------------------ DISPLAY NEWS ------------------ #
if filtered_news:
    for item in filtered_news[start_idx:end_idx]:
        st.markdown(f"""
            <div class='news-card'>
            <h4>{item['title']}</h4>
            <p><b>Source:</b> {item['source']['name']} | <b>Impact:</b> {', '.join(item['impact'])}</p>
            <p>{item['description'] or ''}</p>
            <a href="{item['url']}" target="_blank">🔗 Baca Selengkapnya</a>
            </div>
        """, unsafe_allow_html=True)
else:
    st.warning("❌ Gagal mengambil berita atau tidak ditemukan.")

# ------------------ GRAFIK ------------------ #
impact_data = [imp for item in filtered_news for imp in item['impact']]
if impact_data:
    df = pd.DataFrame(impact_data, columns=["Market"])
    data = df.value_counts().reset_index()
    data.columns = ["Market", "Jumlah Berita"]
    fig = px.bar(data, x="Market", y="Jumlah Berita", color="Market",
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title="Jumlah Berita yang Berdampak ke Market Hari Ini")
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("📉 Tidak ada data dampak berita untuk ditampilkan.")
