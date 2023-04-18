import requests
from bs4 import BeautifulSoup

from flask import Flask, render_template

app = Flask(__name__)

# Retrieve news items from RSS feed
url = 'https://www.nu.nl/rss/algemeen'
response = requests.get(url)
soup = BeautifulSoup(response.content, features='xml')

items = soup.find_all('item')[:5]

news_items = []
for item in items:
    title = item.title.text
    description = item.description.text
    image_url = item.enclosure['url'].replace('256', '1024') if item.enclosure else None
    news_items.append({'title': title, 'description': description, 'image_url': image_url})

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