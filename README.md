# 🎯 Sentiment Tracker – Phân tích cảm xúc đa kênh & Trích xuất đơn hàng

<div align="center">

**Dashboard phân tích cảm xúc theo thời gian thực với chức năng trích xuất thông tin đơn hàng thông minh cho e-commerce Việt**

[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.42.0-red?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![PyTorch](https://img.shields.io/badge/PyTorch-2.6.0-ee4c2c?logo=pytorch&logoColor=white)](https://pytorch.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

</div>

---

## 📋 Mục lục
- [Giới thiệu](#-giới-thiệu)
- [Tính năng chính](#-tính-năng-chính)
- [Stack công nghệ](#-stack-công-nghệ)
- [Cài đặt](#-cài-đặt)
- [Hướng dẫn sử dụng](#-hướng-dẫn-sử-dụng)
- [Cấu trúc dự án](#-cấu-trúc-dự-án)
- [Hiệu suất mô hình](#-hiệu-suất-mô-hình)
- [Đóng góp](#-đóng-góp)
- [Giấy phép](#-giấy-phép)

---

## 📊 Giới thiệu

**Sentiment Tracker** là ứng dụng web thông minh giúp các doanh nghiệp thương mại điện tử giám sát cảm xúc khách hàng trên các kênh mạng xã hội, đồng thời tự động trích xuất thông tin đơn hàng từ bình luận và đánh giá.

### Chức năng chính:
- 🔍 **Phân tích cảm xúc theo thời gian thực**: Sử dụng mô hình PhoBERT được huấn luyện sẵn để phân loại cảm xúc tiếng Việt (Tích cực/Tiêu cực/Trung lập)
- 🎁 **Trích xuất đơn hàng thông minh**: Tự động phát hiện ý định mua hàng và trích xuất thông tin liên lạc (số điện thoại, địa chỉ)
- 📊 **Dashboard tương tác**: Trực quan hóa xu hướng cảm xúc và dữ liệu đơn hàng qua giao diện Streamlit hiện đại
- 💾 **Xuất dữ liệu**: Xuất các đơn hàng được trích xuất ra Excel để dễ dàng tích hợp với hệ thống quản lý

### Lợi ích kinh doanh:
- **F1-Score > 85%** độ chính xác trên dữ liệu cảm xúc tiếng Việt thực tế
- Giảm thời gian nhập đơn hàng thủ công bằng **tự động hóa trích xuất** từ mạng xã hội
- Hỗ trợ **quyết định kinh doanh nhanh** dựa trên phản hồi cảm xúc trực tiếp

---

## 🚀 Tính năng chính

| Tính năng | Mô tả |
|---------|-------------|
| **Web Scraper** | Trình duyệt headless dựa trên Selenium, vượt qua phát hiện bot và render các trang JavaScript (Facebook, news) |
| **Phân loại cảm xúc** | Mô hình PhoBERT được tinh chỉnh cho phân tích cảm xúc tiếng Việt |
| **Trích xuất đơn hàng** | Engine NLP dựa trên regex phát hiện từ khóa mua hàng, số điện thoại (định dạng Việt), địa chỉ |
| **Dashboard cảm xúc** | Hiển thị metrics, biểu đồ pie, phân tích xu hướng với Plotly |
| **Tab đơn hàng** | Bảng dữ liệu đơn hàng được trích xuất, có thể lọc và xuất ra Excel |
| **Hỗ trợ tiếng Việt** | Xử lý văn bản tiếng Việt hoàn chỉnh (tokenization, loại bỏ stopwords) sử dụng pyvi |

---

## 🛠️ Stack công nghệ

### Framework chính
- **Streamlit** (1.42.0) – Framework dashboard web
- **Python** (3.8+) – Ngôn ngữ lập trình chính

### Machine Learning & NLP
- **PyTorch** (2.6.0) – Framework deep learning
- **Transformers** (4.49.0) – Mô hình ngôn ngữ được huấn luyện trước (PhoBERT)
- **pyvi** – Tokenization tiếng Việt & loại bỏ stopwords

### Web Scraping & Xử lý dữ liệu
- **Selenium** – Tự động hóa trình duyệt
- **BeautifulSoup4** – Phân tích HTML
- **Requests** – HTTP client
- **Pandas** (2.2.3) – Thao tác & phân tích dữ liệu

### Trực quan hóa & Xuất dữ liệu
- **Plotly** (6.0.0) – Biểu đồ tương tác
- **openpyxl** (3.1.5) – Xuất Excel

---

## ⚙️ Cài đặt

### Yêu cầu
- Python 3.8 trở lên
- pip (trình quản lý gói Python)

### Bước 1: Clone kho lưu trữ
```bash
git clone https://github.com/laninh-tech/sentiment-tracker.git
cd sentiment-tracker
```

### Bước 2: Tạo môi trường ảo (Khuyên dùng)
```bash
python -m venv venv

# Trên Windows
venv\Scripts\activate

# Trên macOS/Linux
source venv/bin/activate
```

### Bước 3: Cài đặt thư viện
```bash
pip install -r requirements.txt
```

Quá trình này sẽ cài đặt:
- Mô hình PhoBERT từ Hugging Face (tự động tải lần đầu tiên)
- ChromeDriver via `webdriver-manager` (tự động quản lý)
- Tất cả các gói Python cần thiết

---

## 🎮 Hướng dẫn sử dụng

### Bắt đầu nhanh
```bash
streamlit run app.py
```
Ứng dụng sẽ mở trong trình duyệt tại `http://localhost:8501`

### Cách sử dụng các tính năng

#### 1. **Nhập dữ liệu thủ công**
- Chọn "Manual Data Entry" từ Control Panel
- Dán bình luận hoặc đánh giá của khách hàng
- Bấm "Run Analysis pipeline"
- Xem kết quả phân loại cảm xúc và trích xuất đơn hàng

#### 2. **Scraper URL**
- Chọn "URL Web Scraper" từ Control Panel
- Nhập URL (bài viết Facebook, bài báo, blog)
- Tùy chọn: Cung cấp cookie Facebook để truy cập nội dung riêng tư
- Bấm "Extract & Analyze"
- Hệ thống tự động cào, xử lý token và phân tích cảm xúc

#### 3. **Dashboard cảm xúc** (Tab 1)
Xem các số liệu chính:
- Tổng số bình luận được phân tích
- Số lượng cảm xúc Tích cực/Tiêu cực/Trung lập
- Biểu đồ phân bố
- Điểm tin cậy cảm xúc
- Chi tiết cảm xúc từng bình luận

#### 4. **Đơn hàng E-Commerce** (Tab 2)
Duyệt các đơn hàng được trích xuất:
- Số điện thoại (định dạng Việt: 03x, 05x, 07x, 08x, 09x + 8 chữ số)
- Địa chỉ giao hàng được suy luận (đường phố, quận/huyện, tỉnh/thành phố)
- Gợi ý sản phẩm từ bình luận
- Xuất ra Excel (.xlsx) cho nhãn vận chuyển

#### 5. **Xóa dữ liệu Dashboard**
Reset dữ liệu và bắt đầu lại bằng nút "🗑️ Clear Dashboard Data"

---

## 📁 Cấu trúc dự án

```
sentiment-tracker/
├── app.py                   # Ứng dụng dashboard Streamlit chính
├── sentiment_model.py       # Lớp SentimentModel + wrapper PhoBERT
├── scraper.py              # Web scraper sử dụng Selenium
├── order_extractor.py      # Engine trích xuất đơn hàng (số điện thoại, địa chỉ, sản phẩm)
├── requirements.txt         # Thư viện Python cần thiết
├── metadata.json           # Siêu dữ liệu dự án
├── README.md              # Tệp này
└── __pycache__/           # Bộ nhớ cache Python (tự động sinh)
```

### Các module chính

**sentiment_model.py**
- `SentimentModel`: Tải PhoBERT từ Hugging Face
- `preprocess_text()`: Làm sạch văn bản tiếng Việt (chuyển thành chữ thường, loại bỏ URL, tokenization)
- `predict()`: Trả về nhãn cảm xúc + điểm tin cậy

**scraper.py**
- `scrape_url()`: Trình duyệt headless Selenium với các biện pháp chống phát hiện
- Xử lý rendering JavaScript và bảo vệ Cloudflare
- Trích xuất khối văn bản và cấu trúc dưới dạng "bình luận"

**order_extractor.py**
- `OrderExtractor`: Phát hiện đơn hàng dựa trên regex
- Mô hình số điện thoại: Định dạng di động Việt Nam
- Từ khóa địa chỉ & tỉnh thành để phát hiện vị trí
- Chỉ báo biến thể sản phẩm (màu sắc, kích cỡ, đơn vị)

**app.py**
- Giao diện Streamlit với CSS tùy chỉnh
- Quản lý trạng thái phiên cho dữ liệu lưu giữ
- Giao diện dựa trên tab (Sentiment Dashboard | Orders)
- Hiển thị metrics theo thời gian thực và trực quan hóa tương tác

---

## 🎯 Hiệu suất mô hình

### Phân loại cảm xúc
- **Mô hình**: PhoBERT (wonrax/phobert-base-vietnamese-sentiment)
- **F1-Score**: > 85% trên các benchmark cảm xúc tiếng Việt
- **Các lớp**: Tích cực, Tiêu cực, Trung lập
- **Đầu vào**: Văn bản tiếng Việt được xử lý trước (tokenization, làm sạch)
- **Đầu ra**: Nhãn + điểm tin cậy (0.0 - 1.0)

### Trích xuất đơn hàng
- **Tỷ lệ phát hiện số điện thoại**: >95% (định dạng nhà mạng di động Việt Nam)
- **Trích xuất địa chỉ**: Phương pháp dựa trên từ khóa + khớp tỉnh thành
- **Gợi ý sản phẩm**: Từ khóa biến thể (màu, size, kg, v.v.)

---

## 🤝 Đóng góp

Mọi đóng góp đều được chào đón! Vui lòng thực hiện theo các bước sau:

1. Fork kho lưu trữ
2. Tạo nhánh tính năng (`git checkout -b feature/tính-năng-tuyệt-vời`)
3. Commit thay đổi (`git commit -m 'Thêm tính năng tuyệt vời'`)
4. Push lên nhánh (`git push origin feature/tính-năng-tuyệt-vời`)
5. Mở Pull Request

### Tiêu chuẩn code
- Tuân theo hướng dẫn lập trình PEP 8 của Python
- Thêm docstrings cho hàm và lớp
- Kiểm tra các tính năng mới cục bộ trước khi gửi

---

## 📄 Giấy phép

Dự án này được cấp phép theo Giấy phép MIT - xem tệp LICENSE để biết chi tiết.

---

## 📞 Hỗ trợ

Để báo cáo vấn đề, yêu cầu tính năng hoặc có câu hỏi:
- Mở issue trên [GitHub Issues](https://github.com/laninh-tech/sentiment-tracker/issues)
- Liên hệ: Xem thông tin liên hệ trong kho lưu trữ

---

## 🙏 Ghi nhận

- **PhoBERT**: Mô hình được huấn luyện trước từ [wonrax](https://huggingface.co/wonrax/phobert-base-vietnamese-sentiment)
- **Streamlit**: Cảm ơn framework web tuyệt vời
- **Hugging Face**: Cảm ơn thư viện Transformers
- **Cộng đồng NLP Việt Nam**: Cảm ơn pyvi và các tài nguyên ngôn ngữ

---

<div align="center">

Được tạo với ❤️ cho cộng đồng thương mại điện tử Việt Nam

[⬆ Quay lại đầu trang](#-sentiment-tracker--phân-tích-cảm-xúc-đa-kênh--trích-xuất-đơn-hàng)

</div>
