from elasticsearch import Elasticsearch

# Initialize Elasticsearch instance
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme': 'http'}])

# Define index name
index_name = 'news_articles'

# Delete the index
if es.indices.exists(index=index_name):
    es.indices.delete(index=index_name)
    print(f"Index '{index_name}' deleted.")
else:
    print(f"Index '{index_name}' does not exist.")



#  from elasticsearch import Elasticsearch
# from collections import defaultdict

# es = Elasticsearch("http://localhost:9200")

# # Fetch all articles
# res = es.search(index="news_articles", body={"query": {"match_all": {}}}, size=1000)

# # Dictionary to store articles by unique title
# unique_articles = defaultdict(list)

# for hit in res['hits']['hits']:
#     article = hit['_source']
#     title = article['title']
    
#     # Add article to the unique dictionary (list to handle potential duplicates)
#     unique_articles[title].append(hit['_id'])

# # Now delete duplicates
# for article_list in unique_articles.values():
#     if len(article_list) > 1:
#         # Keep the first one, delete the rest
#         for duplicate_id in article_list[1:]:
#             es.delete(index="news_articles", id=duplicate_id)
