from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
from datetime import datetime
import time
import os

# 🧠 크롬 브라우저 설정
options = Options()
# options.add_argument('--headless')  # 필요 시 창 없이 실행
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--no-sandbox')

# ✅ 크롬 드라이버 실행
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# 🔗 AICT 게시판 접속
url = "https://aict.snu.ac.kr/?p=92"
driver.get(url)

# ⏳ 게시물 로딩 대기
WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((By.CSS_SELECTOR, ".gallery_list li"))
)

# 🌐 HTML 추출
html = driver.page_source
soup = BeautifulSoup(html, "html.parser")

# ✅ 최신 게시물 5개 가져오기
posts = soup.select(".gallery_list li")[:5]

rss_items = ""
now = datetime.now().strftime("%a, %d %b %Y %H:%M:%S +0900")

for post in posts:
    title_tag = post.select_one("span.title a")
    title = title_tag.text.strip()
    
    # 🔗 링크 정확히 조합하기
    raw_link = title_tag["href"]
    if raw_link.startswith("http"):
        link = raw_link
    else:
        link = "https://aict.snu.ac.kr" + raw_link

    # 🖼️ 썸네일 추출
    img_tag = post.select_one("span.photo img")
    thumbnail_url = "https://aict.snu.ac.kr" + img_tag["src"] if img_tag else ""

    rss_items += f"""
  <item>
    <title>{title}</title>
    <link>{link}</link>
    <pubDate>{now}</pubDate>
    <description><![CDATA[
      <img src="{thumbnail_url}" width="500"><br>
      <a href="{link}">{title}</a>
    ]]></description>
  </item>
"""

# 🧾 전체 RSS XML 만들기
rss = f"""<?xml version="1.0" encoding="UTF-8" ?>
<rss version="2.0">
<channel>
  <title>AICT 게시판 최신 5개</title>
  <link>{url}</link>
  <description>AICT 최근 게시글 5개를 자동으로 보여주는 RSS</description>
  <lastBuildDate>{now}</lastBuildDate>
{rss_items}
</channel>
</rss>"""

# 📁 바탕화면 > 김수아 폴더 경로
feed_path = r"C:\Users\박정민\Desktop\김수아\feed.xml"
debug_path = r"C:\Users\박정민\Desktop\김수아\debug.html"

# 💾 저장
try:
    with open(feed_path, "w", encoding="utf-8") as f:
        f.write(rss)
    print("✅ feed.xml 저장 완료!")
except Exception as e:
    print("❌ feed.xml 저장 에러:", e)

try:
    with open(debug_path, "w", encoding="utf-8") as f:
        f.write(html)
    print("✅ debug.html 저장 완료!")
except Exception as e:
    print("❌ debug.html 저장 에러:", e)

driver.quit()
print("✅ 전체 작업 완료! 최신 게시물 정보가 feed.xml에 저장됨.")
