import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from newsapi import NewsApiClient
from transformers import pipeline

# ===================== KONFIGURASI =====================
NEWS_API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"  # 🔑 Ganti dengan API key dari https://newsapi.org

# ===================== MODEL AI =====================
@st.cache_resource
def load_summarizer_translator():
    summarizer = pipeline("summarization", model="sshleifer/distilbart-cnn-12-6")
    translator = pipeline("translation", model="Helsinki-NLP/opus-mt-en-id")
    return summarizer, translator

summarizer, translator = load_summarizer_translator()

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
st.set_page_config(page_title="Market Premium AI", layout="wide")

with st.sidebar:
    selected = option_menu(
        "Market Premium",
        ["📈 Chart Live", "📰 News AI"],
        icons=["bar-chart", "robot"],
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
    st.title("📈 Real-Time Chart Emas & Bitcoin")

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
elif selected == "📰 News AI":
    st.title("📰 Berita Ekonomi & Geopolitik (dengan AI Ringkasan & Terjemahan)")

    keyword = st.text_input("🔍 Cari berita:", value="gold OR bitcoin OR war OR inflation OR geopolitics")
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
            desc = desc.replace("The post", "").split("…")[0].strip()

            # AI Summarizer & Translate
            try:
                summary = summarizer(desc, max_length=60, min_length=20, do_sample=False)[0]['summary_text']
                translation = translator(summary)[0]['translation_text']
            except:
                summary = desc
                translation = desc

            # Tampilkan dalam card
            st.markdown(f"""
            <div style="border:1px solid #333;padding:15px;border-radius:10px;margin-bottom:15px;background-color:#1e1e2f;">
                <div style="display:flex;gap:15px;align-items:center;">
                    <img src="{image_url}" width="150" height="100" style="object-fit:cover;border-radius:8px;" />
                    <div style="flex:1">
                        <h4 style="margin-bottom:5px;"><a href="{url}" target="_blank" style="text-decoration:none;color:#FFD700;">{title}</a></h4>
                        <p style="font-size:14px;color:#AAAAAA;margin:0;">🕒 {published} • {source}</p>
                        <p style="font-size:15px;color:#DDDDDD;margin-top:8px;"><b>Ringkasan AI 🇮🇩:</b> {translation}</p>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
