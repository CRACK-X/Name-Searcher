from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
import time
import random

def setup_browser():
    options = Options()
    options.add_argument('--headless')  # Run in headless mode
    options.add_argument('--disable-gpu')
    options.add_argument('--no-sandbox')
    options.add_argument('--log-level=3')
    options.add_argument("user-agent=Mozilla/5.0")
    return webdriver.Chrome(options=options)

def search_person(name):
    sources = [
        # Search engines
        'https://www.google.com/search?q={}',
        'https://www.bing.com/search?q={}',

        # Social media
        'https://www.linkedin.com/search/results/people/?keywords={}',
        'https://www.facebook.com/search/top/?q={}',
        'https://twitter.com/search?q={}',
        'https://www.instagram.com/explore/tags/{}/',

        # Professional
        'https://www.indeed.com/jobs?q={}',
        'https://www.glassdoor.com/Search/results.htm?keyword={}',

        # Academic
        'https://www.google.com/search?q={}+site:researchgate.net',
        'https://www.google.com/search?q={}+site:pubmed.ncbi.nlm.nih.gov',

        # Gov / public records
        'https://www.google.com/search?q={}+site:gov',
        'https://www.google.com/search?q={}+site:publicrecords.com',

        # Forums
        'https://www.google.com/search?q={}+site:reddit.com',
        'https://www.google.com/search?q={}+site:stackoverflow.com'
    ]

    browser = setup_browser()
    results = []

    print(f"\n[+] Searching for: {name}\n")
    
    for url_template in sources:
        query_url = url_template.format(name.replace(' ', '+'))
        print(f"[.] Checking: {query_url}")

        try:
            browser.get(query_url)
            time.sleep(random.uniform(2, 4))  # avoid bot detection
            
            # Try to fetch title of the page
            title = browser.title
            print(f"    └─ Title: {title}")
            results.append({'url': query_url, 'title': title})
        except WebDriverException as e:
            print(f"    └─ Error: {e.msg}")

    browser.quit()

    if not results:
        print("\n[!] No data found.")
    else:
        print(f"\n[✓] {len(results)} sources responded successfully.")
    
    return results

# Example usage
if __name__ == "__main__":
    name = input("Enter the name to search: ")
    data = search_person(name)