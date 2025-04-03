from bs4 import BeautifulSoup

with open("feed.xml", "r", encoding="utf-8") as f:
    soup = BeautifulSoup(f, "xml")

items = soup.find_all("item")[:5]

cards = ""

for item in items:
    title = item.title.text
    link = item.link.text
    img = BeautifulSoup(item.description.text, "html.parser").find("img")["src"]

    cards += f'''
    <a href="{link}" target="_blank" style="text-decoration: none; color: black; width: 100px; text-align: center;">
      <img src="{img}" width="100" height="80" style="object-fit: cover; border-radius: 4px;">
      <div style="font-size: 11px; margin-top: 4px;">{title}</div>
    </a>
    '''

html = f"""
<!DOCTYPE html>
<html>
<head><meta charset="utf-8"></head>
<body>
<div style="display: flex; gap: 10px; font-family: sans-serif;">
  {cards}
</div>
</body>
</html>
"""

with open("latest.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✅ latest.html 생성 완료!")

