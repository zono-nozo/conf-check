import requests
from bs4 import BeautifulSoup
import unicodedata
import sys
import re
import datetime

def fetch_html(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.content
    except requests.exceptions.Timeout:
        print("Request timed out. Please try again later.")
        raise ValueError("Request timed out.")
    except requests.exceptions.RequestException as e:
        print(f"Error occurred while fetching the URL: {e}")
        raise ValueError("Error occurred while fetching the URL.")

def extract_conference_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
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

    return conf_info

def parse_conference_dates(period_text):
    pattern = r"(\d+)年(\d+)月(\d+)日\(\w+\)~(\d+)日\(\w+\)"
    parse = re.search(pattern, period_text)

    if parse:
        year, month, start_day, end_day = parse.groups()
        start_date = datetime.date(int(year), int(month), int(start_day))
        end_date = datetime.date(int(year), int(month), int(end_day))
        return start_date, end_date
    else:
        raise ValueError("Date format not recognized.")

url = "https://www.ipsj.or.jp/event/taikai/89/index.html"

html_content = fetch_html(url)
conference_info = extract_conference_info(html_content)
start_date, end_date = parse_conference_dates(conference_info["大会会期"])