import streamlit as st
import plotly.graph_objs as go
import time
from deriv_ws import DerivWebSocket
import requests

st.set_page_config(layout="wide", page_title="FiatLeak Chart", page_icon="🌍")

st.markdown("""
<style>
body, .stApp {
    background-color: #000;
    color: #00ffcc;
}
.big {
    font-size: 30px;
    font-weight: bold;
    color: #00ffcc !important;
}
.news {
    background-color: #111;
    padding: 10px;
    border-radius: 8px;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<div class='big'>🌍 FiatLeak Style Real-Time Chart + News</div>", unsafe_allow_html=True)

# Bubble animation (FiatLeak style)
st.components.v1.html("""
<div style="height:200px;position:relative;overflow:hidden">
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
""", height=200)

pair = st.selectbox("Pilih Pair:", ["frxXAUUSD", "frxEURUSD", "frxUSDJPY", "R_100"])
dw = DerivWebSocket(symbol=pair)
dw.start()
chart = st.empty()
harga = st.empty()

prices = []

for _ in range(300):
    tick = dw.get_price()
    if tick:
        prices.append(tick)
        if len(prices) > 50:
            prices = prices[-50:]

        fig = go.Figure(go.Scatter(y=prices, mode="lines+markers"))
        fig.update_layout(template="plotly_dark", height=300, margin=dict(l=20, r=20, t=30, b=20))
        chart.plotly_chart(fig, use_container_width=True)
        harga.metric("Harga Sekarang", f"{tick:.2f}")
    time.sleep(1)

dw.stop()

# ===================== News ========================
st.markdown("### 📰 Berita Forex & Crypto")

API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"
url = f"https://newsapi.org/v2/everything?q=forex+OR+crypto&sortBy=publishedAt&language=en&pageSize=5&apiKey={API_KEY}"

try:
    res = requests.get(url)
    articles = res.json()["articles"]
    for news in articles:
        st.markdown(f"""
        <div class='news'>
            <b>{news['title']}</b><br>
            {news['description']}<br>
            <a href="{news['url']}" target="_blank" style="color:#00ffff">[Baca Selengkapnya]</a>
        </div>
        """, unsafe_allow_html=True)
except:
    st.warning("❌ Gagal mengambil berita.")
