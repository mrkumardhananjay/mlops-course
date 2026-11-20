# The delivery-time prediction service.
FROM python:3.12-slim

WORKDIR /app

# Libraries first: this layer is cached and rarely changes.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Code and model last: these change often.
COPY app.py .
COPY model.joblib .

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
