import requests
from bs4 import BeautifulSoup

url = "https://www.ipsj.or.jp/event/taikai/89/index.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")

h3 = soup.find("h3", string="開催概要")
target = h3.find_next("p")

print(response.status_code)
print(target.text)