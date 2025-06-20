import streamlit as st
import requests
from bs4 import BeautifulSoup
from textblob import TextBlob

st.set_page_config(page_title="Berita Otomatis AI", layout="wide")
st.title("📰 AI Scraper Multi-Sumber Berita Indonesia")

keyword = st.text_input("🔍 Kata kunci berita yang dicari:", "ekonomi")
max_berita = st.slider("Jumlah berita per sumber:", 1, 10, 5)

def clean_text(text):
    return ' '.join(text.strip().split())

def summarize(text):
    blob = TextBlob(text)
    return ". ".join(blob.sentences[:2])

def scrape_kompas(keyword, max_items):
    url = f"https://www.kompas.com/tag/{keyword}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.find_all("article", limit=max_items)
    results = []
    for art in articles:
        try:
            a = art.find("a")
            title = clean_text(a.get_text())
            link = a["href"]
            page = requests.get(link)
            page_soup = BeautifulSoup(page.text, "html.parser")
            content = " ".join(p.get_text() for p in page_soup.find_all("p") if len(p.get_text()) > 50)
            summary = summarize(content)
            results.append({"title": title, "link": link, "summary": summary})
        except:
            continue
    return results

def scrape_cnbc(keyword, max_items):
    url = "https://www.cnbcindonesia.com/news"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    articles = soup.find_all("article", limit=20)
    results = []
    count = 0
    for art in articles:
        try:
            a = art.find("a")
            title = clean_text(a.get_text())
            link = a["href"]
            if keyword.lower() in title.lower() and count < max_items:
                page = requests.get(link)
                page_soup = BeautifulSoup(page.text, "html.parser")
                content = " ".join(p.get_text() for p in page_soup.find_all("p") if len(p.get_text()) > 50)
                summary = summarize(content)
                results.append({"title": title, "link": link, "summary": summary})
                count += 1
        except:
            continue
    return results

def scrape_detik(keyword, max_items):
    url = f"https://news.detik.com/indeks?tag={keyword}"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select("article a[href^='https']")
    results = []
    for a in links[:max_items]:
        try:
            link = a["href"]
            title = clean_text(a.get_text())
            page = requests.get(link)
            page_soup = BeautifulSoup(page.text, "html.parser")
            paragraphs = page_soup.find_all("p")
            content = " ".join(p.get_text() for p in paragraphs if len(p.get_text()) > 50)
            summary = summarize(content)
            results.append({"title": title, "link": link, "summary": summary})
        except:
            continue
    return results

if keyword:
    st.subheader("📡 Kompas")
    for item in scrape_kompas(keyword, max_berita):
        st.markdown(f"### {item['title']}")
        st.write(item['summary'])
        st.markdown(f"[Baca Selengkapnya]({item['link']})")
        st.markdown("---")

    st.subheader("📡 CNBC Indonesia")
    for item in scrape_cnbc(keyword, max_berita):
        st.markdown(f"### {item['title']}")
        st.write(item['summary'])
        st.markdown(f"[Baca Selengkapnya]({item['link']})")
        st.markdown("---")

    st.subheader("📡 Detik")
    for item in scrape_detik(keyword, max_berita):
        st.markdown(f"### {item['title']}")
        st.write(item['summary'])
        st.markdown(f"[Baca Selengkapnya]({item['link']})")
        st.markdown("---")
