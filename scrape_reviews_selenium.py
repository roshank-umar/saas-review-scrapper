import time
import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

def scrape_g2_reviews(company_slug, max_pages=2, start_date=None, end_date=None):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    # service = Service(executable_path="PATH_TO_CHROMEDRIVER")  # 🔁 Replace path
    driver = webdriver.Chrome( options=chrome_options)

    all_reviews = []

    for page in range(1, max_pages + 1):
        url = f"https://www.g2.com/products/{company_slug}/reviews?page={page}"
        driver.get(url)
        time.sleep(3)

        soup = BeautifulSoup(driver.page_source, "html.parser")
        review_blocks = soup.find_all("div", class_="paper__bd")

        for block in review_blocks:
            try:
                reviewer = block.find(attrs={"itemprop": "author"}).get_text(strip=True)
                date_str = block.find(attrs={"itemprop": "datePublished"})["content"]
                date = datetime.strptime(date_str, "%Y-%m-%d")
                if start_date and end_date and not (start_date <= date <= end_date):
                    continue

                rating = block.find("span", class_="screen-reader-only").get_text(strip=True)
                review = block.find(attrs={"itemprop": "reviewBody"}).get_text(strip=True)

                all_reviews.append({
                    "reviewer": reviewer,
                    "date": date.strftime('%Y-%m-%d'),
                    "rating": rating,
                    "review": review
                })
            except Exception as e:
                print("G2 parsing error:", e)

    driver.quit()
    return all_reviews

def scrape_capterra_reviews(capterra_url, max_pages=2, start_date=None, end_date=None):
    headers = {'User-Agent': 'Mozilla/5.0'}
    all_reviews = []

    for page in range(1, max_pages + 1):
        url = f"{capterra_url}?page={page}"
        response = requests.get(url, headers=headers)
        breakpoint()
        if response.status_code != 200:
            print(f"Failed to load Capterra page {page}")
            continue

        soup = BeautifulSoup(response.text, 'lxml')
        review_blocks = soup.find_all('div', class_='reviewCard')
        breakpoint()

        for block in review_blocks:
            try:
                reviewer = block.find('span', class_='user-name').get_text(strip=True)
                date_str = block.find('div', class_='review-date').get_text(strip=True)
                date = datetime.strptime(date_str, '%B %d, %Y')
                if start_date and end_date and not (start_date <= date <= end_date):
                    continue

                rating = block.find('span', class_='capterra-rating-number').text.strip()
                review = block.find('p', class_='review-body').get_text(strip=True)

                all_reviews.append({
                    "reviewer": reviewer,
                    "date": date.strftime('%Y-%m-%d'),
                    "rating": rating,
                    "review": review
                })
            except Exception as e:
                print("Capterra parsing error:", e)

    return all_reviews

def save_reviews(reviews, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(reviews, f, indent=4, ensure_ascii=False)
    print(f"✅ Saved {len(reviews)} reviews to {filename}")

def main():
    company = input("Enter company slug (for G2): ").strip().lower()  # e.g. "hubspot-operations-hub"
    source = input("Enter source (g2/capterra): ").strip().lower()
    start = input("Enter start date (YYYY-MM-DD): ")
    end = input("Enter end date (YYYY-MM-DD): ")
    start_date = datetime.strptime(start, "%Y-%m-%d")
    end_date = datetime.strptime(end, "%Y-%m-%d")

    if source == "g2":
        reviews = scrape_g2_reviews(company, start_date=start_date, end_date=end_date)
        filename = f"{company}_g2_reviews.json"
    elif source == "capterra":
        capterra_url = input("Enter full Capterra product reviews URL: ").strip()
        reviews = scrape_capterra_reviews(capterra_url, start_date=start_date, end_date=end_date)
        filename = f"{company}_capterra_reviews.json"
    else:
        print("❌ Invalid source. Use 'g2' or 'capterra'.")
        return

    save_reviews(reviews, filename)

if __name__ == "__main__":
    main()
