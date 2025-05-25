# Đề xuất Công nghệ và Kiến trúc Hệ thống - Bot Trading AI Binance Futures (v1.1 - Streamlit UI)

**Phiên bản:** 1.1
**Ngày:** 25 tháng 5 năm 2025

## 1. Đề xuất Công nghệ (Technology Stack)

Việc lựa chọn công nghệ phù hợp là rất quan trọng để đảm bảo hệ thống hoạt động hiệu quả, ổn định và dễ bảo trì, đặc biệt với yêu cầu phân tích thời gian thực và giao diện người dùng thân thiện.

### 1.1. Backend (Lõi xử lý)
*   **Ngôn ngữ lập trình:** **Python 3.x**
    *   **Lý do:** Python là lựa chọn hàng đầu cho các ứng dụng khoa học dữ liệu, tài chính và AI. Nó có hệ sinh thái thư viện phong phú, cộng đồng hỗ trợ lớn, cú pháp rõ ràng, và khả năng xử lý dữ liệu mạnh mẽ.
*   **Thư viện chính:**
    *   **Kết nối API Binance:**
        *   `python-binance`: Thư viện phổ biến, hỗ trợ cả REST API và WebSocket API của Binance, giúp đơn giản hóa việc lấy dữ liệu thị trường (giá, nến) và dữ liệu tài khoản (nếu cần trong tương lai).
        *   Hoặc `requests` (cho REST) và `websockets` (cho WebSocket) nếu muốn kiểm soát chi tiết hơn.
    *   **Xử lý và Phân tích Dữ liệu:**
        *   `pandas`: Cực kỳ mạnh mẽ cho việc xử lý chuỗi thời gian (time-series data), tính toán và quản lý dữ liệu nến (OHLCV).
        *   `NumPy`: Nền tảng cho tính toán khoa học, được pandas sử dụng và hữu ích cho các phép toán số học hiệu năng cao.
    *   **Tính toán Chỉ báo Kỹ thuật:**
        *   `TA-Lib (python wrapper)`: Thư viện tiêu chuẩn công nghiệp, cung cấp hàng trăm chỉ báo kỹ thuật được tối ưu hóa về tốc độ.
        *   Hoặc `pandas-ta`: Một thư viện khác tích hợp tốt với Pandas, dễ sử dụng hơn TA-Lib trong một số trường hợp.
    *   **Xử lý Bất đồng bộ / Đa luồng (Khuyến nghị):**
        *   `asyncio` hoặc `threading`: Cần thiết để chạy các tác vụ nền (lấy dữ liệu, phân tích) liên tục mà không chặn giao diện người dùng Streamlit. Dữ liệu từ các tác vụ nền này sẽ cần được cập nhật vào trạng thái của Streamlit (Session State) để hiển thị.

### 1.2. Frontend (Giao diện Người dùng - Web-based)
*   **Framework:** **Streamlit**
    *   **Lý do:** Theo yêu cầu mới của người dùng. Streamlit cho phép xây dựng giao diện người dùng web tương tác cho các ứng dụng dữ liệu bằng Python một cách nhanh chóng và dễ dàng. Nó tích hợp tốt với hệ sinh thái khoa học dữ liệu Python, phù hợp cho việc hiển thị dữ liệu, biểu đồ và nhận input từ người dùng. Giao diện sẽ được truy cập qua trình duyệt web trên mạng cục bộ.
    *   **Ưu điểm:** Phát triển nhanh, dễ học, không cần kiến thức frontend phức tạp (HTML/CSS/JS), tích hợp tốt với thư viện Python data science.
    *   **Nhược điểm:** Ít tùy biến giao diện chi tiết hơn so với framework GUI desktop hoặc web frontend chuyên dụng, hoạt động như một web server, quản lý trạng thái và cập nhật real-time cần được xử lý cẩn thận (ví dụ: dùng Session State, caching, auto-refresh).
*   **Thư viện hỗ trợ (Tùy chọn):**
    *   `plotly` hoặc `matplotlib`: Streamlit tích hợp sẵn với nhiều thư viện vẽ biểu đồ, giúp trực quan hóa dữ liệu giá và chỉ báo.

### 1.3. Lưu trữ Cấu hình
*   **Phương pháp:** **File cấu hình (JSON hoặc YAML)**
    *   **Lý do:** Đơn giản, dễ đọc, dễ chỉnh sửa, phù hợp cho cấu hình không quá phức tạp (chế độ, vốn, TP/lệnh, SL/lệnh) trong môi trường chạy cục bộ.
    *   **Thay thế:** SQLite nếu cần lưu trữ lịch sử hoặc cấu hình phức tạp hơn.

## 2. Kiến trúc Hệ thống (System Architecture)

Kiến trúc được điều chỉnh để phù hợp với Streamlit, vẫn đảm bảo tách biệt các mối quan tâm và xử lý nền.

### 2.1. Mô hình Tổng thể
Ứng dụng sẽ bao gồm một tiến trình chính chạy Streamlit server và các luồng/tác vụ nền để xử lý việc lấy dữ liệu và phân tích.

*   **Tiến trình Streamlit (Main Process):**
    *   Chạy Streamlit server, phục vụ giao diện người dùng qua trình duyệt web.
    *   Xử lý các tương tác của người dùng (nhập cấu hình, chọn chế độ).
    *   Đọc dữ liệu (giá, đề xuất, log) từ trạng thái được cập nhật bởi các tác vụ nền (ví dụ: Streamlit Session State, Cache) và hiển thị lên giao diện.
    *   Kích hoạt/quản lý các tác vụ nền khi ứng dụng khởi động hoặc khi cấu hình thay đổi.
