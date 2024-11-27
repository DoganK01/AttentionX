FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1

WORKDIR /app

RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


COPY app/ .


RUN pip install --no-cache-dir -r requirements.txt


EXPOSE 8083


CMD ["python", "-m", "chainlit", "run", "main.py", "-h", "--port", "8083", "--host", "0.0.0.0"]
