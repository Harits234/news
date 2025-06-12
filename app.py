import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Fungsi scraping dari Investing.com
def get_investing_news():
    url = "https://www.investing.com/news/"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    news_list = []

    for article in soup.select(".textDiv"):
        title_elem = article.select_one("a.title")
        time_elem = article.select_one(".date")
        if title_elem and time_elem:
            title = title_elem.get_text(strip=True)
            link = "https://www.investing.com" + title_elem["href"]
            time_posted = time_elem.get_text(strip=True)
            news_list.append({"Source": "Investing", "Title": title, "Time": time_posted, "Link": link})
    return news_list

# Fungsi scraping dari FXStreet
def get_fxstreet_news():
    url = "https://www.fxstreet.com/news"
    headers = {'User-Agent': 'Mozilla/5.0'}
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")
    news_list = []

    for article in soup.select("div.news-item"):
        title_elem = article.select_one("a")
        time_elem = article.select_one("span.date")
        if title_elem and time_elem:
            title = title_elem.get_text(strip=True)
            link = "https://www.fxstreet.com" + title_elem["href"]
            time_posted = time_elem.get_text(strip=True)
            news_list.append({"Source": "FXStreet", "Title": title, "Time": time_posted, "Link": link})
    return news_list

# Fungsi ambil berita Crypto dari API
def get_cryptopanic_news():
    url = "https://cryptopanic.com/api/v1/posts/?auth_token=demo&public=true"
    r = requests.get(url)
    if r.status_code != 200:
        return []
    data = r.json()
    news_list = []
    for item in data.get("results", []):
        news_list.append({
            "Source": "CryptoPanic",
            "Title": item["title"],
            "Time": item["published_at"],
            "Link": item["url"]
        })
    return news_list

# Setup Streamlit
st.set_page_config(page_title="Real-Time News Feed", layout="wide")
st.title("📰 Real-Time Market News")
st.markdown("Pantau berita *Forex*, *Saham*, dan *Crypto* terbaru dari berbagai sumber terpercaya.")

# Pilihan kategori
category = st.selectbox("📊 Pilih kategori berita:", ["Semua", "Forex", "Saham", "Crypto"])
if st.button("🔄 Refresh Berita"):
    with st.spinner("Mengambil berita terbaru..."):
        all_news = []
        if category in ["Semua", "Forex", "Saham"]:
            all_news.extend(get_investing_news())
            all_news.extend(get_fxstreet_news())
        if category in ["Semua", "Crypto"]:
            all_news.extend(get_cryptopanic_news())

        if all_news:
            df = pd.DataFrame(all_news)
            for idx, row in df.iterrows():
                st.markdown(f"### {row['Title']}")
                st.markdown(f"🕒 {row['Time']} | 📰 {row['Source']}")
                st.markdown(f"[🌐 Baca Selengkapnya]({row['Link']})", unsafe_allow_html=True)
                st.markdown("---")
        else:
            st.warning("❌ Gagal mengambil berita. Coba lagi nanti.")
