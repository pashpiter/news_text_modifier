FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt ./

RUN pip install -r requirements.txt --no-cache-dir

COPY ./ ./

RUN flake8 .

RUN pytest

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]