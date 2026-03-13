# Sentiment Tracker

Production-oriented Vietnamese NLP system for sentiment analysis and e-commerce order information extraction.

## Why this project
- Turn unstructured social comments into actionable business signals.
- Detect sentiment in real time to support customer service and brand monitoring.
- Extract order intent, phone, and address hints to reduce manual operations.

## Core capabilities
- Vietnamese sentiment classification pipeline.
- Rule-based order entity extraction (phone, location, product hints).
- Web scraping workflow for collecting social text sources.
- Streamlit dashboard for interactive analysis and export.

## Tech stack
- Python
- Transformers / PyTorch
- Streamlit
- Pandas
- Selenium + BeautifulSoup

## Project structure
```text
sentiment-tracker/
|-- app.py
|-- sentiment_model.py
|-- order_extractor.py
|-- scraper.py
|-- requirements.txt
|-- .env.example
```

## Quick start
```bash
git clone https://github.com/laninh-tech/sentiment-tracker.git
cd sentiment-tracker
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

## Use cases
- Social sentiment monitoring for Vietnamese products and campaigns.
- Pre-processing and qualification of incoming order comments.
- Lightweight NLP prototype before production API deployment.

## Roadmap
- Add benchmark report for model metrics.
- Improve extraction quality with hybrid ML + rules.
- Add API service mode (FastAPI) for system integration.

## Author
La Quang Ninh  
GitHub: https://github.com/laninh-tech