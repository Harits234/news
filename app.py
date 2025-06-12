import streamlit as st
import requests
from textblob import TextBlob
from datetime import datetime
import pytz
import pandas as pd
from collections import Counter
import plotly.express as px

# ------------------------- SETUP UI -------------------------
st.set_page_config(page_title="Real-Time Market News", layout="wide")

st.markdown("""
    <style>
        body {
            background-color: #ffffff;
            color: #111111;
            font-family: 'Segoe UI', sans-serif;
        }
        .news-card {
            background: rgba(255,255,255,0.95);
            border-radius: 15px;
            padding: 20px;
            margin: 10px 0;
            box-shadow: 0 4px 8px rgba(0,0,0,0.05);
        }
        .news-title {
            font-weight: bold;
            font-size: 20px;
            margin-bottom: 5px;
        }
        .news-meta {
            font-size: 13px;
            color: #777;
            margin-bottom: 10px;
        }
        .read-more {
            text-decoration: none;
            color: #007BFF;
            font-size: 14px;
        }
        .impact-badge {
            background-color: #f0f0f0;
            color: #000;
            border-radius: 5px;
            padding: 2px 6px;
            font-size: 12px;
            margin-right: 4px;
        }
        .sentiment-badge {
            background-color: #e0e0e0;
            border-radius: 4px;
            padding: 2px 6px;
            font-size: 12px;
        }
        .animated-bg {
            background: url('https://www.transparenttextures.com/patterns/white-wall-3.png');
            background-size: cover;
            background-repeat: repeat;
        }
    </style>
    <div class="animated-bg">
""", unsafe_allow_html=True)

# ------------------------- API & ANALYTICS -------------------------
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

def get_newsapi_data():
    url = (
        f"https://newsapi.org/v2/top-headlines?"
        "language=en&pageSize=30&apiKey=" + API_KEY
    )
    res = requests.get(url)
    if res.status_code == 200:
        articles = res.json().get("articles", [])
        return [
            {
                "title": a["title"],
                "url": a["url"],
                "source": a["source"]["name"],
                "time": a["publishedAt"]
            }
            for a in articles
        ]
    return []

def analyze_sentiment(text):
    polarity = TextBlob(text).sentiment.polarity
    if polarity > 0.1:
        return "📈 Positif"
    elif polarity < -0.1:
        return "📉 Negatif"
    else:
        return "⚖️ Netral"

def detect_impact(text):
    impact = []
    if any(k in text.lower() for k in ['fed', 'usd', 'eur', 'jpy', 'interest', 'rates', 'inflation']):
        impact.append("💱 Forex")
    if any(k in text.lower() for k in ['bitcoin', 'crypto', 'ethereum', 'blockchain']):
        impact.append("🪙 Crypto")
    if any(k in text.lower() for k in ['stocks', 'nasdaq', 's&p', 'dow', 'tesla', 'apple']):
        impact.append("📈 Saham")
    return impact if impact else ["❓ Tidak Diketahui"]

def format_time(t):
    try:
        dt = datetime.fromisoformat(t.replace("Z", "+00:00"))
        local_dt = dt.astimezone(pytz.timezone("Asia/Jakarta"))
        return local_dt.strftime("%d %b %Y, %H:%M WIB")
    except:
        return t

# ------------------------- MAIN CONTENT -------------------------
st.title("📰 Real-Time Market News")
st.markdown("Pantau berita **Forex, Crypto, dan Saham** secara real-time dari berbagai sumber terpercaya.")
st.divider()

news = get_newsapi_data()

if news:
    impact_counter = Counter()

    for item in news:
        impact = detect_impact(item['title'])
        sentiment = analyze_sentiment(item['title'])
        for i in impact:
            impact_counter[i] += 1

        impact_badges = " ".join([f'<span class="impact-badge">{i}</span>' for i in impact])
        st.markdown(f"""
            <div class="news-card">
                <div class="news-title">{item['title']}</div>
                <div class="news-meta">🕒 {format_time(item['time'])} | 📰 {item['source']}</div>
                <div>{impact_badges} <span class="sentiment-badge">{sentiment}</span></div>
                <a class="read-more" href="{item['url']}" target="_blank">🌐 Baca Selengkapnya</a>
            </div>
        """, unsafe_allow_html=True)

    # 📊 Grafik Dampak Harian
    st.markdown("### 📊 Dampak Berita Hari Ini")
    df_impact = pd.DataFrame({
        "Market": list(impact_counter.keys()),
        "Jumlah Berita": list(impact_counter.values())
    })
    fig = px.bar(df_impact, x="Market", y="Jumlah Berita", color="Market",
                 color_discrete_sequence=px.colors.qualitative.Pastel,
                 title="Jumlah Berita yang Berdampak ke Market Hari Ini")
    fig.update_layout(paper_bgcolor="white", plot_bgcolor="white")
    st.plotly_chart(fig, use_container_width=True)

else:
    st.error("❌ Gagal mengambil berita. Coba lagi nanti.")

st.markdown("</div>", unsafe_allow_html=True)
