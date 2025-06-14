import streamlit as st
import websocket
import json
import threading
import time
import requests
import plotly.graph_objs as go
import streamlit.components.v1 as components

st.set_page_config(layout="wide", page_title="FiatLeak Realtime", page_icon="🌍")

# 1. Tampilan mirip FiatLeak
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

st.markdown("<div class='big'>🌍 FiatLeak Style Market Monitor</div>", unsafe_allow_html=True)

# 2. Bubble effect mirip fiatleak
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

# 3. Real-time price dari WebSocket Deriv
selected_pair = st.selectbox("Pilih Pair:", ["frxXAUUSD", "frxEURUSD", "frxUSDJPY", "R_100"])
latest_price_placeholder = st.empty()
chart_placeholder = st.empty()

price_data = []

def on_message(ws, message):
    global price_data
    data = json.loads(message)
    if "tick" in data:
        price = data["tick"]["quote"]
        price_data.append(price)
        if len(price_data) > 50:
            price_data.pop(0)
        latest_price_placeholder.metric(f"Harga {selected_pair}", f"{price:.2f}")
        fig = go.Figure(go.Scatter(y=price_data, mode='lines+markers'))
        fig.update_layout(template="plotly_dark", height=300)
        chart_placeholder.plotly_chart(fig, use_container_width=True)

def on_open(ws):
    sub_msg = json.dumps({"ticks": selected_pair})
    ws.send(sub_msg)

def run_websocket():
    ws = websocket.WebSocketApp(
        "wss://ws.derivws.com/websockets/v3?app_id=1089",
        on_open=on_open,
        on_message=on_message
    )
    ws.run_forever()

# Jalankan WebSocket di thread terpisah
if 'ws_thread_started' not in st.session_state:
    st.session_state.ws_thread_started = True
    threading.Thread(target=run_websocket, daemon=True).start()

# 4. Berita real-time
st.markdown("### 📰 Berita Terkini")
API_KEY = "fadb8f16daaf4ad3baa0aa710051d8f1"

def fetch_news():
    try:
        url = f"https://newsapi.org/v2/everything?q=forex+OR+crypto&sortBy=publishedAt&language=en&apiKey={API_KEY}"
        r = requests.get(url)
        articles = r.json().get("articles", [])
        return articles[:5]
    except:
        return []

news = fetch_news()
for item in news:
    st.markdown(f"""
    <div class='news'>
        <b>{item['title']}</b><br>
        {item['description']}<br>
        <a href="{item['url']}" target="_blank" style="color:#00ffff">[Baca Selengkapnya]</a>
    </div>
    """, unsafe_allow_html=True)
