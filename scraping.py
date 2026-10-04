import requests

url = "https://www.ipsj.or.jp/event/taikai/89/index.html"
response = requests.get(url)
response.encoding = response.apparent_encoding
print(response.status_code)
print(response.text[:500])