FROM python:3.12-slim

WORKDIR /app
COPY scraping_engine/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt && \
    playwright install chromium && \
    playwright install-deps chromium

COPY scraping_engine/ .

CMD ["python", "run.py"]
