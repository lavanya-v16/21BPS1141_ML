import requests
from bs4 import BeautifulSoup
from elasticsearch import Elasticsearch

# Initialize Elasticsearch instance
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme':'http'}])

# Define index name
index_name = 'news_articles'

def scrape_and_index():
    print("Scraping news articles...")
    url = 'https://news.google.com/rss/search?q=lockdown'
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    
    # Extract news articles
    for item in soup.find_all('item'):
        title = item.find('title').text
        link = item.find('link').text

        # Index document in Elasticsearch
        es.index(index=index_name, body={
            'title': title,
            'link': link
        })

    print("Scraping and indexing completed.")

if __name__ == '__main__':
    scrape_and_index()
