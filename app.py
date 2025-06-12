import streamlit as st
import requests
import pandas as pd

# API Key kamu
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

# Fungsi ambil berita dari NewsAPI
def get_newsapi_data(category="business"):
    url = f"https://newsapi.org/v2/top-headlines?language=en&category={category}&pageSize=20&apiKey={API_KEY}"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    data = r.json()
    return [{
        "Source": item["source"]["name"],
        "Title": item["title"],
        "Time": item["publishedAt"].replace("T", " ").replace("Z", ""),
        "Link": item["url"]
    } for item in data.get("articles", [])]

# Tampilan Streamlit
st.set_page_config(page_title="📰 Real-Time Market News", layout="wide")
st.title("📰 Real-Time Market News")
st.markdown("Pantau berita *Forex*, *Saham*, dan *Crypto* terbaru dari berbagai sumber terpercaya via NewsAPI.org.")

# Kategori pilihan
category_map = {
    "Forex / Saham": "business",
    "Teknologi": "technology",
    "Crypto": "general",  # NewsAPI belum punya kategori khusus 'crypto', jadi kita pakai 'general'
}

selected = st.selectbox("📊 Pilih kategori berita:", list(category_map.keys()))
selected_category = category_map[selected]

if st.button("🔄 Refresh Berita"):
    with st.spinner("Mengambil berita..."):
        news = get_newsapi_data(selected_category)
        if news:
            for item in news:
                st.markdown(f"### {item['Title']}")
                st.markdown(f"🕒 {item['Time']} | 📰 {item['Source']}")
                st.markdown(f"[🌐 Baca Selengkapnya]({item['Link']})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("❌ Gagal ambil berita. Coba lagi nanti.")
