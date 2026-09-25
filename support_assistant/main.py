import uvicorn
from fastapi import FastAPI
from rag_graph import rag_app, AskRequest, SupportResponse


# ------------------------------------------------------------
# FastAPI Application
# ------------------------------------------------------------

app = FastAPI(
    title="Zepto Customer Support AI Assistant",
    description=(
        "RAG-based support assistant for Zepto delivery, "
        "returns, refunds, cancellation, membership, tracking, "
        "gift cards, and customer support policies."
    ),
    version="1.0.0"
)


# ------------------------------------------------------------
# Root Endpoint
# ------------------------------------------------------------

@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "Zepto Support Assistant API"
    }


# ------------------------------------------------------------
# POST /ask
# ------------------------------------------------------------

@app.post("/ask", response_model=SupportResponse)
def ask_question(request: AskRequest):

    # Initial LangGraph state
    initial_state = {
        "query": request.query,
        "intent": "",
        "retrieved_docs": [],
        "final_output": None
    }

    # Run the LangGraph workflow
    final_state = rag_app.invoke(initial_state)

    # Return the validated Pydantic response
    return final_state["final_output"]


# ------------------------------------------------------------
# Run FastAPI locally
# ------------------------------------------------------------

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="127.0.0.1",
        port=7860,
        reload=True
    )

