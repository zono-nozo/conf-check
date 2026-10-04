import requests
from bs4 import BeautifulSoup
import unicodedata

url = "https://www.ipsj.or.jp/event/taikai/89/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

print(response.status_code)

h3 = soup.find("h3", string="開催概要")
target = h3.find_next("p")

normalized_text = unicodedata.normalize("NFKC", target.text)

texts = normalized_text.splitlines()

conf_info = {}

for text in texts:
    parts = text.split(":", 1)
    if len(parts) == 2:
        key, value = parts
        key = key.replace(' ', '')
        value = value.strip()
        if key == "大会会期" or key == "会場":
            conf_info[key] = value
            