from flask import Flask, request, jsonify
from elasticsearch import Elasticsearch
import requests
from bs4 import BeautifulSoup
import threading
import time

# Initialize Flask app
app = Flask(__name__)

# Initialize Elasticsearch instance
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme':'http'}])

# Define index name
index_name = 'news_articles'

# Create Elasticsearch index if it doesn't exist
def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, ignore=400)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

create_index()

# Scrape function that will run in a background thread
def scrape_and_index():
    while True:
        print("Scraping news articles...")
        url = 'https://news.google.com/rss/search?q=lockdown'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')
        
        # Extract news articlesF
        for item in soup.find_all('item'):
            title = item.find('title').text
            link = item.find('link').text

            # Index document in Elasticsearch
            es.index(index=index_name, body={
                'title': title,
                'link': link
            })

        print("Scraping and indexing completed.")
        
        # Sleep for 4 hours before scraping again
        time.sleep(14400)  # 4 hours = 14400 seconds

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return "API is running!"

# Run the Flask server
if __name__ == '__main__':
    # Start the background thread for scraping
    scraper_thread = threading.Thread(target=scrape_and_index)
    scraper_thread.start()
    
    # Start the Flask server
    app.run(debug=True)
