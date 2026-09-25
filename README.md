# Zepto Data & AI Platform — Capstone Project

Welcome! This capstone project is an end-to-end AI/ML platform structured into three connected modules: **Data Engineering, Analytics & Predictive Modeling, and a GenAI Policy Support Assistant**.

---

## 🧭 Project Architecture & Recommended Reading Order

The project is designed as a connected workflow:

### 1. 📂 [Data Pipeline](./data_pipeline/) — Module 1: Data Engineering Pipeline

Transforms raw scraped catalog data into clean, normalized data and stores it in a SQLite relational database.

**Key areas:**

* Web scraping
* Data cleaning
* Data transformation
* Currency conversion
* SQLite database creation
* SQL queries
* Pandas analysis

### 2. 📂 [Analytics](./analytics/) — Module 2: Analytics & Predictive Modeling

Performs exploratory data analysis and machine learning using the Titanic dataset.

**Key areas:**

* Exploratory Data Analysis
* Data preprocessing
* Classification
* Model evaluation
* Imbalance handling
* SMOTE
* Random Forest
* GridSearchCV
* Regression
* ML pipeline serialization

### 3. 📂 [Support Assistant](./support_assistant/) — Module 3: GenAI Policy Support Assistant

Provides a local RAG-based customer support system using Zepto policy documents.

**Key areas:**

* Local embeddings
* Sentence Transformers
* ChromaDB
* LangGraph
* Structured prompting
* Pydantic
* FastAPI
* Docker

---

# 📌 Project Overview

The project demonstrates an end-to-end data and AI workflow:

```text
Raw Data
   ↓
Data Engineering
   ↓
Clean Structured Data
   ↓
Analytics & Machine Learning
   ↓
AI / RAG Support Assistant
   ↓
FastAPI + Docker
```

The three modules demonstrate different stages of a practical AI/ML platform:

* **Data Engineering** — collecting, cleaning, transforming, and storing data.
* **Data Analytics & Machine Learning** — exploring data, training models, evaluating performance, and creating reusable ML pipelines.
* **Generative AI / RAG** — retrieving relevant policy information and generating policy-grounded customer-support responses.

---

# 🗂️ Repository Structure

```text
zepto-data-ai-platform/
│
├── README.md
├── requirements.txt
├── .gitignore
│
├── data_pipeline/
│   ├── README.md
│   ├── pipeline.py
│   └── zepto_store.db
│
├── analytics/
│   ├── README.md
│   ├── 01_eda.ipynb
│   ├── 02_modeling.ipynb
│   ├── titanic.csv
│   └── best_pipeline.joblib
│
└── support_assistant/
    ├── README.md
    ├── Dockerfile
    ├── main.py
    ├── rag_graph.py
    ├── prompt_template.py
    │
    └── docs/
        ├── doc_01.txt
        ├── doc_02.txt
        ├── doc_03.txt
        ├── doc_04.txt
        ├── doc_05.txt
        ├── doc_06.txt
        ├── doc_07.txt
        └── doc_08.txt
```

---

# 🛠️ Technologies Used

## Programming

* Python

## Data Engineering

* Requests
* BeautifulSoup
* Pandas
* SQLite

## Data Analysis

* Pandas
* NumPy
* Matplotlib
* Seaborn

## Machine Learning

* Scikit-learn
* Imbalanced-learn
* Logistic Regression
* Decision Tree
* Random Forest
* GridSearchCV
* SMOTE

## Generative AI / RAG

* Sentence Transformers
* `all-MiniLM-L6-v2`
* ChromaDB
* LangGraph
* LangChain Core
* Pydantic

## API & Deployment

* FastAPI
* Uvicorn
* Docker

## Model Serialization

* Joblib

---

# 📂 Module 1 — Data Engineering Pipeline

## Objective

The data engineering module converts raw catalog data into clean and structured relational data.

## Workflow

```text
Books to Scrape
      ↓
Web Scraping
      ↓
Data Cleaning
      ↓
Price & Rating Processing
      ↓
Currency Conversion
      ↓
SQLite Database
      ↓
SQL Queries
      ↓
Pandas / SQL Analysis
```

## Key Tasks

* Scrape product/book catalog data.
* Clean prices and ratings.
* Process availability information.
* Convert GBP prices to INR using the project's fixed conversion rate.
* Store processed data in SQLite.
* Create relational tables.
* Execute SQL queries.
* Compare SQL results with equivalent Pandas operations.

## Main Files

```text
data_pipeline/
├── pipeline.py
├── zepto_store.db
└── README.md
```

📖 **Detailed documentation:** [Data Pipeline README](./data_pipeline/README.md)

