# Danh sách Tính năng Chi tiết - Bot Trading AI Binance Futures (v1.1)

## 1. Chức năng Cốt lõi

### 1.1. Phân tích Dữ liệu Thời gian thực
*   **Kết nối API Binance:** Thiết lập và duy trì kết nối ổn định với API Binance Futures để lấy dữ liệu thị trường.
*   **Lấy Dữ liệu Token:** Lấy dữ liệu giá (candlestick OHLCV - Open, High, Low, Close, Volume) cho các cặp giao dịch được chỉ định (BTCUSDT, SOLUSDT, ETHUSDT) trên các khung thời gian: 1 phút, 5 phút, 15 phút, 30 phút, 1 giờ, 4 giờ, 1 ngày.
*   **Tính toán Chỉ báo Kỹ thuật:** Xử lý dữ liệu giá để tính toán các chỉ báo kỹ thuật phổ biến (ví dụ: Moving Averages - MA, Relative Strength Index - RSI, Moving Average Convergence Divergence - MACD, Bollinger Bands). Danh sách chỉ báo cụ thể và các tham số sẽ được điều chỉnh dựa trên chế độ giao dịch được chọn (Scalp/Swing).
*   **Phân tích Đa khung thời gian:** Tổng hợp và phân tích tín hiệu từ các chỉ báo trên nhiều khung thời gian để có cái nhìn toàn diện về xu hướng và động lượng thị trường, ưu tiên các khung thời gian phù hợp với chế độ Scalp hoặc Swing.

### 1.2. Cấu hình Người dùng
*   **Giao diện Nhập liệu:** Cung cấp giao diện cho người dùng nhập và chọn các thông số sau:
    *   **Chế độ Giao dịch:** Lựa chọn giữa "Scalp" (giao dịch ngắn hạn, lợi nhuận nhỏ, tần suất cao) hoặc "Swing" (giao dịch dài hạn hơn, lợi nhuận lớn hơn, tần suất thấp).
    *   **Vốn Hiện có (USDT):** Tổng số vốn người dùng dự định sử dụng cho bot.
    *   **Lợi nhuận Mục tiêu/Lệnh (USDT):** Mức lợi nhuận mong muốn cho mỗi giao dịch thành công (có thể gợi ý giá trị mặc định dựa trên chế độ Scalp/Swing).
    *   **Lỗ Tối đa/Lệnh (USDT):** Mức lỗ tối đa người dùng chấp nhận cho mỗi giao dịch (có thể gợi ý giá trị mặc định dựa trên chế độ Scalp/Swing).
*   **Lưu trữ Cấu hình:** Lưu trữ an toàn các cấu hình do người dùng nhập/chọn để sử dụng trong các phiên làm việc sau.

### 1.3. Bộ máy Chiến lược Giao dịch
*   **Logic Giao dịch Thích ứng:** Triển khai các thuật toán/logic giao dịch riêng biệt hoặc có thể điều chỉnh tham số dựa trên chế độ giao dịch (Scalp/Swing) do người dùng chọn.
    *   **Scalp Mode:** Ưu tiên các tín hiệu trên khung thời gian thấp (ví dụ: 1m, 5m, 15m), sử dụng các chỉ báo nhạy cảm với biến động giá ngắn hạn, đặt mục tiêu TP/SL gần hơn.
    *   **Swing Mode:** Ưu tiên các tín hiệu trên khung thời gian cao hơn (ví dụ: 1h, 4h, 1d), tập trung vào xu hướng lớn, đặt mục tiêu TP/SL xa hơn.
*   **Xác định Cơ hội:** Tự động xác định các cơ hội vào lệnh tiềm năng (Long hoặc Short) dựa trên các quy tắc phù hợp với chế độ đã chọn.
*   **Quản lý Rủi ro Tích hợp:** Tính toán khối lượng vào lệnh và mức đòn bẩy đề xuất dựa trên vốn hiện có, mức lỗ tối đa/lệnh, khoảng cách đến điểm dừng lỗ (Stop Loss), và có thể điều chỉnh theo mức độ rủi ro của chế độ Scalp/Swing.

### 1.4. Tạo Đề xuất Giao dịch
*   **Thông tin Đầy đủ:** Với mỗi cơ hội được xác định, tạo ra một đề xuất giao dịch chi tiết bao gồm:
    *   **Token:** Mã token (BTC, SOL, ETH).
    *   **Chế độ:** Scalp hoặc Swing (để người dùng biết đề xuất này thuộc chế độ nào).
    *   **Hướng Lệnh:** Long hoặc Short.
    *   **Giá vào lệnh (Entry - Limit):** Mức giá đề xuất để đặt lệnh giới hạn.
    *   **Điểm Dừng lỗ (Stop Loss - SL):** Mức giá để cắt lỗ nếu thị trường đi ngược hướng.
    *   **Điểm Chốt lời (Take Profit - TP):** Mức giá để chốt lời khi đạt mục tiêu lợi nhuận.
    *   **Đòn bẩy (Leverage):** Mức đòn bẩy được đề xuất.
*   **Giải thích Lý do:** Cung cấp giải thích rõ ràng, dựa trên phân tích kỹ thuật và chế độ giao dịch đã chọn, về lý do tại sao đề xuất giao dịch này được đưa ra.

## 2. Chức năng Hỗ trợ (Không thay đổi)

### 2.1. Giao diện Người dùng
*   Hiển thị trạng thái kết nối, giá token, cấu hình, đề xuất, log.

### 2.2. Lưu trữ và Tải Cấu hình
*   Lưu/tải cấu hình người dùng giữa các phiên.

### 2.3. Ghi Log
*   Ghi lại các sự kiện quan trọng, lỗi, và đề xuất đã tạo.
