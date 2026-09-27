# Zepto Data & AI Platform — Capstone Project

An end-to-end Data Engineering, Analytics & Machine Learning, and GenAI Support Assistant project organized into three connected modules.

## Repository

GitHub: https://github.com/vishwagnakummari-jpg/Zepto-Data-AI-Platform

---

## Project Architecture & Reading Order

The project is organized as a single integrated platform:

### 1. `/data_pipeline` — Module 1: Data Engineering Pipeline

Transforms raw scraped catalog data into clean, normalized relational data and validates it using SQLite, SQL, and Pandas.

**Main areas:**
- Web scraping
- Data cleaning and transformation
- Fixed-rate currency conversion
- SQLite relational database
- SQL validation
- Pandas validation

[View Module 1 README](./data_pipeline/README.md)

### 2. `/analytics` — Module 2: Analytics & Predictive Modeling

Performs exploratory data analysis and machine learning using the Titanic dataset.

**Main areas:**
- Data profiling and cleaning
- Outlier and correlation analysis
- Classification
- Class-imbalance handling
- Random Forest hyperparameter tuning
- Fare regression
- Complete ML pipeline serialization

[View Module 2 README](./analytics/README.md)

### 3. `/support_assistant` — Module 3: GenAI Policy Support Assistant

Implements a local RAG-based customer support assistant grounded in Zepto policy documents.

**Main areas:**
- Policy document ingestion
- Local Sentence Transformer embeddings
- ChromaDB retrieval
- LangGraph workflow
- Structured Pydantic responses
- FastAPI `/ask` endpoint
- Docker support
- Deterministic `MOCK_LLM=1` execution

[View Module 3 README](./support_assistant/README.md)

---

## Overall Architecture

```text
                    Zepto Data & AI Platform
                             |
             +---------------+---------------+
             |               |               |
             v               v               v
      Data Pipeline      Analytics      Support Assistant
             |               |               |
        Web Scraping     Titanic Data    Policy Documents
             |               |               |
       Data Cleaning        EDA          Embeddings
             |               |               |
          SQLite        ML Models       ChromaDB
             |               |               |
        SQL/Pandas       Joblib          LangGraph
                                             |
                                          FastAPI