import streamlit as st
import random
import requests
import plotly.graph_objs as go
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="FiatLeak Clone", page_icon="🌐")

# CSS Kustom untuk tema gelap mirip fiatleak
st.markdown("""
    <style>
    body, .stApp {
        background-color: #000;
        color: #00ffcc;
    }
    .big-font {
        font-size:30px !important;
        font-weight:bold;
        color: #00ffcc;
    }
    .news-block {
        background-color: #111;
        padding: 10px;
        border-radius: 10px;
        margin-bottom: 10px;
    }
    </style>
""", unsafe_allow_html=True)

st.markdown('<p class="big-font">🌍 Real-Time Market Flow & News</p>', unsafe_allow_html=True)

# Dummy price update (real API bisa diganti Deriv/Binance WebSocket)
def get_realtime_price(pair):
    if "XAU" in pair:
        return round(random.uniform(1800, 2200), 2)
    elif "BTC" in pair:
        return round(random.uniform(30000, 70000), 2)
    elif "ETH" in pair:
        return round(random.uniform(1500, 4000), 2)
    else:
        return round(random.uniform(1.0, 1.5), 4)

# Real-time Bubble Animation HTML
def render_bubble_animation(pair):
    html_code = f"""
    <div style="height:400px; background:black; position:relative; overflow:hidden;">
        <script>
        function createBubble() {{
            const bubble = document.createElement("div");
            bubble.style.width = bubble.style.height = Math.random() * 20 + 10 + "px";
            bubble.style.background = "#00ffcc";
            bubble.style.position = "absolute";
            bubble.style.borderRadius = "50%";
            bubble.style.left = Math.random() * 100 + "%";
            bubble.style.top = "100%";
            bubble.style.opacity = 0.6;
            bubble.style.animation = "moveUp 5s linear forwards";
            document.getElementById("bubble-container").appendChild(bubble);
            setTimeout(() => bubble.remove(), 5000);
        }}

        setInterval(createBubble, 300);

        </script>
        <style>
            @keyframes moveUp {{
                0% {{ transform: translateY(0); }}
                100% {{ transform: translateY(-500px); opacity: 0; }}
            }}
        </style>
        <div id="bubble-container" style="width:100%; height:100%; position:relative;"></div>
    </div>
    """
    components.html(html_code, height=400)

# Fetch berita
def fetch_news():
    API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"
    url = f"https://newsapi.org/v2/everything?q=forex+OR+crypto&sortBy=publishedAt&language=en&apiKey={API_KEY}"
    try:
        r = requests.get(url)
        articles = r.json().get("articles", [])
        return articles[:5]
    except:
        return []

# UI Layout
col1, col2 = st.columns(2)
with col1:
    selected_pair = st.selectbox("Pilih Pair", ["XAUUSD", "BTCUSD", "ETHUSD", "EURUSD", "USDJPY"])
with col2:
    latest_price = get_realtime_price(selected_pair)
    st.metric(label=f"Harga {selected_pair}", value=latest_price)

# Bubble Visual
render_bubble_animation(selected_pair)

# Chart (Dummy Line Chart)
st.markdown("### 📈 Pergerakan Harga")
prices = [get_realtime_price(selected_pair) for _ in range(30)]
fig = go.Figure(go.Scatter(y=prices, mode='lines+markers', name=selected_pair))
fig.update_layout(height=300, template="plotly_dark")
st.plotly_chart(fig, use_container_width=True)

# News Section
st.markdown("### 📰 Berita Market Terkini")
news = fetch_news()
if news:
    for item in news:
        st.markdown(f"""
        <div class="news-block">
        <b>{item['title']}</b><br>
        {item['description']}<br>
        <a href="{item['url']}" style="color:#00ffff" target="_blank">[Baca Selengkapnya]</a>
        </div>
        """, unsafe_allow_html=True)
else:
    st.info("Berita tidak tersedia sekarang.")

