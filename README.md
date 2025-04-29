# saas-review-scrapper
SaaS Product Review Scraper
This Python script allows you to scrape product reviews from G2 and Capterra  or 3rd Party (Review API) for a specific company and date range. The collected reviews are saved in a structured JSON format.

🚀 Features
Scrapes reviews from G2 or Capterra

Filters reviews based on a start date and end date

Extracts important fields: title, description, date, reviewer, and rating

Saves the results in a JSON file

🧰 Requirements
Before running the script, install the necessary Python packages:

bash
Copy
Edit
pip install requests beautifulsoup4 lxml selenium
⚙️ Usage
Run the script using:

bash
Copy
Edit
python scrape_reviews.py
python scrape_reviews_selenium.py (Review using selenium)
python scrape_reviews_reviewapi.py (Review using third party)
You will be prompted to input:

Company Name: The company/product as it appears in the URL (e.g., hubspot-crm for https://www.g2.com/products/hubspot-crm/reviews)

Start Date: In the format YYYY-MM-DD

End Date: In the format YYYY-MM-DD

Source: Either G2 or Capterra

Example:

bash
Copy
Edit
Enter company name: hubspot-crm
Enter start date (YYYY-MM-DD): 2024-01-01
Enter end date (YYYY-MM-DD): 2024-12-31
Enter review source (G2 or Capterra): g2
If reviews are found, they will be saved to a file like:

pgsql
Copy
Edit
hubspot-crm_20240101_20241231_g2_reviews.json
📁 Output
Each review in the JSON file will look like:

json
Copy
Edit
{
  "title": "Great CRM tool!",
  "description": "HubSpot makes it easy to manage leads and track deals.",
  "date": "2024-03-12",
  "reviewer": "Jane D.",
  "rating": "5"
}
📝 Notes
The script uses basic HTML parsing, so it may break if the structure of G2 or Capterra changes.

It does not use official APIs—so scraping is subject to public website limitations and may be blocked or rate-limited.

Always make sure your use complies with the terms of service of the sites you're scraping.

📬 Feedback
If you run into issues or want to improve the script, feel free to contribute or open an issue!
