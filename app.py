import streamlit as st
import requests
from datetime import datetime
import pytz
from textblob import TextBlob

API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

# Keyword untuk mendeteksi dampak berita
impact_keywords = {
    "forex": ["usd", "eur", "inflation", "interest rate", "federal reserve", "ecb", "bank of japan", "forex", "currency", "yield"],
    "crypto": ["bitcoin", "ethereum", "crypto", "blockchain", "binance", "coinbase", "token", "web3", "defi"],
    "stocks": ["stock", "nasdaq", "dow", "earnings", "ipo", "tech stocks", "share price", "s&p", "equity", "elon musk", "tesla", "apple"]
}

def detect_impact(text):
    text = text.lower()
    impacted = []
    for market, keywords in impact_keywords.items():
        if any(keyword in text for keyword in keywords):
            impacted.append(market.capitalize())
    return impacted if impacted else ["Umum"]

def analyze_sentiment(text):
    blob = TextBlob(text)
    polarity = blob.sentiment.polarity
    if polarity > 0.2:
        return "🟢 Bullish"
    elif polarity < -0.2:
        return "🔴 Bearish"
    else:
        return "⚪️ Netral"

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

# Page config
st.set_page_config(page_title="📰 Market News AI", layout="wide")

# Custom CSS + Background Animation
st.markdown("""
<style>
body {
    background-color: #f4f6f8;
    color: #222222;
}
.main-title {
    font-size: 40px;
    font-weight: 800;
    color: #222222;
    margin-bottom: 0.2em;
}
.subtitle {
    font-size: 18px;
    color: #555555;
    margin-bottom: 1.5em;
}
.news-card {
    background: #ffffff;
    padding: 20px;
    margin-bottom: 15px;
    border-radius: 15px;
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
}
.news-title {
    font-size: 20px;
    font-weight: bold;
    color: #000000;
}
.news-meta {
    font-size: 13px;
    color: #666666;
    margin-bottom: 5px;
}
.impact-badge, .sentiment-badge {
    display: inline-block;
    background: #007bff;
    color: white;
    padding: 3px 10px;
    font-size: 12px;
    border-radius: 999px;
    margin-right: 5px;
}
.sentiment-badge {
    background: #28a745;
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

<!-- Animation: Particles.js -->
<div id="particles-js" style="position: fixed; width: 100%; height: 100%; z-index: -1;"></div>
<script src="https://cdn.jsdelivr.net/npm/particles.js@2.0.0/particles.min.js"></script>
<script>
particlesJS("particles-js", {
  "particles": {
    "number": {"value": 60},
    "color": {"value": "#007bff"},
    "shape": {"type": "circle"},
    "opacity": {"value": 0.2},
    "size": {"value": 4},
    "line_linked": {"enable": true,"distance": 100,"color": "#007bff","opacity": 0.2,"width": 1},
    "move": {"enable": true,"speed": 2}
  },
  "interactivity": {"detect_on": "canvas","events": {"onhover": {"enable": true,"mode": "grab"}}}
});
</script>
""", unsafe_allow_html=True)

# Header
st.markdown('<div class="main-title">📰 Real-Time Market News</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Pantau berita terbaru dengan AI Sentiment dan Dampak Market. Powered by NewsAPI & TextBlob.</div>', unsafe_allow_html=True)

# Pilihan kategori
category_map = {
    "📈 Forex / Saham": "business",
    "💻 Teknologi": "technology",
    "🪙 Crypto": "general",
}
selected = st.selectbox("📊 Pilih kategori berita:", list(category_map.keys()))
selected_category = category_map[selected]

# Button ambil berita
if st.button("🔄 Muat Berita Terbaru"):
    with st.spinner("Mengambil dan menganalisis berita..."):
        news = get_newsapi_data(selected_category)
        if news:
            for item in news:
                impact = detect_impact(item['title'])
                sentiment = analyze_sentiment(item['title'])
                impact_badges = " ".join([f'<span class="impact-badge">{i}</span>' for i in impact])
                st.markdown(f"""
                    <div class="news-card">
                        <div class="news-title">{item['title']}</div>
                        <div class="news-meta">🕒 {format_time(item['time'])} | 📰 {item['source']}</div>
                        <div>{impact_badges} <span class="sentiment-badge">{sentiment}</span></div>
                        <a class="read-more" href="{item['url']}" target="_blank">🌐 Baca Selengkapnya</a>
                    </div>
                """, unsafe_allow_html=True)
        else:
            st.error("❌ Tidak ada berita yang bisa ditampilkan. Coba beberapa saat lagi.")
else:
    st.info("Klik tombol di atas untuk mulai mengambil berita.")
