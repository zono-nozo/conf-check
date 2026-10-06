import requests
from bs4 import BeautifulSoup
import unicodedata
import sys

url = "https://www.ipsj.or.jp/event/taikai/89/index.html"

try:
    response = requests.get(url, timeout=10)

    response.raise_for_status()

except requests.exceptions.Timeout:
    print("Request timed out. Please try again later.")
    sys.exit(1)

except requests.exceptions.RequestException as e:
    print(f"Error occurred while fetching the URL: {e}")
    sys.exit(1)

soup = BeautifulSoup(response.content, "html.parser")

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
            