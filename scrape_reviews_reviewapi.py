import requests
import json
from datetime import datetime

def fetch_reviews(company, start_date, end_date, source):
    api_key = 'your_api_key_here'
    url = f'https://api.reviewapi.io/v1/reviews?company={company}&start_date={start_date}&end_date={end_date}&source={source}&api_key={api_key}'
    
    response = requests.get(url)
    if response.status_code == 200:
        reviews = response.json()
        return reviews
    else:
        print(f"Error fetching reviews: {response.status_code}")
        return []

def save_reviews_to_json(reviews, filename):
    with open(filename, 'w') as file:
        json.dump(reviews, file, indent=4)

if __name__ == "__main__":
    company = input("Enter company name: ")
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    source = input("Enter review source (G2, Capterra, or Third-Party): ").lower()

    reviews = fetch_reviews(company, start_date, end_date, source)
    if reviews:
        filename = f"{company}_{start_date}_{end_date}_{source}_reviews.json"
        save_reviews_to_json(reviews, filename)
        print(f"Reviews saved to {filename}")
    else:
        print("No reviews found.")
