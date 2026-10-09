import connect_db

import requests
from bs4 import BeautifulSoup
import unicodedata
import re
import datetime

DATES = "大会会期"
LOCATION = "会場"

REQUIRED_KEYS = [DATES, LOCATION]

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

    conference_info = {}
    for text in texts:
        parts = text.split(":", 1)
        if len(parts) == 2:
            key, value = parts
            key = key.replace(' ', '')
            value = value.strip()
            if key in REQUIRED_KEYS:
                conference_info[key] = value

    missing_keys = [key for key in REQUIRED_KEYS if key not in conference_info]
    if missing_keys:
        raise ValueError(f"Required information missing for keys: {missing_keys}")

    return conference_info

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
    
def main():
    with connect_db.connect_to_db() as connection:
        rows = connect_db.get_conferences_to_check(connection)

        for conference_id, url in rows:
            try:
                html_content = fetch_html(url)
                conference_info = extract_conference_info(html_content)
                
                location = conference_info[LOCATION]
                start_date, end_date = parse_conference_dates(conference_info[DATES])

            except requests.RequestException as e:
                print(f"Error fetching the URL: {e}")
                continue

            except ValueError as e:
                print(f"Error processing the conference information: {e}")
                continue
            
            connect_db.update_conference_info(connection, conference_id, location, start_date, end_date)

if __name__ == "__main__":
    main()