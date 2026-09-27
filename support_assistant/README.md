# Zepto Customer Support AI Assistant

## 1. Overview

This module implements a local Retrieval-Augmented Generation (RAG) support assistant for Zepto policy questions.

The application uses:

* **Sentence Transformers** — local document embeddings
* **ChromaDB** — persistent vector storage and retrieval
* **LangGraph** — intent classification and workflow routing
* **Pydantic** — structured response validation
* **FastAPI** — REST API
* **Uvicorn** — local API server

The required execution mode is deterministic offline mock mode:

```text
MOCK_LLM=1
```

No paid API or external LLM service is required for the graded baseline.

---

## 2. Architecture

```text
Policy Documents
      |
      v
Document Ingestion
      |
      v
Sentence Transformers
all-MiniLM-L6-v2
      |
      v
ChromaDB
      |
      v
classify_intent
      |
      +-------------------------+
      |                         |
      v                         v
policy_question          general_question
      |                         |
      v                         v
retrieve_and_answer       direct_answer
      |
      v
Top-3 ChromaDB Retrieval
      |
      v
SupportResponse
(Pydantic)
      |
      v
FastAPI /ask
```

### Pipeline Components

| Stage               | Implementation                              |
| ------------------- | ------------------------------------------- |
| Ingestion           | `rag_graph.py` loads documents from `docs/` |
| Embedding           | Sentence Transformers `all-MiniLM-L6-v2`    |
| Storage/Retrieval   | Persistent ChromaDB collection              |
| Routing             | LangGraph `classify_intent`                 |
| Policy Retrieval    | LangGraph `retrieve_and_answer`             |
| General Query       | LangGraph `direct_answer`                   |
| Response Validation | Pydantic `SupportResponse`                  |
| API                 | `main.py` with FastAPI                      |

---

## 3. Project Structure

```text
support_assistant/
│
├── docs/
│   ├── doc_01.txt
│   ├── doc_02.txt
│   ├── doc_03.txt
│   ├── doc_04.txt
│   ├── doc_05.txt
│   ├── doc_06.txt
│   ├── doc_07.txt
│   └── doc_08.txt
│
├── chroma_db/
│   └── Persistent ChromaDB vector store
│
├── main.py
├── rag_graph.py
├── prompt_template.py
├── Dockerfile
└── README.md
```

---

## 4. Policy Documents

The `docs/` directory contains the eight required Zepto policy documents:

```text
doc_01.txt
doc_02.txt
doc_03.txt
doc_04.txt
doc_05.txt
doc_06.txt
doc_07.txt
doc_08.txt
```

Each document is stored using its filename-based document ID:

```text
doc_01
doc_02
...
doc_08
```

---

## 5. Ingestion, Embedding & Retrieval

The vector-store initialization is implemented in:

```text
rag_graph.py
```

The eight policy documents are embedded using:

```text
all-MiniLM-L6-v2
```

The embeddings are stored in a persistent ChromaDB collection under:

```text
chroma_db/
```

Policy queries are embedded and compared against the stored vectors. The top **3 most similar chunks** are retrieved.

The retrieved document IDs are returned through the `sources` field.

---

## 6. Intent Classification

The LangGraph workflow starts with:

```text
classify_intent
```

In the required mock mode, classification uses a keyword heuristic.

The policy keywords are:

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

If a keyword is present, the query is classified as:

```text
policy_question
```

Otherwise it is classified as:

```text
general_question
```

No LLM call is made in the required mock mode.

---

## 7. LangGraph Workflow

The application contains three named nodes.

### `classify_intent`

Routes the query to either:

```text
policy_question
```

or:

```text
general_question
```

### `retrieve_and_answer`

For a policy question:

1. Embeds the query.
2. Retrieves the top 3 ChromaDB results.
3. Stores the retrieved document IDs.
4. Generates the deterministic mock response from the top retrieved chunk.
5. Creates the validated `SupportResponse`.

### `direct_answer`

For a general question, returns:

