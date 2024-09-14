from flask import Flask, request, jsonify, render_template
from elasticsearch import Elasticsearch, NotFoundError
import requests
from bs4 import BeautifulSoup
import threading
import time
from datetime import datetime
from collections import defaultdict
import redis
import json
import os

# Initialize Flask app
app = Flask(__name__)

# Retrieve environment variables
REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = int(os.getenv('REDIS_PORT', 6379))
ES_HOST = os.getenv('ES_HOST', 'localhost')
ES_PORT = int(os.getenv('ES_PORT', 9200))

# Initialize Elasticsearch instance
es = Elasticsearch([{'host': ES_HOST, 'port': ES_PORT, 'scheme': 'http'}])

# Initialize Redis instance
cache = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0, decode_responses=True)

# Define index name
index_name = 'news_articles'
users = defaultdict(int)

# Create Elasticsearch index if it doesn't exist
def create_index():
    try:
        if not es.indices.exists(index=index_name):
            es.indices.create(index=index_name, ignore=400)
            print(f"Index '{index_name}' created.")
        else:
            print(f"Index '{index_name}' already exists.")
    except Exception as e:
        print(f"Error creating index: {e}")

create_index()

# Scrape function that will run in a background thread
def scrape_and_index():
    while True:
        print("Scraping news articles...")
        url = 'https://news.google.com/rss/search?q=flood'
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'xml')

        # Extract news articles
        for item in soup.find_all('item'):
            title = item.find('title').text
            link = item.find('link').text

            # Index document in Elasticsearch if not already present
            try:
                if not es.exists(index=index_name, id=link):
                    es.index(index=index_name, id=link, body={
                        'title': title,
                        'link': link
                    })
            except Exception as e:
                pass

        print("Scraping and indexing completed.")
        time.sleep(1800)  # 30 minutes

# Route for index.html
@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

# Health check endpoint
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "API is running (21BPS1141)"}), 200

# Search endpoint
@app.route('/search', methods=['POST'])
def search():
    user_id = request.form.get('user_id')
    if user_id is None:
        return jsonify({"error": "User ID is required"}), 400

    if user_id not in users:
        users[user_id] = 0
    
    if users[user_id] >= 5:
        return jsonify({"error": "Rate limit exceeded. Too Many Requests"}), 429
    
    users[user_id] += 1

    query_text = request.form.get('text', '')
    top_k = request.form.get('top_k', default=5, type=int)
    threshold = request.form.get('threshold', default=0.7, type=float)
    
    cache_key = f"{user_id}:{query_text}:{top_k}:{threshold}"

    cache_start_time = datetime.now()
    cached_result = cache.get(cache_key)
    cache_retrieval_time = (datetime.now() - cache_start_time).total_seconds()
    
    if cached_result:
        results = json.loads(cached_result)
        inference_time = cache_retrieval_time
    else:
        start_time = datetime.now()

        print(f"Request received: user_id={user_id}, query_text={query_text}, top_k={top_k}, threshold={threshold}")

        body = {
            "query": {
                "match": {
                    "title": query_text
                }
            },
            "size": top_k
        }
        
        try:
            res = es.search(index=index_name, body=body)
        except NotFoundError as e:
            print(f"Search error: {e}")
            return jsonify({"error": "Index not found"}), 404
        except Exception as e:
            print(f"Search error: {e}")
            return jsonify({"error": f"Search error: {e}"}), 500
        
        results = []
        for hit in res['hits']['hits']:
            if hit['_score'] >= threshold:
                if {
                    'title': hit['_source']['title'],
                    'link': hit['_source']['link'],
                    'score': hit['_score']
                } not in results:
                    results.append({
                        'title': hit['_source']['title'],
                        'link': hit['_source']['link'],
                        'score': hit['_score']
                    })
        
        cache.set(cache_key, json.dumps(results), ex=3600)  # Cache for 1 hour
        inference_time = (datetime.now() - start_time).total_seconds()
    
    return render_template('results.html', results=results, inference_time=inference_time, cache_retrieval_time=cache_retrieval_time if cached_result else None)

if __name__ == '__main__':
    scraper_thread = threading.Thread(target=scrape_and_index)
    scraper_thread.daemon = True
    scraper_thread.start()

    print("Starting Flask server...")
    app.run(debug=True, use_reloader=False)