---

# 📊 Module 2 — Analytics & Predictive Modeling

## Objective

The analytics module performs exploratory data analysis and develops machine learning models using the Titanic dataset.

## Workflow

```text
Titanic Dataset
      ↓
Data Exploration
      ↓
Data Preprocessing
      ↓
Train/Test Split
      ↓
Classification Models
      ↓
Model Evaluation
      ↓
Imbalance Handling
      ↓
Hyperparameter Tuning
      ↓
Regression Side Task
      ↓
Complete ML Pipeline
      ↓
Joblib Serialization
```

## Classification Models

The project evaluates:

* Logistic Regression
* Decision Tree
* Random Forest

Evaluation metrics include:

* Accuracy
* Precision
* Recall
* F1 Score
* ROC-AUC

## Imbalance Handling

The project compares:

* Baseline Random Forest
* Random Forest with balanced class weights
* Random Forest with SMOTE applied only to the training data

## Hyperparameter Tuning

Random Forest hyperparameters are tuned using:

```text
GridSearchCV
```

The tuning process evaluates:

* Number of estimators
* Maximum tree depth
* Maximum features

The tuned Random Forest also uses an OOB score.

## Regression Side Task

A Linear Regression model is used to predict passenger fare.

Evaluation metrics include:

* MAE
* RMSE
* R²
* Adjusted R²

## Model Serialization

The complete preprocessing and machine learning pipeline is saved as:

```text
best_pipeline.joblib
```

The saved pipeline can be reloaded and used with raw input data.

## Main Files

```text
analytics/
├── 01_eda.ipynb
├── 02_modeling.ipynb
├── titanic.csv
├── best_pipeline.joblib
└── README.md
```

📖 **Detailed documentation:** [Analytics README](./analytics/README.md)

---

# 🤖 Module 3 — GenAI Policy Support Assistant

## Objective

The support assistant is a local RAG-based customer support system that answers questions using a fixed set of Zepto policy documents.

## Technologies

* Sentence Transformers
* `all-MiniLM-L6-v2`
* ChromaDB
* LangGraph
* Pydantic
* FastAPI
* Docker

## RAG Architecture

```text
Policy Documents
      ↓
Document Ingestion
      ↓
Sentence Transformer
(all-MiniLM-L6-v2)
      ↓
Vector Embeddings
      ↓
ChromaDB
      ↓
Cosine Similarity Retrieval
      ↓
Top-3 Relevant Documents
      ↓
LangGraph
      ↓
Structured Response
      ↓
FastAPI
```

## Policy Documents

The system uses eight policy documents:

```text
doc_01.txt — Delivery Policy
doc_02.txt — Returns & Refunds
doc_03.txt — Membership Tiers
doc_04.txt — Order Tracking
doc_05.txt — Order Cancellation Policy
doc_06.txt — Damaged or Missing Items
doc_07.txt — Gift Cards
doc_08.txt — Customer Support Hours
```

## LangGraph Workflow

The graph contains three named nodes:

```text
                  ┌── retrieve_and_answer
                  │
classify_intent ──┤
                  │
                  └── direct_answer
```

### `classify_intent`

Classifies the incoming query as:

* `policy_question`
* `general_question`

The mock classifier checks policy-related keywords including:

```text
delivery
return
refund
membership
tracking
cancel
gift card
support hours
```

### `retrieve_and_answer`

For policy questions:

1. Queries ChromaDB.
2. Retrieves the top 3 relevant documents.
3. Uses cosine similarity.
4. Generates the deterministic mock response.
5. Returns retrieved document IDs as sources.

### `direct_answer`

For general questions, the mock system returns:

```text
I can only answer questions about Zepto policies right now.
```

---

# 🧩 Structured Prompt

The RAG prompt contains:

* Role
* Context
* Task
* Format
* Length
* Negative constraint
* Few-shot example

The prompt instructs the assistant to answer using only the supplied policy context.

The prompt is stored in:

```text
support_assistant/prompt_template.py
```

---

# 🔒 Mock LLM Mode

The application supports deterministic mock mode:

```text
MOCK_LLM=1
```

Mock mode is enabled by default.

This allows the support assistant to run locally without requiring a paid external LLM API.

For policy questions:

```text
Based on the retrieved context: <retrieved policy snippet>
```

For general questions:

```text
I can only answer questions about Zepto policies right now.
```

---

# 🧾 Pydantic Response

The API returns a structured response:

```json
{
  "answer": "string",
  "sources": ["doc_01"],
  "confidence": 1.0
}
```

Fields:

* `answer` — assistant response
* `sources` — retrieved document IDs
* `confidence` — confidence value between 0 and 1

