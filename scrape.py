from bs4 import BeautifulSoup
import requests
import sys
from openai import OpenAI
import os
from config import config
import json
from readability import Document

# Initialize the OpenAI client with your API key
client = OpenAI(api_key=config.openai_api_key)


#TODO: Добавить функцию для скрейпинга страницы и сохранения в файл
def scrape_website(url):
    # Add headers to mimic a browser request
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Referer': 'https://www.google.com/',
        'DNT': '1',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # Raise an exception for HTTP errors
        return response.text  # Return raw HTML string
    except requests.exceptions.RequestException as e:
        print(f"Error fetching the URL {url}: {e}")
        return None

def extract_text_from_html(html):
    if html is None:
        return ""  # Return empty string if HTML is None
    doc = Document(html)  # Pass raw HTML string
    main_content = doc.summary()  # Extracts main body text as HTML
    soup = BeautifulSoup(main_content, 'lxml')
    return soup.get_text().strip()  # Return cleaned text

def save_text_to_file(text, filename):
    try:
        with open(filename, "w", encoding="utf-8") as f:  # Added encoding
            f.write(text)
        print(f"Saved text to {filename}")
    except Exception as e:
        print(f"Error saving to {filename}: {e}")

if __name__ == "__main__":
    # Load URL list from JSON
    try:
        with open("url_list.json", "r") as f:
            url_list = json.load(f)
    except FileNotFoundError:
        print("url_list.json not found!")
        sys.exit(1)
    except json.JSONDecodeError:
        print("Invalid JSON in url_list.json!")
        sys.exit(1)

    # Process each university and its URLs
    for university in url_list:
        for i, url in enumerate(url_list[university]):
            print(f"Scraping {url} for {university}...")
            html = scrape_website(url)
            text = extract_text_from_html(html)
            # Use a unique filename per URL to avoid overwriting
            #filename = f"{university}_{i}.txt"

            #University files should be combined together
            with open(f"{university}.txt", "a") as f:
                f.write(text)

            #save_text_to_file(text, filename)