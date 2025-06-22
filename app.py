import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from newsapi import NewsApiClient

# Konfigurasi API
NEWS_API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

# Fungsi ambil berita
def get_news(keyword="emas"):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    all_articles = newsapi.get_everything(q=keyword, language="id", sort_by="publishedAt", page_size=10)
    return all_articles["articles"]

# Setup UI
st.set_page_config(page_title="Dashboard Emas & Kripto", layout="wide")

with st.sidebar:
    selected = option_menu(
        "Dashboard 1Miliar", 
        ["📈 Chart Live", "📰 Berita Terkini"], 
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

# Halaman Chart Live
if selected == "📈 Chart Live":
    st.title("📈 Live Chart Emas & Bitcoin (TradingView)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🪙 Bitcoin (BTCUSD)")
        components.html("""
            <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=BINANCE:BTCUSDT&width=100%&height=400&locale=en&dateRange=1D&colorTheme=dark&isTransparent=false&autosize=true"
            width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
        """, height=400)

    with col2:
        st.subheader("🥇 Emas (XAUUSD)")
        components.html("""
            <iframe src="https://s.tradingview.com/embed-widget/mini-symbol-overview/?symbol=OANDA:XAUUSD&width=100%&height=400&locale=en&dateRange=1D&colorTheme=dark&isTransparent=false&autosize=true"
            width="100%" height="400" frameborder="0" allowtransparency="true" scrolling="no"></iframe>
        """, height=400)

# Halaman Berita
elif selected == "📰 Berita Terkini":
    st.title("📰 Berita Ekonomi & Kripto Hari Ini")

    keyword = st.text_input("🔍 Cari berita:", value="emas OR bitcoin OR geopolitik")
    if keyword:
        articles = get_news(keyword)
        for article in articles:
            st.markdown(f"""
            ### [{article['title']}]({article['url']})
            ⏱️ {article['publishedAt'][:10]} | 🏷️ {article['source']['name']}  
            {article['description'] or ''}
            ---
            """)
