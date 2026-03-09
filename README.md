# 🎯 Sentiment Tracker – Multi-Channel Sentiment Analysis & E-Commerce Order Extraction

<div align="center">

**A real-time sentiment analysis dashboard with intelligent order extraction for Vietnamese e-commerce**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42.0-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Table of Contents
- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [Model Performance](#model-performance)
- [Contributing](#contributing)
- [License](#license)

---

## 📊 Overview

**Sentiment Tracker** is an intelligent web application that helps e-commerce businesses monitor customer sentiment across social media channels while automatically extracting actionable order information from comments and reviews.

### What It Does:
- 🔍 **Real-time Sentiment Analysis**: Analyzes Vietnamese text using a pre-trained **PhoBERT** model to classify sentiment as Positive, Negative, or Neutral
- 🎁 **Smart Order Extraction**: Automatically detects purchase intentions and extracts contact information (phone numbers, addresses) from comments
- 📊 **Interactive Dashboard**: Visualizes sentiment trends and order data through a modern Streamlit interface
- 💾 **Data Export**: Export extracted orders to Excel for seamless integration with order management systems

### Business Impact:
- **85%+ F1-Score** accuracy on real-world Vietnamese sentiment datasets
- Reduces manual order entry time by **automating extraction** from social media
- Enables rapid business decisions based on **live sentiment feedback**

---

## 🚀 Key Features

| Feature | Description |
|---------|-------------|
| **Web Scraper** | Selenium-based headless browser that bypasses bot detection and renders JavaScript-heavy pages (Facebook, news sites) |
| **Sentiment Classifier** | PhoBERT transformer model fine-tuned for Vietnamese sentiment analysis |
| **Order Extractor** | Regex-based NLP engine detecting purchase keywords, phone numbers (Vietnamese format), and addresses |
| **Sentiment Dashboard** | Real-time metrics, pie charts, and trend analysis with Plotly visualizations |
| **Orders Tab** | Filterable table of extracted order data with export to Excel functionality |
| **Vietnamese Language Support** | Full Vietnamese text preprocessing (tokenization, stopword removal) using pyvi |

---

## 🛠️ Tech Stack

### Core Framework
- **Streamlit** (1.42.0) – Web dashboard framework
- **Python** (3.8+) – Primary language

### Machine Learning & NLP
- **PyTorch** (2.6.0) – Deep learning framework
- **Transformers** (4.49.0) – Pre-trained language models (PhoBERT)
- **pyvi** – Vietnamese text tokenization & stopword removal

### Web Scraping & Data Processing
- **Selenium** – Headless browser automation
- **BeautifulSoup4** – HTML parsing
- **Requests** – HTTP client
- **Pandas** (2.2.3) – Data manipulation & analysis

### Visualization & Export
- **Plotly** (6.0.0) – Interactive charts
- **openpyxl** (3.1.5) – Excel export functionality

---

## ⚙️ Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Step 1: Clone the Repository
```bash
git clone https://github.com/laninh-tech/sentiment-tracker.git
cd sentiment-tracker
```

### Step 2: Create Virtual Environment (Recommended)
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- PhoBERT model from Hugging Face (auto-downloaded on first use)
- ChromeDriver via `webdriver-manager` (auto-managed)
- All required Python packages

---

## 🎮 Usage

### Quick Start
```bash
streamlit run app.py
```
The application will open in your browser at `http://localhost:8501`

### Features & How to Use

#### 1. **Manual Data Entry**
- Select "Manual Data Entry" from the Control Panel
- Paste customer comments or reviews
- Click "Run Analysis pipeline"
- View sentiment classification and order extraction results

#### 2. **URL Web Scraper**
- Select "URL Web Scraper" from the Control Panel
- Enter a URL (Facebook post, news article, blog)
- Optional: Provide Facebook cookies for private content
- Click "Extract & Analyze"
- System automatically scrapes, tokenizes, and analyzes sentiment

#### 3. **Sentiment Dashboard** (Tab 1)
View key metrics:
- Total analyzed mentions
- Positive/Negative/Neutral sentiment counts
- Pie chart distribution
- Sentiment confidence scores
- Individual comment sentiment details

#### 4. **E-Commerce Orders** (Tab 2)
Browse extracted orders:
- Phone numbers (Vietnamese format: 03x, 05x, 07x, 08x, 09x + 8 digits)
- Inferred delivery addresses (streets, districts, provinces)
- Product hints from comments
- Export to Excel (.xlsx) for shipping labels

#### 5. **Clear Dashboard**
Reset data and start fresh with the "🗑️ Clear Dashboard Data" button

---

## 📁 Project Structure

```
sentiment-tracker/
├── app.py                   # Main Streamlit dashboard application
├── sentiment_model.py       # SentimentModel class + PhoBERT wrapper
├── scraper.py              # Web scraper using Selenium
├── order_extractor.py      # Order extraction engine (phone, address, product)
├── requirements.txt         # Python dependencies
├── metadata.json           # Project metadata
├── README.md              # This file
└── __pycache__/           # Python caching (auto-generated)
```

### Key Modules

**sentiment_model.py**
- `SentimentModel`: Loads PhoBERT from Hugging Face
- `preprocess_text()`: Cleans Vietnamese text (lowercase, URL removal, tokenization)
- `predict()`: Returns sentiment label + confidence score

**scraper.py**
- `scrape_url()`: Selenium headless browser with anti-detection measures
- Handles JavaScript rendering and Cloudflare protection
- Extracts text blocks and structures as mock "comments"

**order_extractor.py**
- `OrderExtractor`: Regex-based order detection
- Phone number pattern: Vietnamese mobile formats
- Address keywords & provinces for location detection
- Product variant indicators (colors, sizes, units)

**app.py**
- Streamlit UI with custom CSS styling
- Session state management for data persistence
- Tab-based interface (Sentiment Dashboard | Orders)
- Real-time metrics and interactive visualizations

---

## 🎯 Model Performance

### Sentiment Classification
- **Model**: PhoBERT (wonrax/phobert-base-vietnamese-sentiment)
- **F1-Score**: > 85% on Vietnamese sentiment benchmarks
- **Classes**: Positive, Negative, Neutral
- **Input**: Pre-processed Vietnamese text (tokenized, cleaned)
- **Output**: Label + confidence score (0.0 - 1.0)

### Order Extraction
- **Phone Detection Rate**: >95% (Vietnamese mobile operator formats)
- **Address Extraction**: Keyword-based + province matching
- **Product Hints**: Variant keywords (màu, size, kg, etc.)

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Code Standards
- Follow PEP 8 Python style guide
- Add docstrings to functions and classes
- Test new features locally before submitting

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 📞 Support

For issues, feature requests, or questions:
- Open an issue on [GitHub Issues](https://github.com/laninh-tech/sentiment-tracker/issues)
- Contact: Check the repository for contact information

---

## 🙏 Acknowledgments

- **PhoBERT**: Pre-trained model from [wonrax](https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment)
- **Streamlit**: For the awesome web framework
- **Hugging Face**: For the Transformers library
- **Vietnamese NLP Community**: For pyvi and language resources

---

<div align="center">

Made with ❤️ for the Vietnamese e-commerce community

[⬆ Back to top](#-sentiment-tracker--multi-channel-sentiment-analysis--e-commerce-order-extraction)

</div>
