import streamlit as st
import requests
import pandas as pd
from datetime import datetime
import pytz

# API KEY NewsAPI
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

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
        "time": item["publishedAt"],
        "url": item["url"]
    } for item in data.get("articles", [])]

# Konversi waktu ke lokal
def format_time(iso_time):
    utc_dt = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Jakarta"))
    return local_dt.strftime("%d %b %Y %H:%M WIB")

# Streamlit Config
st.set_page_config(page_title="📰 Real-Time News", layout="wide")

# Header
st.markdown("""
    <style>
    .main-title {
        font-size: 40px;
        font-weight: 700;
        color: #222831;
        margin-bottom: 0.5em;
    }
    .subtitle {
        font-size: 18px;
        color: #666;
    }
    .news-card {
        border-radius: 10px;
        padding: 20px;
        margin-bottom: 15px;
        background-color: #f8f9fa;
        box-shadow: 0 1px 4px rgba(0,0,0,0.1);
    }
    .news-title {
        font-size: 20px;
        font-weight: bold;
        color: #212529;
    }
    .news-meta {
        font-size: 14px;
        color: #888;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📰 Real-Time Market News</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pantau berita *Forex*, *Saham*, dan *Crypto* terbaru dari sumber terpercaya.</div>', unsafe_allow_html=True)

# Pilihan kategori
category_map = {
    "📈 Forex / Saham": "business",
    "💻 Teknologi": "technology",
    "🪙 Crypto": "general",  # General karena NewsAPI belum support kategori crypto khusus
}

selected = st.selectbox("Pilih kategori berita:", list(category_map.keys()))
selected_category = category_map[selected]

if st.button("🔄 Muat Ulang Berita"):
    with st.spinner("Mengambil berita terbaru..."):
        news = get_newsapi_data(selected_category)
        if news:
            for item in news:
                st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{item['title']}</div>
                        <div class="news-meta">🕒 {format_time(item['time'])} | 📰 {item['source']}</div>
                        <a href="{item['url']}" target="_blank">🌐 Baca Selengkapnya</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Tidak bisa mengambil berita. Coba beberapa saat lagi.")
