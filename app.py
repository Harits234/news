import streamlit as st
import requests
import pandas as pd
import datetime

# API Key kamu
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

# Mapping kategori untuk NewsAPI
category_map = {
    "💼 Forex / Saham": "business",
    "🖥️ Teknologi": "technology",
    "🪙 Crypto": "general",  # NewsAPI belum punya kategori khusus crypto
}

# Styling CSS
st.markdown("""
    <style>
        .news-card {
            border-radius: 12px;
            padding: 20px;
            margin-bottom: 20px;
            background-color: #f9f9f9;
            box-shadow: 0 4px 10px rgba(0,0,0,0.05);
        }
        .news-title {
            font-size: 20px;
            font-weight: bold;
            color: #333;
        }
        .news-meta {
            font-size: 13px;
            color: gray;
            margin-bottom: 10px;
        }
        .read-more {
            font-size: 14px;
            color: #0066cc;
            text-decoration: none;
        }
        .read-more:hover {
            text-decoration: underline;
        }
    </style>
""", unsafe_allow_html=True)

# Fungsi ambil data
def get_newsapi_data(category="business"):
    url = f"https://newsapi.org/v2/top-headlines?language=en&category={category}&pageSize=20&apiKey={API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    data = r.json()
    return [{
        "source": item["source"]["name"],
        "title": item["title"],
        "published": item["publishedAt"].replace("T", " ").replace("Z", ""),
        "url": item["url"]
    } for item in data.get("articles", [])]

# Header
st.set_page_config(page_title="📰 Market News", layout="wide")
st.markdown("<h1 style='text-align: center;'>📰 Real-Time Market News</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Pantau berita pasar global terkini dari berbagai sektor</p>", unsafe_allow_html=True)

# Sidebar
st.sidebar.header("📊 Kategori Berita")
selected_category_name = st.sidebar.radio("Pilih Kategori:", list(category_map.keys()))
selected_category = category_map[selected_category_name]

# Refresh button
if st.sidebar.button("🔄 Refresh Sekarang"):
    st.experimental_rerun()

# Konten berita
st.write(f"### Berita: {selected_category_name}")
with st.spinner("Mengambil berita terbaru..."):
    news = get_newsapi_data(selected_category)
    if news:
        for item in news:
            st.markdown(f"""
                <div class='news-card'>
                    <div class='news-title'>{item["title"]}</div>
                    <div class='news-meta'>🕒 {item["published"]} | 📰 {item["source"]}</div>
                    <a class='read-more' href='{item["url"]}' target='_blank'>🌐 Baca Selengkapnya</a>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.warning("❌ Gagal ambil berita. Coba lagi nanti.")
