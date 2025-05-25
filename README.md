# 🤖 Binance Futures AI Bot

Bot Trading AI cho Binance Futures hỗ trợ phân tích kỹ thuật và đưa ra đề xuất giao dịch cho các token BTC, SOL, ETH với 2 chế độ: Scalp và Swing.

## ✨ Tính năng chính

- 📊 **Phân tích kỹ thuật đa khung thời gian** (1m, 5m, 15m, 30m, 1h, 4h, 1d)
- 🎯 **2 chế độ giao dịch**: Scalp (ngắn hạn) và Swing (dài hạn)
- 💡 **Đề xuất giao dịch thông minh** với Entry, SL, TP, Leverage
- 📈 **Giao diện web thân thiện** với Streamlit
- 🔄 **Cập nhật dữ liệu thời gian thực** từ Binance API
- ⚙️ **Cấu hình linh hoạt** theo nhu cầu người dùng
- 📝 **Log hoạt động chi tiết**

## 🚀 Cài đặt

### 1. Yêu cầu hệ thống
- Python 3.8 trở lên
- Kết nối Internet ổn định
- 4GB RAM (khuyến nghị)

### 2. Clone repository
```bash
git clone <repository-url>
cd binance-trading
```

### 3. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 4. Chạy ứng dụng
```bash
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

## 📖 Hướng dẫn sử dụng

### 1. Cấu hình giao dịch
- **Chế độ giao dịch**: Chọn Scalp hoặc Swing
  - **Scalp**: Giao dịch ngắn hạn (1-15 phút), lợi nhuận nhỏ, tần suất cao
  - **Swing**: Giao dịch dài hạn (1-24 giờ), lợi nhuận lớn, tần suất thấp
- **Vốn khả dụng**: Nhập số vốn USDT bạn muốn sử dụng
- **Lợi nhuận mục tiêu**: Mức lợi nhuận mong muốn cho mỗi lệnh
- **Lỗ tối đa**: Mức lỗ tối đa chấp nhận cho mỗi lệnh

### 2. Khởi động Bot
- Nhấn nút "🚀 Bắt đầu Bot" trong sidebar
- Bot sẽ tự động kết nối Binance API và tải dữ liệu
- Theo dõi trạng thái kết nối ở phần đầu trang

### 3. Theo dõi đề xuất
- Xem các đề xuất giao dịch trong bảng chính
- Mỗi đề xuất bao gồm:
  - **Timestamp**: Thời gian tạo đề xuất
  - **Mode**: Chế độ giao dịch (Scalp/Swing)
  - **Token**: BTC, ETH, hoặc SOL
  - **Direction**: LONG (mua) hoặc SHORT (bán)
  - **Entry**: Giá vào lệnh đề xuất
  - **SL**: Stop Loss (cắt lỗ)
  - **TP**: Take Profit (chốt lời)
  - **Leverage**: Đòn bẩy đề xuất
  - **Reason**: Lý do phân tích kỹ thuật

### 4. Thực hiện giao dịch
⚠️ **Quan trọng**: Bot chỉ đưa ra đề xuất, không tự động giao dịch. Bạn cần:
- Tự đánh giá và quyết định có thực hiện giao dịch hay không
- Đăng nhập Binance và đặt lệnh thủ công
- Quản lý rủi ro theo khả năng tài chính của bản thân

## 🔧 Cấu trúc dự án

```
binance-trading/
├── app.py                 # Ứng dụng Streamlit chính
├── requirements.txt       # Dependencies
├── README.md             # Hướng dẫn này
├── config/               # Cấu hình
│   ├── __init__.py
│   ├── config.py         # Quản lý cấu hình
│   └── settings.json     # File cấu hình mặc định
├── modules/              # Modules chính
│   ├── __init__.py
│   ├── data_models.py    # Data models
│   ├── binance_connector.py  # Kết nối Binance API
│   ├── technical_analysis.py # Phân tích kỹ thuật
│   └── trading_strategy.py   # Logic chiến lược
├── ui/                   # Giao diện người dùng
│   ├── __init__.py
│   └── components.py     # Components UI
├── utils/                # Tiện ích
│   ├── __init__.py
│   └── logger.py         # Logging
└── documents/            # Tài liệu đặc tả
```

## 📊 Chỉ báo kỹ thuật được sử dụng

### Scalp Mode
- **RSI** (14): Ngưỡng 30/70 cho oversold/overbought
- **Moving Averages**: MA10, MA20
- **MACD** (12,26,9): Tín hiệu cross
- **Bollinger Bands**: Breakout signals
- **Khung thời gian ưu tiên**: 1m, 5m, 15m

### Swing Mode
- **RSI** (14): Ngưỡng 20/80 cho oversold/overbought
- **Moving Averages**: MA20, MA50
- **MACD** (12,26,9): Trend confirmation
- **Bollinger Bands**: Support/Resistance
- **Khung thời gian ưu tiên**: 1h, 4h, 1d

## ⚠️ Tuyên bố miễn trừ trách nhiệm

- Bot này chỉ là công cụ hỗ trợ phân tích kỹ thuật
- Không đảm bảo lợi nhuận và có thể gây thua lỗ
- Mọi quyết định giao dịch và rủi ro thuộc về người dùng
- Không sử dụng số tiền không thể chịu đựng được nếu mất
- Luôn thực hiện nghiên cứu riêng trước khi giao dịch

## 🛠️ Khắc phục sự cố

### Lỗi kết nối Binance
- Kiểm tra kết nối Internet
- Thử khởi động lại bot
- Binance API có thể bị giới hạn tốc độ

### Bot không tạo đề xuất
- Đảm bảo đã cấu hình đúng chế độ giao dịch
- Chờ đủ dữ liệu để phân tích (ít nhất 5-10 phút)
- Thị trường có thể không có tín hiệu rõ ràng

### Lỗi cài đặt dependencies
```bash
# Nếu gặp lỗi với pandas-ta
pip install --upgrade pip
pip install pandas-ta --no-cache-dir

# Nếu gặp lỗi với aiohttp
pip install aiohttp --upgrade
```

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra log trong ứng dụng
2. Đọc kỹ hướng dẫn này
3. Kiểm tra file log trong thư mục `logs/` (nếu có)

## 📝 Changelog

### v1.1
- Thêm hỗ trợ chế độ Scalp/Swing
- Cải thiện giao diện Streamlit
- Tối ưu hóa phân tích kỹ thuật
- Thêm quản lý rủi ro tự động

### v1.0
- Phiên bản đầu tiên
- Hỗ trợ 3 token: BTC, ETH, SOL
- Phân tích kỹ thuật cơ bản
- Giao diện web với Streamlit

---

**Phát triển bởi AI Assistant** | **Phiên bản 1.1** | **2025** 