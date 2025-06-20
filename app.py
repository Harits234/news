import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

st.set_page_config(page_title="Berita Kompas AI", layout="wide")
st.title("📰 AI Berita Kompas - Otomatis & Terupdate")

keyword = st.text_input("🔍 Kata kunci berita (Contoh: ekonomi, jokowi, bursa)", "ekonomi")

def summarize(text):
    blob = TextBlob(text)
    return ". ".join(blob.sentences[:2])

def scrape_kompas(keyword):
    search_url = f"https://www.kompas.com/search?q={keyword}"
    headers = {"User-Agent": "Mozilla/5.0"}
    res = requests.get(search_url, headers=headers)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.find_all("div", class_="article__list", limit=5)
    results = []

    for art in articles:
        try:
            a = art.find("a", class_="article__link")
            title = a.get_text(strip=True)
            link = a["href"]
            article_page = requests.get(link, headers=headers)
            article_soup = BeautifulSoup(article_page.text, "html.parser")
            content = " ".join(p.get_text() for p in article_soup.find_all("p") if len(p.get_text()) > 50)
            if content:
                summary = summarize(content)
                results.append({"title": title, "link": link, "summary": summary})
        except:
            continue
    return results

if keyword:
    news = scrape_kompas(keyword)
    if not news:
        st.warning("Berita tidak ditemukan. Coba kata kunci lain.")
    for item in news:
        st.subheader(item['title'])
        st.write(item['summary'])
        st.markdown(f"[🔗 Baca Selengkapnya]({item['link']})")
        st.markdown("---")
