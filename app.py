import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from newsapi import NewsApiClient

# ===================== KONFIGURASI =====================
NEWS_API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"  # 🔑 Ganti dengan API key dari https://newsapi.org

# ===================== FUNGSI DETEKSI DAMPAK =====================
def detect_impact(text):
    text = text.lower()
    high_keywords = ['rate hike', 'war', 'conflict', 'inflation spike', 'oil surge', 'missile', 'attack', 'sanction', 'federal reserve', 'fomc']
    medium_keywords = ['inflation', 'geopolitical', 'unrest', 'protest', 'fed meeting', 'banking', 'data release', 'recession', 'interest rate']
    
    for word in high_keywords:
        if word in text:
            return "🚨 High"
    for word in medium_keywords:
        if word in text:
            return "⚠️ Medium"
    return "✅ Low"

# ===================== AMBIL BERITA =====================
def get_news(keyword="gold OR bitcoin"):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    all_articles = newsapi.get_everything(
        q=keyword,
        language="en",
        sort_by="publishedAt",
        page_size=10
    )
    return all_articles["articles"]

# ===================== SETUP UI =====================
st.set_page_config(page_title="TPM NEWS", layout="wide")

with st.sidebar:
    selected = option_menu(
        "Market Premium",
        ["📈 Chart Live", "📰 News Update"],
        icons=["bar-chart", "newspaper"],
        default_index=0,
        styles={
            "container": {"padding": "5px", "background-color": "#000022"},
            "icon": {"color": "#FFD700", "font-size": "20px"},
            "nav-link": {"color": "#FFFFFF", "font-size": "18px", "text-align": "left"},
            "nav-link-selected": {"background-color": "#FFD700", "color": "black"},
        },
    )

st.markdown("<style>body{background-color:#0f0f2f;}</style>", unsafe_allow_html=True)

# ===================== HALAMAN CHART =====================
if selected == "📈 Chart Live":
    st.title("📈 Real-Time Chart Gold & Bitcoin")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🪙 Bitcoin (BTC/USDT)")
        components.html("""
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=BINANCE:BTCUSDT&interval=5&theme=dark&style=1&locale=en&toolbar_bg=rgba(0,0,0,1)"
            width="100%" height="450" frameborder="0" allowfullscreen></iframe>
        """, height=450)

    with col2:
        st.subheader("🥇 Emas (XAU/USD)")
        components.html("""
            <iframe src="https://s.tradingview.com/widgetembed/?symbol=OANDA:XAUUSD&interval=5&theme=dark&style=1&locale=en&toolbar_bg=rgba(0,0,0,1)"
            width="100%" height="450" frameborder="0" allowfullscreen></iframe>
        """, height=450)

# ===================== HALAMAN BERITA =====================
elif selected == "📰 News Update":
    st.title("📰 News Feed: Gold, Bitcoin & Geopolitics")

    keyword = st.text_input("🔍 Search News:", value="gold OR bitcoin OR war OR inflation")
    if keyword:
        articles = get_news(keyword)
        for article in articles:
            title = article['title'].strip()
            url = article['url']
            published = article['publishedAt'][:10]
            source = article['source']['name']
            desc = article.get('description') or '*No description available*'
            image_url = article.get('urlToImage') or "https://via.placeholder.com/300x200.png?text=No+Image"

            # Bersihkan deskripsi
            desc_clean = desc.replace("The post", "").split("…")[0].strip()

            # Deteksi dampak berita
            impact = detect_impact(desc + " " + title)

            # Tampilkan dalam bentuk card thumbnail
            st.markdown(f"""
            <div style="border:1px solid #333;padding:15px;border-radius:10px;margin-bottom:15px;background-color:#1e1e2f;">
                <div style="display:flex;gap:15px;align-items:center;">
                    <img src="{image_url}" width="150" height="100" style="object-fit:cover;border-radius:8px;" />
                    <div style="flex:1">
                        <h4 style="margin-bottom:5px;"><a href="{url}" target="_blank" style="text-decoration:none;color:#FFD700;">{title}</a></h4>
                        <p style="font-size:14px;color:#AAAAAA;margin:0;">🕒 {published} • {source} • <b style="color:#00FFAA;">{impact} Impact</b></p>
                        <p style="font-size:15px;color:#DDDDDD;">{desc_clean}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
