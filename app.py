import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd
import plotly.express as px
from datetime import datetime

# ============================
# Konfigurasi Awal
# ============================
st.set_page_config(page_title="📈 Real-Time Market News", layout="wide")
st.markdown("""
    <style>
        .reportview-container {
            background: linear-gradient(to right, #ffffff, #f4f6f8);
        }
        .css-1d391kg { background-color: transparent; }
        .css-ffhzg2 { font-family: 'Segoe UI', sans-serif; }
        .stSlider > div { padding-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)

# ============================
# API Configuration
# ============================
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"
BASE_URL = "https://newsapi.org/v2/everything"

# ============================
# Fungsi Ambil Berita
# ============================
def fetch_news(query="forex", page=1):
    try:
        params = {
            "q": query,
            "language": "en",
            "pageSize": 10,
            "page": page,
            "apiKey": API_KEY
        }
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        return data.get("articles", []), data.get("totalResults", 0)
    except:
        return [], 0

# ============================
# Fungsi Dampak Berita (dummy logic)
# ============================
def calculate_impact(articles):
    impact = {"Forex": 0, "Crypto": 0, "Saham": 0}
    for article in articles:
        title = article["title"].lower()
        if "forex" in title or "currency" in title:
            impact["Forex"] += 1
        elif "crypto" in title or "bitcoin" in title:
            impact["Crypto"] += 1
        elif "stock" in title or "equity" in title:
            impact["Saham"] += 1
    return impact

# ============================
# UI Sidebar
# ============================
st.sidebar.title("📂 Opsi Berita")
category = st.sidebar.selectbox("Pilih kategori", ["Semua", "Forex", "Crypto", "Saham"])
search_keyword = st.sidebar.text_input("🔍 Cari berita", value="")
refresh = st.sidebar.button("🔄 Refresh Berita")
dark_mode = st.sidebar.toggle("🌙 Dark Mode", value=False)

if dark_mode:
    st.markdown("""
        <style>
            body, .reportview-container {
                background-color: #1e1e1e;
                color: #ffffff;
            }
        </style>
    """, unsafe_allow_html=True)

# ============================
# Proses Keyword
# ============================
query_map = {
    "Semua": "markets",
    "Forex": "forex",
    "Crypto": "crypto",
    "Saham": "stock market"
}

query = query_map.get(category, "markets")
if search_keyword:
    query += f" {search_keyword}"

# ============================
# Ambil dan Tampilkan Berita
# ============================
st.title("📰 Real-Time Market News")
st.markdown("Pantau berita **Forex**, **Crypto**, dan **Saham** dari berbagai sumber terpercaya.")

news, total = fetch_news(query=query)

if not news:
    st.error("❌ Gagal mengambil berita. Coba lagi nanti.")
else:
    total_pages = (total // 10) + 1
    if total_pages > 1:
        page = st.slider("📑 Halaman", 1, total_pages, 1)
        news, _ = fetch_news(query=query, page=page)
    else:
        page = 1

    for article in news:
        with st.container():
            st.subheader(article['title'])
            st.write(f"📅 {article['publishedAt'][:10]} | 📰 {article['source']['name']}")
            st.write(article['description'])
            st.markdown(f"[Baca Selengkapnya]({article['url']})")
            st.markdown("---")

    # ============================
    # Grafik Dampak Harian
    # ============================
    impact = calculate_impact(news)
    data = pd.DataFrame({
        "Market": list(impact.keys()),
        "Jumlah Berita": list(impact.values())
    })
    fig = px.bar(data, x="Market", y="Jumlah Berita", color="Market",
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title="📊 Dampak Berita Hari Ini")
    st.plotly_chart(fig, use_container_width=True)

# ============================
# Footer
# ============================
st.markdown("---")
st.caption("Dibuat oleh Muhammad Harits Syahdan · Powered by NewsAPI.org")
