FROM python:3.11-slim

WORKDIR /app

# Copy root requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy support_assistant code and documents
COPY support_assistant/ /app/

EXPOSE 7860

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "7860"]