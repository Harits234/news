import streamlit as st
import requests
from datetime import datetime
import pytz

API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

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

def format_time(iso_time):
    utc_dt = datetime.strptime(iso_time, "%Y-%m-%dT%H:%M:%SZ")
    local_dt = utc_dt.replace(tzinfo=pytz.utc).astimezone(pytz.timezone("Asia/Jakarta"))
    return local_dt.strftime("%d %b %Y %H:%M WIB")

# Dark Theme Custom CSS
st.set_page_config(page_title="📰 Market News - Dark", layout="wide")

st.markdown("""
    <style>
    body {
        background-color: #121212;
        color: #f0f0f0;
    }
    .main-title {
        font-size: 40px;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 0.2em;
    }
    .subtitle {
        font-size: 18px;
        color: #aaaaaa;
        margin-bottom: 1.5em;
    }
    .news-card {
        background: #1e1e1e;
        padding: 20px;
        margin-bottom: 15px;
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(255,255,255,0.05);
        transition: all 0.2s ease-in-out;
    }
    .news-card:hover {
        background: #272727;
    }
    .news-title {
        font-size: 20px;
        font-weight: bold;
        color: #ffffff;
    }
    .news-meta {
        font-size: 13px;
        color: #888888;
        margin-bottom: 10px;
    }
    .read-more {
        font-size: 14px;
        color: #1fa7ff;
        text-decoration: none;
    }
    .read-more:hover {
        text-decoration: underline;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<div class="main-title">📰 Real-Time Market News</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Update berita terbaru seputar Forex, Saham, dan Crypto dalam tampilan dark premium.</div>', unsafe_allow_html=True)

# Pilih kategori
category_map = {
    "📈 Forex / Saham": "business",
    "💻 Teknologi": "technology",
    "🪙 Crypto": "general",
}

selected = st.selectbox("📊 Pilih kategori berita:", list(category_map.keys()))
selected_category = category_map[selected]

if st.button("🔄 Muat Berita Terbaru"):
    with st.spinner("Mengambil berita..."):
        news = get_newsapi_data(selected_category)
        if news:
            for item in news:
                st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{item['title']}</div>
                        <div class="news-meta">🕒 {format_time(item['time'])} | 📰 {item['source']}</div>
                        <a class="read-more" href="{item['url']}" target="_blank">🌐 Baca Selengkapnya</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Tidak ada berita yang bisa ditampilkan. Coba beberapa saat lagi.")
else:
    st.info("Klik tombol di atas untuk mulai mengambil berita.")
