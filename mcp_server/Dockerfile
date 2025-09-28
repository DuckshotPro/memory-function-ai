FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

# We need to fix the requirements file before installing
RUN sed -i '/--fix/d' requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
