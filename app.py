import asyncio
import streamlit as st
import plotly.graph_objs as go
import streamlit.components.v1 as components
from deriv_api import DerivAPI
from newsapi import NewsApiClient
import datetime

# ===================== Config =====================
DERIV_APP_ID = 1089  # bisa diganti
NEWS_API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"
st.set_page_config(layout="wide", page_title="FiatLeak Clone", page_icon="🌐")

# ===================== Styles =====================
st.markdown("""
<style>
body, .stApp{background-color:#000;color:#00ffcc;}
.big{font-size:32px;font-weight:bold;color:#00ffcc !important;}
#bubble-container div{background:#00ffcc;}
.news{background:#111;padding:10px;border-radius:8px;margin:5px 0;}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1 class='big'>🌍 Market Flow & News (Real-time)</h1>", unsafe_allow_html=True)

# ===================== WebSocket Connection =====================
@st.experimental_singleton
def get_deriv_api():
    return DerivAPI(app_id=DERIV_APP_ID)

api = get_deriv_api()

# subscribe to ticks
async def subscribe_ticks(symbol, callback):
    await api.connect()
    await api.authorize({"authorize": ""})
    source = await api.subscribe({"ticks": symbol})
    async for tick in source:
        callback(tick["tick"]["quote"])

# placeholder
price_ph = st.empty()
chart_ph = st.empty()

price_data = []

# ===================== Bubble Animation =====================
def bubble_html():
    return """
    <div style="height:250px;position:relative;overflow:hidden">
    <script>
    setInterval(()=>{
      const b = document.createElement('div');
      const r = Math.random()*20+10;
      b.style.width=b.style.height=r+'px';
      b.style.left=Math.random()*100+'%';
      b.style.position='absolute';
      b.style.borderRadius='50%';
      b.style.top='100%';
      b.style.opacity=0.6;
      b.style.background='#00ffcc';
      b.style.animation='u 5s linear forwards';
      document.getElementById('bub').appendChild(b);
      setTimeout(()=>b.remove(),5000);
    },300);
    </script>
    <style>@keyframes u{0%{transform:translateY(0);}100%{transform:translateY(-500px);opacity:0;}}</style>
    <div id="bub" style="width:100%;height:100%;position:absolute;"></div>
    </div>
    """

components.html(bubble_html(), height=250)

# ===================== News API =====================
newsapi = NewsApiClient(api_key=NEWS_API_KEY)
def get_news():
    resp = newsapi.get_everything(q="forex OR crypto", language="en", sort_by="publishedAt", page_size=5)
    return resp["articles"]

# ===================== UI Controls =====================
pair = st.selectbox("Pilih Pair:", ["frxXAUUSD", "R_100", "frxEURUSD","frxUSDJPY"])
st.subheader("💱 Price & Chart")

# ===================== Async Ticks Handler =====================
def on_tick(q):
    price_data.append(q)
    if len(price_data)>30:
        price_data.pop(0)
    price_ph.metric(f"Harga {pair}", f"{q:.5f}")

    fig = go.Figure(go.Scatter(y=price_data, mode="lines+markers", name=pair))
    fig.update_layout(template="plotly_dark", height=300)
    chart_ph.plotly_chart(fig, use_container_width=True)

# start websocket listener
if 'ws_started' not in st.session_state:
    st.session_state.ws_started = True
    asyncio.run(subscribe_ticks(pair, on_tick))

# ===================== Show News =====================
st.subheader("📰 Berita Terkini")
for art in get_news():
    st.markdown(f"<div class='news'><b>{art['title']}</b><br>{art['description']}<br><a href='{art['url']}' style='color:#0ff;'>Baca selengkapnya</a></div>", unsafe_allow_html=True)
