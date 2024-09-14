# **Document Retrieval System**

## Description

The Document Retrieval System is a backend application built to retrieve and manage documents efficiently. The application is designed using Python and Flask,
and it integrates various components such as Elasticsearch for indexing, Redis for caching, and a background thread for scraping news articles.
It provides API endpoints for health checks and document retrieval, with built-in user request tracking and rate limiting.

## Features

- **Document Retrieval:** Retrieve relevant documents based on user queries.
- **Caching:** Utilizes Redis for caching search results to improve performance.
- **Background Scraping:** Periodic scraping of news articles to keep the document index up-to-date.
- **API Endpoints:** Health check and search functionality with request tracking and rate limiting.

## Overall Architecture
![Frontend](https://github.com/user-attachments/assets/32d60574-3638-4649-88a0-1e075c94b042)

## Database Used
Elasticsearch is an analytical engine developed on Java that is open sourced. It enables it to handle vast amounts of data quickly and in near real-time, delivering search responses in milliseconds.
Unlike traditional structured databases that uses tables and schemas, elasticsearch is a document- based model that provides more flexibility and efficiency for file handling. As elasticsearch provides powerful
indexing capabilities and easy of dealing with text documents, it was preferred over other databases for this project. Its ability to quickly process and retrieve large volumes of documents is crucial for ensuring 
fast and accurate responses to user queries.
![Elasticsearch101-Picture_(9)](https://github.com/user-attachments/assets/4f532de1-94ca-4fde-92fb-dd010b5e6ebd)

## Caching technique Used
**Caching Method:** Redis
Redis is used for caching search results due to its high performance and support for in-memory data storage. It provides fast data access and is well-suited for caching search results, which helps in reducing the load 
on Elasticsearch and improving overall application performance.
#### Query run time before caching:
![WhatsApp Image 2024-09-14 at 10 47 02 PM](https://github.com/user-attachments/assets/ab069bff-894e-4442-abf7-e0dc637d8c4a)

#### Query run time after caching:
![WhatsApp Image 2024-09-14 at 11 09 58 PM](https://github.com/user-attachments/assets/6154e20e-861f-4353-93fe-0de1a6178031)


## Background Scraping

The application includes a background thread that starts when the server boots up. This thread periodically scrapes news articles every half an hour and updates the Elasticsearch index. This process utilizes
BeautifulSoup, a powerful Python library for web scraping and updating news articles in the Elasticsearch index.
### Scrapped articles stored as JSON in elasticsearch db:
![WhatsApp Image 2024-09-14 at 11 13 08 PM](https://github.com/user-attachments/assets/e84d4286-fe8e-49f7-aad4-734bead58400)

## API Endpoints:
## 1) **'/'**

**Method:** GET

**Description:** Serves the main landing page of the Document Retrieval System application. This page is intended to provide users with a starting point for interacting with the system, providing option to perform searches and view results.

**Response:** Returns the HTML content of the index.html file. This file is designed to provide a user-friendly interface for interacting with the backend API.
![WhatsApp Image 2024-09-14 at 11 18 51 PM](https://github.com/user-attachments/assets/813f3f88-7f91-4da8-976b-9ad175500950)

## 2) **'/health'**

**Method:** GET

**Description:** Returns a random response to check if the API is active.

**Response:** {"status": "API is running (21BPS1141)"}

![WhatsApp Image 2024-09-14 at 11 16 25 PM](https://github.com/user-attachments/assets/0300aaef-1e2b-41e0-8206-787c075d54a9)


## 3) **'/search'**

**Method:** GET

**Description:** Retrieves a list of top results based on the query.

**Parameters:**

  
text (required): The search query text.
  
  top_k (optional, default: 5): Number of top results to return.
  
  threshold (optional, default: 0.5): Minimum similarity score for results.
  
  user_id (required): Unique identifier for the user making the request.
  
  Response: JSON object containing the search results and inference time.
  
  ![WhatsApp Image 2024-09-14 at 11 09 58 PM](https://github.com/user-attachments/assets/6154e20e-861f-4353-93fe-0de1a6178031)

**Rate Limiting:**

If a user makes more than 5 requests, they will receive an HTTP 429 status code indicating that the rate limit has been exceeded. This helps prevent abuse and ensures fair usage of the service.
![WhatsApp Image 2024-09-14 at 11 28 23 PM](https://github.com/user-attachments/assets/a4b74e19-b714-4abf-b30e-a5fc779a048f)


# Installation Guide
## Step 1: Clone the Repository
Start by cloning the repository to your local machine using Git.
'git clone https://github.com/your-username/your-repo.git'
Navigate into the project directory: cd your-repo

## Step 2: Set Up a Virtual Environment (Optional but Recommended)
python -m venv venv
venv\Scripts\activate

## Step 3: Install Dependencies
pip install -r requirements.txt

## Step 4: Configure Environment Variables
ELASTICSEARCH_URL=http://localhost:9200

## Step 5: Run the Application
python app.py
The application will now be running on http://localhost:5000/
