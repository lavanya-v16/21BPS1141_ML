from elasticsearch import Elasticsearch

# Initialize Elasticsearch instance
es = Elasticsearch([{'host': 'localhost', 'port': 9200, 'scheme':'http'}])

# Define index name
index_name = 'news_articles'

# Create index function
def create_index():
    if not es.indices.exists(index=index_name):
        es.indices.create(index=index_name, ignore=400)
        print(f"Index '{index_name}' created.")
    else:
        print(f"Index '{index_name}' already exists.")

if __name__ == '__main__':
    create_index()
