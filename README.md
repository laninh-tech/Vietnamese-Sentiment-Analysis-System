# Sentiment Intelligence Tracker

Vietnamese NLP pipeline for sentiment analysis and order-intent extraction from unstructured social content.

## Project Objective
Convert noisy user comments into actionable business insights, including sentiment signals and potential order information.

## Tech Stack
- Python
- PyTorch + Transformers
- Streamlit
- Selenium + BeautifulSoup
- Pandas

## Key Capabilities
- Vietnamese sentiment classification
- Order signal extraction (phone, location hints, product hints)
- URL-based text collection workflow
- Interactive dashboard for analysis and export

## Installation
```bash
git clone https://github.com/laninh-tech/sentiment-tracker.git
cd sentiment-tracker
python -m venv .venv
# Windows
.venv\Scripts\activate
# macOS/Linux
# source .venv/bin/activate
pip install -r requirements.txt
```

## Run
```bash
streamlit run app.py
```

## Current Results
- Established a reusable Vietnamese NLP workflow for practical use.
- Reduced manual review effort by extracting order-relevant signals.
- Created a foundation for future API deployment and scaling.

## Roadmap
- Add benchmark report and model comparison table.
- Improve extraction precision with hybrid rules + model approach.
- Expose inference through FastAPI for integration.

## Author
La Quang Ninh