---

# 🚀 FastAPI

The support assistant exposes:

```text
POST /ask
```

### Policy Query

Request:

```json
{
  "query": "What is the return policy for damaged grocery items?"
}
```

Example mock response:

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours...",
  "sources": [
    "doc_02",
    "doc_06",
    "doc_05"
  ],
  "confidence": 1.0
}
```

### General Query

Request:

```json
{
  "query": "How do I bake a cake?"
}
```

Response:

```json
{
  "answer": "I can only answer questions about Zepto policies right now.",
  "sources": [],
  "confidence": 1.0
}
```

---

# 🐳 Docker

Build the Support Assistant image from the **project root**:

```bash
docker build -f support_assistant/Dockerfile -t zepto-support .
```

Run the container:

```bash
docker run -p 7860:7860 zepto-support
```

Open the FastAPI Swagger documentation:

**http://localhost:7860/docs**

---

# ⚙️ Installation

## 1. Clone the Repository

```bash
git clone https://github.com/srujithach0-lang/zepto-data-ai-platform.git
```

## 2. Enter the Project Directory

```bash
cd zepto-data-ai-platform
```

## 3. Create a Virtual Environment

```bash
python -m venv .venv
```

## 4. Activate the Virtual Environment — Windows

```powershell
.venv\Scripts\activate
```

## 5. Install Dependencies

```bash
pip install -r requirements.txt
```

---

# ▶️ Running the Modules

## Module 1 — Data Pipeline

Open the module:

```bash
cd data_pipeline
```

Run:

```bash
python pipeline.py
```

Return to the project root when finished:

```bash
cd ..
```

---

## Module 2 — Analytics

Open the following notebooks in VS Code/Jupyter:

```text
analytics/01_eda.ipynb
analytics/02_modeling.ipynb
```

Run the notebook cells in order.

The modeling notebook generates:

```text
analytics/best_pipeline.joblib
```

---

## Module 3 — Support Assistant

From the project root:

```bash
cd support_assistant
```

Run:

```bash
python main.py
```

Open:

**http://127.0.0.1:7860/docs**

For Docker, return to the project root and use:

```bash
cd ..
docker build -f support_assistant/Dockerfile -t zepto-support .
docker run -p 7860:7860 zepto-support
```

Then open:

**http://localhost:7860/docs**

---

# 🔍 Project Design Highlights

### Data Engineering

Transforms raw scraped data into structured relational data using Python, Pandas, SQL, and SQLite.

### Machine Learning

Implements a complete ML workflow:

```text
Preprocessing
      ↓
Training
      ↓
Evaluation
      ↓
Imbalance Handling
      ↓
Hyperparameter Tuning
      ↓
Serialization
      ↓
Reloading
```

### RAG

Uses local embeddings and vector similarity retrieval to ground support responses in a fixed policy corpus.

### API

FastAPI provides the `/ask` endpoint for customer-support queries.

### Deployment

Docker provides a reproducible local environment for running the support assistant.

---

# 📁 Module Documentation

Detailed documentation is available in each module:

* 📊 [Module 1 — Data Pipeline README](./data_pipeline/README.md)
* 📈 [Module 2 — Analytics & Modeling README](./analytics/README.md)
* 🤖 [Module 3 — Support Assistant README](./support_assistant/README.md)

---

# 📌 Project Status

| Module                          | Status      |
| ------------------------------- | ----------- |
| Data Engineering Pipeline       | ✅ Completed |
| Analytics & Predictive Modeling | ✅ Completed |
| GenAI Policy Support Assistant  | ✅ Completed |
| FastAPI                         | ✅ Tested    |
| Docker                          | ✅ Tested    |
| Documentation                   | ✅ Included  |

---

# 🎯 Learning Outcomes

This capstone demonstrates practical experience with:

* Data collection and cleaning
* Relational database design
* SQL and Pandas
* Exploratory Data Analysis
* Machine Learning
* Model evaluation
* Imbalanced classification
* SMOTE
* Hyperparameter tuning
* Regression
* ML pipeline serialization
* Embeddings
* Vector databases
* Retrieval-Augmented Generation
* LangGraph
* Structured prompting
* Pydantic
* FastAPI
* Docker

---

# 👩‍💻 Author

**Kummari Vishwagna**

BSc Honours — Computer Science / Data Science

### Skills Demonstrated

```text
Python | Pandas | NumPy | SQL | Machine Learning
RAG | LLMs | Prompt Engineering | LangGraph
ChromaDB | FastAPI | Docker
```

---

# 📜 License

This project was created as part of an academic capstone project for learning and demonstration purposes.
