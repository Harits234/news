import streamlit as st
from streamlit_option_menu import option_menu
import streamlit.components.v1 as components
from newsapi import NewsApiClient

# Konfigurasi API Key
NEWS_API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"  # ← Ganti dengan key dari newsapi.org

# Fungsi ambil berita dari NewsAPI
def get_news(keyword="gold OR bitcoin"):
    newsapi = NewsApiClient(api_key=NEWS_API_KEY)
    all_articles = newsapi.get_everything(
        q=keyword,
        language="en",
        sort_by="publishedAt",
        page_size=10
    )
    return all_articles["articles"]

# Setup halaman utama
st.set_page_config(page_title="Market Insight Premium", layout="wide")

with st.sidebar:
    selected = option_menu(
        "Market Insight",
        ["📊 Chart Live", "📰 News Update"],
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

# === CHART PAGE ===
if selected == "📊 Chart Live":
    st.title("📈 Real-Time Market Chart (TradingView)")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Bitcoin (BTC/USDT)")
        components.html("""
            <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_f2df5&symbol=BINANCE:BTCUSDT&interval=5&theme=dark&style=1&locale=en&toolbar_bg=rgba(0,0,0,1)&enable_publishing=false&hide_top_toolbar=false&hide_legend=false&save_image=false&studies=[]"
            width="100%" height="450" frameborder="0" allowfullscreen></iframe>
        """, height=450)

    with col2:
        st.subheader("Gold (XAU/USD)")
        components.html("""
            <iframe src="https://s.tradingview.com/widgetembed/?frameElementId=tradingview_f2df5&symbol=OANDA:XAUUSD&interval=5&theme=dark&style=1&locale=en&toolbar_bg=rgba(0,0,0,1)&enable_publishing=false&hide_top_toolbar=false&hide_legend=false&save_image=false&studies=[]"
            width="100%" height="450" frameborder="0" allowfullscreen></iframe>
        """, height=450)

# === NEWS PAGE ===
elif selected == "📰 News Update":
    st.title("📰 News Feed: Gold, Bitcoin & Geopolitics")

    keyword = st.text_input("🔍 Search News:", value="gold OR bitcoin OR geopolitics OR war OR inflation")
    if keyword:
        articles = get_news(keyword)
        for article in articles:
            st.markdown(f"""
            ---
            ### [{article['title']}]({article['url']})
            ⏱️ `{article['publishedAt'][:10]} • {article['source']['name']}`  
            {article['description'] or '*No description available*'}
            """)
