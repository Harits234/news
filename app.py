import streamlit as st
import requests
from textblob import TextBlob
from datetime import datetime

st.set_page_config(page_title="Berita Harian Otomatis", layout="wide")

NEWS_API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

def get_daily_news(keyword="indonesia", language="id"):
    today = datetime.utcnow().strftime("%Y-%m-%d")
    url = f"https://newsapi.org/v2/everything?q={keyword}&from={today}&language={language}&sortBy=publishedAt&apiKey={NEWS_API_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get("articles", [])
    else:
        return []

def summarize_text(text):
    blob = TextBlob(text)
    summary = ". ".join(blob.sentences[:2])
    sentiment = blob.sentiment.polarity
    return summary, sentiment

st.title("📰 Berita Otomatis Terbaru Hari Ini")
st.markdown("Update otomatis setiap dibuka. Tanpa klik, tanpa ribet.")

# Pilih topik berita
keyword = st.selectbox("Topik berita hari ini:", ["politik", "ekonomi", "teknologi", "internasional", "kripto"])
max_articles = st.slider("Jumlah berita ditampilkan", 1, 10, 5)

# Ambil berita otomatis saat halaman dibuka
articles = get_daily_news(keyword)

if not articles:
    st.error("Gagal mengambil berita. Coba ganti kata kunci atau periksa API key.")
else:
    for i, article in enumerate(articles[:max_articles]):
        st.markdown(f"### {i+1}. {article['title']}")
        st.markdown(f"**Sumber:** {article['source']['name']} | **Tanggal:** {datetime.strptime(article['publishedAt'], '%Y-%m-%dT%H:%M:%SZ').strftime('%d %b %Y %H:%M')}")
        st.image(article.get("urlToImage", ""), width=600)
        st.markdown(f"*{article['description']}*")

        if article["content"]:
            summary, sentiment = summarize_text(article["content"])
            st.markdown("**📄 Ringkasan AI:**")
            st.write(summary)
            st.markdown(f"**📊 Sentimen:** {'Positif ✅' if sentiment > 0 else 'Negatif ❌' if sentiment < 0 else 'Netral ⚖️'}")

        st.markdown(f"[🔗 Baca Selengkapnya]({article['url']})")
        st.markdown("---")
