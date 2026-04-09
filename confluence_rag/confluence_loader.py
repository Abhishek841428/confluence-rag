import os
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv

load_dotenv()

BASE_URL = os.getenv("CONFLUENCE_BASE_URL")
EMAIL = os.getenv("CONFLUENCE_EMAIL")
API_TOKEN = os.getenv("CONFLUENCE_API_TOKEN")
SPACE_KEY = os.getenv("CONFLUENCE_SPACE_KEY")


def fetch_pages(limit=50):
    if not all([BASE_URL, EMAIL, API_TOKEN, SPACE_KEY]):
        raise EnvironmentError(
            "Missing one or more environment variables: CONFLUENCE_BASE_URL, CONFLUENCE_EMAIL, CONFLUENCE_API_TOKEN, CONFLUENCE_SPACE_KEY"
        )

    url = f"{BASE_URL.rstrip('/')}/rest/api/content"
    params = {
        "spaceKey": SPACE_KEY,
        "expand": "body.storage,title",
        "limit": limit
    }

    response = requests.get(url, auth=(EMAIL, API_TOKEN), params=params)
    response.raise_for_status()
    data = response.json()

    pages = []
    for page in data.get("results", []):
        html = page.get("body", {}).get("storage", {}).get("value", "")
        title = page.get("title", "Untitled")
        text = clean_html(html)

        pages.append({
            "title": title,
            "text": text
        })

    return pages


def clean_html(html):
    soup = BeautifulSoup(html, "html.parser")
    return soup.get_text(separator=" ")