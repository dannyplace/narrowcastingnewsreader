import requests
from bs4 import BeautifulSoup
import threading
import re

from flask import Flask, render_template

app = Flask(__name__)

# Initialize the news items list
news_items = []

def fetch_rss_feed():
    global news_items
    
    # Retrieve news items from RSS feed
    url = 'https://www.nu.nl/rss/algemeen'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, features='xml')

    items = soup.find_all('item')[:5]

    # Update the news items list
    news_items.clear()
    for item in items:
        title = item.title.text
        description = item.description.text
        # Strip <a> tags from description and show them as plain text
        description = re.sub(r'<a.*?>(.*?)<\/a>', r'\1', description)
        description = re.sub(r'<em.*?>(.*?)<\/em>', r'\1', description)
        image_url = item.enclosure['url'].replace('256', '1024') if item.enclosure else None
        news_items.append({'title': title, 'description': description, 'image_url': image_url})

    # Schedule the next fetch
    threading.Timer(120, fetch_rss_feed).start()

# Schedule the first fetch
fetch_rss_feed()

# Index of the current news item being displayed
current_index = 0

@app.route('/')
def home():
    global current_index 

    # Get the current news item
    news_item = news_items[current_index]

    # Increment the current index or wrap around to the beginning if at the end
    current_index = (current_index + 1) % len(news_items)

    return render_template('index.html', news_item=news_item)

if __name__ == '__main__':
    app.run(debug=True)