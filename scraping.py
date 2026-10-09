import connect_db

import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import datetime

def fetch_html(url):
    response = requests.get(url, timeout=10)
    response.raise_for_status()
    return response.content

def extract_conference_info(html_content):
    soup = BeautifulSoup(html_content, "html.parser")
    h3 = soup.find("h3", string="開催概要")
    if not h3:
        raise ValueError("Could not find the '開催概要' section in the HTML content.")
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
        if start_date > end_date:
            raise ValueError("Start date is after end date.")
        return start_date, end_date
    else:
        raise ValueError("Date format not recognized.")

with connect_db.connect_to_db() as connection:
    rows = connect_db.get_conferences_to_check(connection)

    for conference_id, url in rows:
        try:
            html_content = fetch_html(url)
            conference_info = extract_conference_info(html_content)
            start_date, end_date = parse_conference_dates(conference_info["大会会期"])
        except requests.RequestException as e:
            print(f"Error fetching the URL: {e}")
            continue
        except ValueError as e:
            print(f"Error processing the conference information: {e}")
            continue
        
        connect_db.update_conference_dates(connection, conference_id, start_date, end_date)