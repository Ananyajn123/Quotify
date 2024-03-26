from pushbullet import Pushbullet
import random
import requests
from bs4 import BeautifulSoup
from apscheduler.schedulers.blocking import BlockingScheduler

authors = []
quotes = []

def scrape(page):
    page_num = str(page)
    url = "https://www.goodreads.com/quotes/tag/inspirational?page=" + page_num
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    quoteText = soup.find_all('div', attrs = {'class' : 'quoteText'})

    for i in quoteText:
        quote = i.text.strip().split('\n')[0]
        quoteAuthor = soup.find('span', attrs = {'class' : 'authorOrTitle'}).text.strip()
        quotes.append(quote)
        authors.append(quoteAuthor)

# Example: Determine the number of pages dynamically
url_first_page = "https://www.goodreads.com/quotes/tag/inspirational"
response_first_page = requests.get(url_first_page)
soup_first_page = BeautifulSoup(response_first_page.text, "html.parser")
next_page_link = soup_first_page.find("a", class_="next_page")
last_page_text = next_page_link.previous_sibling.get_text(strip=True) if next_page_link else '1'
last_page = int(last_page_text) if last_page_text else 1

for num in range(1, last_page + 1):
    scrape(num)



API_KEY = 'o.KyzcR9V7RSUyHll1Z8JmG7RlnTVvgQDC'
pb = Pushbullet(API_KEY)

def get_daily_quote():
    try:
        if not quotes:
            print("No quotes available")
            return
        random_num = random.randint(0,len(quotes) - 1)
        message = f"{quotes[random_num]}"
        push = pb.push_note('Quote Of The Day', message)
        # time.sleep(60)
    except Exception as e:
        print(f'Error: {e}')


scheduler = BlockingScheduler()
scheduler.add_job(get_daily_quote, 'cron', hour=20, minute=52)
scheduler.start()
# schedule.every().day.at("10:47").do(get_daily_quote)
#
# while True:
#     schedule.run_pending()
#     time.sleep(1)

# with open('text.txt','r') as f:
#     text = f.read()


