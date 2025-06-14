import streamlit as st
import plotly.graph_objs as go
import websocket
import json
import threading
import time
import requests

st.set_page_config(layout="wide", page_title="FiatLeak Real-Time", page_icon="🌍")

# ===== Styling ala FiatLeak ====
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

# ===== Bubble animasi ====
st.components.v1.html("""
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
""", height=250)

# ======= User pilih pair =======
pair = st.selectbox("Pilih Pair:", ["frxXAUUSD", "frxEURUSD", "frxUSDJPY", "R_100"])

# ====== Tempat tampil data ======
price_box = st.empty()
chart_box = st.empty()

price_data = []

# ====== WebSocket Handler ======
def on_message(ws, message):
    global price_data
    data = json.loads(message)
    if "tick" in data:
        price = data["tick"]["quote"]
        price_data.append(price)
        if len(price_data) > 50:
            price_data = price_data[-50:]

        # Update Streamlit
        price_box.metric(f"Harga {pair}", f"{price:.2f}")
        fig = go.Figure()
        fig.add_trace(go.Scatter(y=price_data, mode="lines+markers", name=pair))
        fig.update_layout(template="plotly_dark", height=300, margin=dict(l=20, r=20, t=30, b=20))
        chart_box.plotly_chart(fig, use_container_width=True)

def on_open(ws):
    ws.send(json.dumps({"ticks": pair}))

def run_ws():
    ws = websocket.WebSocketApp(
        "wss://ws.derivws.com/websockets/v3?app_id=1089",
        on_message=on_message,
        on_open=on_open
    )
    ws.run_forever()

# Jalankan WebSocket cuma sekali
if 'ws_started' not in st.session_state:
    st.session_state.ws_started = True
    threading.Thread(target=run_ws, daemon=True).start()

# ======== News Bagian =========
st.markdown("### 📰 Berita Forex & Crypto")
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

def fetch_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=forex+OR+crypto&sortBy=publishedAt&language=en&pageSize=5&apiKey={API_KEY}"
        res = requests.get(url)
        articles = res.json().get("articles", [])
        return articles
    except:
        return []

for news in fetch_news():
    st.markdown(f"""
    <div class='news'>
        <b>{news['title']}</b><br>
        {news['description']}<br>
        <a href="{news['url']}" target="_blank" style="color:#00ffff">[Baca Selengkapnya]</a>
    </div>
    """, unsafe_allow_html=True)
