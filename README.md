Web-Aware RAG Engine

This project implements a simplified version of a scalable, web-aware Retrieval-Augmented Generation (RAG) engine.
It ingests web content asynchronously, stores metadata in a local database, and allows querying over the processed text.
The implementation avoids Docker, Redis, and Qdrant to keep it lightweight and easy to run locally.

Objectives

The goal of this project is to demonstrate understanding of:

Asynchronous ingestion workflows

Background task handling

Metadata management in a relational database

Text embedding and retrieval logic

Scalable API architecture patterns

Design Overview


Components

FastAPI: Handles API endpoints for ingestion and querying.

SQLite: Stores ingestion metadata and processing results.

SQLAlchemy: ORM layer for database interactions.

Requests: Downloads and extracts web content.

Threading: Provides asynchronous behavior without external queues.

Custom embedding logic: Simulates text vectorization using a simple TF-IDF-like approach.

File Descriptions

main.py — Contains all FastAPI endpoints and background thread logic.

db.py — Defines database schema and manages connection setup.

embedding.py — Implements lightweight text embedding functions.

requirements.txt — Lists minimal dependencies needed to run the project.

Installation Instructions

Clone this repository:

git clone <your_repo_url>
cd rag-engine-simple


Create a virtual environment (optional but recommended):

python -m venv venv
venv\Scripts\activate         # on Windows
source venv/bin/activate      # on Linux/macOS


Install required dependencies:

pip install fastapi uvicorn sqlalchemy requests


Run the application:

uvicorn main:app --reload


Open your browser and visit:

http://127.0.0.1:8000/docs

API Endpoints
1. POST /ingest-url

Submit a webpage URL for background ingestion and processing.

Example request:

{
  "url": "https://example.com"
}


Example response:

{
  "ingestion_id": "3c6460d5-6a01-4d6a-a2e3-d96b6a41b9f2",
  "status": "PENDING"
}

2. GET /ingestion/{ingestion_id}

Check the ingestion status and view metadata.

Example response:

{
  "id": "3c6460d5-6a01-4d6a-a2e3-d96b6a41b9f2",
  "url": "https://example.com",
  "status": "COMPLETED",
  "submitted_at": "2025-10-24T12:10:15",
  "completed_at": "2025-10-24T12:10:20",
  "error": null
}

3. POST /query

Submit a text query over the stored content (simulated).

Example request:

{
  "query": "What is this article about?"
}


Example response:

{
  "answer": "Query received: What is this article about?",
  "total_docs": 1
}

How It Works

A user submits a URL using /ingest-url.
The API immediately returns a unique ingestion ID with status PENDING.

In the background, a separate thread:

Downloads the webpage content.

Extracts readable text.

Generates a basic numerical embedding.

Updates the status in the SQLite database to COMPLETED.

The user can check the status anytime using /ingestion/{id}.

Once the ingestion is complete, queries can be made to simulate RAG-style retrieval.

Example Usage

Run the app:

uvicorn main:app --reload


Open the interactive API documentation:

http://127.0.0.1:8000/docs


Submit a URL via /ingest-url:

{
  "url": "https://example.com"
}


Copy the ingestion_id from the response and check:

GET /ingestion/<ingestion_id>


Once the status is COMPLETED, try a query:

{
  "query": "Summarize the content."
}

Database Schema

The metadata is stored in a single SQLite table called ingestions.

Column	Type	Description
id	String	Unique UUID for each ingestion
url	Text	Source webpage URL
status	Enum	PENDING / PROCESSING / COMPLETED / FAILED
submitted_at	Timestamp	Time of initial request
completed_at	Timestamp	Time of completion
error	Text	Error message (if any)
Scalability and Extensions

To scale this project into a production-grade RAG system:

Replace the thread-based worker with a message queue (e.g., Redis, RQ, or Celery).

Use a true embedding model (e.g., OpenAI or Sentence Transformers).

Store vectors in a proper vector database (e.g., Qdrant, FAISS, or Chroma).

Add caching, pagination, and authentication layers.

Containerize the project using Docker and compose multiple workers.

Summary

This simplified version focuses on clarity and local usability while retaining the structure of a scalable RAG pipeline.
It can be easily extended to include real embeddings, retrieval systems, and distributed workers.

Author

Developed as part of a recruitment challenge to demonstrate understanding of scalable RAG architecture design, asynchronous API development, and practical system implementation.

