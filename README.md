# Hybrid Search With Postgres & PgVector For RAG using Groq

This project demonstrates how to implement a hybrid search engine for Retrieval-Augmented Generation (RAG) using Postgres with PgVector. It showcases the use of asynchronous streaming with Groq's function calling capabilities in a FastAPI application.

![Postgres as a vector Database | Implementing Hybrid search with Postgres for RAG Using Groq.](./demo.png?raw=true "Demo")

## Description

This project utilizes Postgres as a vector database to create a hybrid search engine that combines vector search and text search capabilities. It leverages PgVector for storing and querying vector embeddings, and Groq's Large Language Model for function calling to retrieve information from the database through hybrid search.

## Technologies Used

![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-CC2927?style=for-the-badge&logo=sqlalchemy&logoColor=white)
![Groq](https://img.shields.io/badge/Groq-00ADD8?style=for-the-badge&logo=groq&logoColor=white)

## Features

- FastAPI-based implementation
- Hybrid search combining vector and text search capabilities
- Function calling for executing commands and retrieving information
- Chat interface for real-time communication
- Product search and recommendation system

## Getting Started

### Prerequisites

- Python 3.8 or higher
- PostgreSQL
- PgVector

### Dependencies

Refer to `requirements.txt` for a complete list of dependencies. Key dependencies include:

- FastAPI
- OpenAI API (for generating embeddings)
- Groq (for Large Language Model)
- SQLAlchemy
- PgVector

### Installation

1. Clone the repository
2. Create and activate a virtual environment
3. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

4. Install PostgreSQL:
   - For Ubuntu: `sudo apt-get install postgresql`
   - For macOS: `brew install postgresql`
   - For Windows: Download and install from the official PostgreSQL website

5. Create a database named `rag_example_schema`:
   ```
   psql -U postgres
   CREATE DATABASE rag_example_schema;
   ```

6. Enable the vector extension:
   ```
   \c rag_example_schema
   CREATE EXTENSION IF NOT EXISTS vector;
   \q
   ```

7. Set up environment variables:
   Create a `.env` file in the root directory and add the following variables:
   ```
   OPENAI_API_KEY=your_openai_api_key
   GROQ_API_KEY=your_groq_api_key
   DATABASE_NAME=rag_example_schema
   DATABASE_USER=your_database_user
   DATABASE_PASSWORD=your_database_password
   DATABASE_URL=localhost
   DATABASE_PORT=5432
   ```

8. Temporarily disable the index in `models/product.py`:
   Comment out the following lines:

   ```python:models/product.py
   # index_ada002 = Index(
   #     "hnsw_index_for_innerproduct_product_embedding_ada002",
   #     Product.embedding,
   #     postgresql_using="hnsw",
   #     postgresql_with={"m": 16, "ef_construction": 64},
   #     postgresql_ops={"embedding_ada002": "vector_ip_ops"},
   # )
   ```

9. Load initial data:
   ```
   python scripts/load_data.py
   ```

10. Re-enable the index in `models/product.py`:
    Uncomment the lines you commented in step 8:

    ```python:models/product.py
    index_ada002 = Index(
        "hnsw_index_for_innerproduct_product_embedding_ada002",
        Product.embedding,
        postgresql_using="hnsw",
        postgresql_with={"m": 16, "ef_construction": 64},
        postgresql_ops={"embedding_ada002": "vector_ip_ops"},
    )
    ```

11. Run the application:
    ```
    uvicorn main:app --reload
    ```

Your application should now be running at `http://localhost:8000`.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request with your changes.
