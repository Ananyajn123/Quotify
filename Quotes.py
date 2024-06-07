from pushbullet import Pushbullet
import random
import requests
from bs4 import BeautifulSoup

quotes = []
authors = []

def scrape_quotes(page):
    url = f"https://www.goodreads.com/quotes/tag/inspirational?page={page}"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")
    quote_blocks = soup.find_all('div', class_='quoteDetails')

    for block in quote_blocks:
        quote_text = block.find('div', class_='quoteText').text.strip().split('\n')[0].strip()
        quote_author = block.find('span', class_='authorOrTitle').text.strip()
        quotes.append(quote_text)
        authors.append(quote_author)

    print(f"Page {page} scraped: {len(quote_blocks)} quotes found.")

for page_num in range(1, 6):
    scrape_quotes(page_num)


API_KEY = 'o.ED3qydrqOawApvoGT7v5MG7yvDQC7ed2'  
pb = Pushbullet(API_KEY)

def send_daily_quote():
    if not quotes:
        print("No quotes available.")
        return

    random_index = random.randint(0, len(quotes) - 1)
    message = f"{quotes[random_index]}\n\n— {authors[random_index]}"
    push = pb.push_note("Quote Of The Day", message)
    print("Notification sent successfully.")

if __name__ == "__main__":
    send_daily_quote()