```text
I can only answer questions about Zepto policies right now.
```

No retrieval is required for this route.

### Conditional Routing

```text
classify_intent
      |
      +---- policy_question ----> retrieve_and_answer
      |
      +---- general_question ---> direct_answer
```

---

## 8. Mock LLM Mode

The required graded mode is:

```text
MOCK_LLM=1
```

In this mode:

* Intent classification uses the keyword heuristic.
* ChromaDB retrieval runs normally.
* No external LLM API is called.
* Policy answers use the deterministic format:

```text
Based on the retrieved context: <top retrieved chunk excerpt>
```

* General questions use the fixed response:

```text
I can only answer questions about Zepto policies right now.
```

This makes the application deterministic and fully offline.

---

## 9. Optional Real LLM Mode

The optional real-LLM path can be enabled with:

```text
MOCK_LLM=0
```

In this mode, the structured prompt in:

```text
prompt_template.py
```

can be used for the generation step.

The prompt follows the required role-context-task-format-length structure and includes:

* Role definition
* Retrieved context
* Task
* Output format
* Length constraint
* Negative constraint
* Few-shot example

The required submission does not depend on this optional path.

---

## 10. Pydantic Response

The response model is:

```text
SupportResponse
```

It contains:

```json
{
  "answer": "string",
  "sources": ["document_id"],
  "confidence": 1.0
}
```

### Fields

* `answer` — final response returned to the customer
* `sources` — retrieved document/chunk IDs
* `confidence` — value between `0.0` and `1.0`

In mock mode:

```text
Policy question:
sources = retrieved document IDs
confidence = 1.0

General question:
sources = []
confidence = 1.0
```

---

## 11. FastAPI API

The FastAPI application is implemented in:

```text
main.py
```

Endpoint:

```text
POST /ask
```

Request:

```json
{
  "query": "What is the return policy for damaged grocery items?"
}
```

Example policy response:

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect...",
  "sources": [
    "doc_02",
    "doc_06",
    "doc_05"
  ],
  "confidence": 1.0
}
```

---

## 12. General Query Example

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

This demonstrates the `general_question` route.

---

## 13. Policy Query Example

Request:

```json
{
  "query": "What is the return policy for damaged grocery items?"
}
```

Response:

```json
{
  "answer": "Based on the retrieved context: Grocery and perishable items may be reported for a return within 24 hours of delivery if damaged, spoiled, or incorrect...",
  "sources": [
    "doc_02",
    "doc_06",
    "doc_05"
  ],
  "confidence": 1.0
}
```

This demonstrates the `policy_question` route and top-3 retrieval.

---

## 14. Running the Application

From the project root:

```bash
cd support_assistant
```

Run:

```bash
python main.py
```

The API runs locally at:

```text
http://127.0.0.1:7860
```

Interactive API documentation:

```text
http://127.0.0.1:7860/docs
```

Use the `/ask` endpoint to test both policy and general questions.

---

## 15. Docker

The project includes a `Dockerfile` for local containerization.

Build the image:

```bash
docker build -t zepto-support-assistant .
```

Run the container:

```bash
docker run -p 7860:7860 zepto-support-assistant
```

The API can then be accessed at:

```text
http://127.0.0.1:7860
```

---

## 16. Design Summary

The complete pipeline is:

```text
Policy Documents
      |
      v
Ingestion
      |
      v
all-MiniLM-L6-v2
Embeddings
      |
      v
ChromaDB
      |
      v
classify_intent
      |
      +-------------------+
      |                   |
      v                   v
Policy Query        General Query
      |                   |
      v                   v
Top-3 Retrieval      direct_answer
      |
      v
retrieve_and_answer
      |
      +---------+
                |
                v
        SupportResponse
                |
                v
           FastAPI /ask
```

The implementation provides a local deterministic RAG workflow with document ingestion, local embeddings, ChromaDB retrieval, LangGraph routing, structured Pydantic responses, and a FastAPI interface.