*   **Luồng/Tác vụ Backend (Worker Threads / Async Tasks):**
    *   **Module Kết nối Binance:** (Tương tự kiến trúc trước) Chạy nền, kết nối API, lấy dữ liệu OHLCV liên tục.
    *   **Module Phân tích Kỹ thuật:** (Tương tự kiến trúc trước) Chạy nền, nhận dữ liệu, tính toán chỉ báo dựa trên chế độ (Scalp/Swing).
    *   **Module Chiến lược Giao dịch:** (Tương tự kiến trúc trước) Chạy nền, nhận kết quả phân tích, áp dụng logic chiến lược, tạo đề xuất.
    *   **Module Cập nhật Trạng thái (State Update):** Các tác vụ nền sẽ cập nhật dữ liệu mới nhất (giá, đề xuất, log) vào một cơ chế chia sẻ trạng thái mà tiến trình Streamlit có thể truy cập (ví dụ: Streamlit Session State, một cache đơn giản, hoặc file tạm). Giao diện Streamlit sẽ tự động làm mới (auto-refresh) hoặc người dùng làm mới thủ công để thấy dữ liệu mới nhất.

### 2.2. Sơ đồ Kiến trúc (Conceptual - Streamlit)

```
+-------------------+      +-------------------------+      +----------------------+
|   Binance API     |<---->| Module Kết nối Binance  |<---->(Dữ liệu thô)
| (REST/WebSocket)  |      | (Background Task/Thread) |      +----------+-----------+
+-------------------+      +-------------------------+                 |
                                                                       V
+-------------------+      +-------------------------+      +----------------------+
| File Cấu hình     |<---->| Module Chiến lược       |<---->(Kết quả P.tích)
| (JSON/YAML)       |      | (Background Task/Thread) |      +----------+-----------+
+-------------------+      +----------+--------------+                 ^      |
       ^                         | (Đề xuất)                             |      V
       |                         V                                       |
       |             +-----------+-----------+                 +----------+-----------+
       |             | Streamlit Session State |<--------------| Module Phân tích KT  |
       |             | (hoặc Cache/Shared Mem) |                 | (Background Task/Thread)|
       |             +-----------+-----------+                 +----------------------+
       |                         ^         |
       | (Đọc cấu hình)          |         | (Đọc dữ liệu để hiển thị)
       V                         |         V
+---------------------+      +---+---------------------+
| Trình duyệt Web     |<---->| Streamlit Server        |
| (UI: http://localhost)|      | (Main Process)          |
+---------------------+      +-------------------------+
```

### 2.3. Luồng Dữ liệu Chính (Streamlit)
1.  **Khởi chạy:** Người dùng chạy script Streamlit (`streamlit run app.py`).
2.  **Khởi tạo:** Streamlit server khởi động. Các tác vụ nền (kết nối, phân tích, chiến lược) được khởi chạy.
3.  **Kết nối & Lấy dữ liệu:** Module Kết nối lấy dữ liệu từ Binance.
4.  **Phân tích & Chiến lược:** Dữ liệu được xử lý qua Module Phân tích và Chiến lược.
5.  **Cập nhật Trạng thái:** Kết quả (giá mới nhất, đề xuất mới, log) được các tác vụ nền ghi vào Streamlit Session State hoặc cơ chế chia sẻ khác.
6.  **Hiển thị UI:** Người dùng truy cập ứng dụng qua trình duyệt. Streamlit đọc trạng thái hiện tại và hiển thị giao diện.
7.  **Tương tác Người dùng:** Người dùng thay đổi cấu hình (chế độ, vốn, TP/SL) trên giao diện.
8.  **Cập nhật Cấu hình:** Streamlit cập nhật cấu hình vào Session State và/hoặc file cấu hình. Các tác vụ nền đọc cấu hình mới này để điều chỉnh hoạt động.
9.  **Làm mới Giao diện:** Giao diện Streamlit tự động làm mới định kỳ hoặc khi có tương tác, đọc lại trạng thái mới nhất để hiển thị cập nhật.

## 3. Lý do Lựa chọn (Cập nhật cho Streamlit)
*   **Phát triển nhanh:** Streamlit cho phép tạo giao diện web nhanh chóng bằng Python, giảm thời gian phát triển so với GUI desktop.
*   **Dễ sử dụng & Tích hợp:** Phù hợp với người dùng Python, tích hợp tốt với thư viện data science.
*   **Web-based:** Dễ dàng truy cập cục bộ qua trình duyệt, không cần cài đặt ứng dụng riêng.
*   **Hiệu năng Backend:** Kiến trúc vẫn giữ các tác vụ xử lý nặng ở backend (Python với thư viện tối ưu), đảm bảo hiệu năng phân tích.
*   **Khả năng bảo trì:** Tách biệt logic backend và frontend (Streamlit UI) vẫn được duy trì ở mức độ nhất định.
*   **Phù hợp yêu cầu:** Đáp ứng yêu cầu chạy cục bộ, hiển thị thông tin và tương tác cơ bản. Có thể dễ dàng chia sẻ trong mạng nội bộ.

