import requests
from bs4 import BeautifulSoup
from datetime import datetime
import json

def fetch_reviews_from_g2(company_name, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"https://www.g2.com/products/{company_name}/reviews?page={page}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        breakpoint()
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            review_elements = soup.find_all('div', class_='review')
            if not review_elements:
                break  # No more reviews, exit the loop

            for review in review_elements:
                review_date = review.find('time')['datetime']
                review_date = datetime.strptime(review_date, '%Y-%m-%dT%H:%M:%S.%fZ')

                if start_date <= review_date <= end_date:
                    title = review.find('h3').text.strip()
                    description = review.find('p').text.strip()
                    reviewer = review.find('span', class_='reviewer-name').text.strip()
                    rating = review.find('span', class_='rating').text.strip()

                    reviews.append({
                        'title': title,
                        'description': description,
                        'date': review_date.strftime('%Y-%m-%d'),
                        'reviewer': reviewer,
                        'rating': rating
                    })

            page += 1  # Move to the next page
        else:
            print(f"Error fetching reviews from G2: {response.status_code}")
            break

    return reviews

def fetch_reviews_from_capterra(company_name, start_date, end_date):
    reviews = []
    page = 1

    while True:
        url = f"https://www.capterra.com/p/{company_name}/reviews?page={page}"
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')

            review_elements = soup.find_all('div', class_='review')
            if not review_elements:
                break  # No more reviews, exit the loop

            for review in review_elements:
                review_date = review.find('time')['datetime']
                review_date = datetime.strptime(review_date, '%Y-%m-%dT%H:%M:%S.%fZ')

                if start_date <= review_date <= end_date:
                    title = review.find('h3').text.strip()
                    description = review.find('p').text.strip()
                    reviewer = review.find('span', class_='reviewer-name').text.strip()
                    rating = review.find('span', class_='rating').text.strip()

                    reviews.append({
                        'title': title,
                        'description': description,
                        'date': review_date.strftime('%Y-%m-%d'),
                        'reviewer': reviewer,
                        'rating': rating
                    })

            page += 1  # Move to the next page
        else:
            print(f"Error fetching reviews from Capterra: {response.status_code}")
            break

    return reviews

def save_reviews_to_json(reviews, filename):
    with open(filename, 'w') as f:
        json.dump(reviews, f, indent=4)

def main():
    company_name = input("Enter company name (e.g., 'zoom'): ").strip().lower()
    start_date = input("Enter start date (YYYY-MM-DD): ").strip()
    end_date = input("Enter end date (YYYY-MM-DD): ").strip()

    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    source = input("Enter review source (G2 or Capterra): ").strip().lower()

    if source == 'g2':
        reviews = fetch_reviews_from_g2(company_name, start_date, end_date)
    elif source == 'capterra':
        reviews = fetch_reviews_from_capterra(company_name, start_date, end_date)
    else:
        print("Invalid source. Please enter 'G2' or 'Capterra'.")
        return

    if reviews:
        filename = f"{company_name}_{start_date.strftime('%Y%m%d')}_{end_date.strftime('%Y%m%d')}_{source}_reviews.json"
        save_reviews_to_json(reviews, filename)
        print(f"Reviews saved to {filename}")
    else:
        print("No reviews found for the specified criteria.")

if __name__ == "__main__":
    main()
