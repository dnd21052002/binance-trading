# Mockup Giao diện Người dùng (UI) - Bot Trading AI Binance Futures (v1.1)

**Mục đích:** Mô tả bố cục và các thành phần chính của giao diện người dùng cho bot trading, bao gồm lựa chọn chế độ Scalp/Swing.

**Loại giao diện:** Giao diện đồ họa (GUI) cho ứng dụng Desktop.

**Bố cục Tổng thể:**

```
+--------------------------------------------------------------------------+
| [APP TITLE: Binance Futures AI Bot] | [Status: Connected to Binance ✅] |
+--------------------------------------------------------------------------+
| Token Watchlist                     | User Configuration                 |
| +---------------------------------+ | +--------------------------------+ |
| | BTC/USDT: 68,500.50           | | | Trading Mode:                  | |
| | ETH/USDT: 3,800.75            | | |  (*) Scalp   ( ) Swing         | |
| | SOL/USDT: 165.20              | | | Available Capital (USDT):    | |
| |                                 | | | [ 10000_________ ] Input    | |
| | (Prices update in real-time)    | | | Target Profit/Trade (USDT):| |
| |                                 | | | [ 50 (Scalp)____ ] Input    | |
| |                                 | | | Max Loss/Trade (USDT):     | |
| |                                 | | | [ 25 (Scalp)____ ] Input    | |
| +---------------------------------+ | +--------------------------------+ |
+--------------------------------------------------------------------------+
| Trading Suggestions                                                      |
+--------------------------------------------------------------------------+
| [Timestamp] | Mode  | Token | Direction | Entry (Limit) | SL    | TP    | Leverage | Reason                                      |
|-------------|-------|-------|-----------|---------------|-------|-------|----------|---------------------------------------------|
| 10:35:12    | Scalp | BTC   | LONG      | 68450.00      | 68200 | 69000 | 10x      | RSI(5m)>70, MACD cross(1m), Price>MA20(15m) |
| 10:33:50    | Swing | ETH   | SHORT     | 3810.50       | 3835  | 3750  | 15x      | Price below BB(4h), RSI(1h) < 30, Trend(1d) Down |
| 10:28:05    | Scalp | SOL   | LONG      | 164.80        | 163.5 | 168.0 | 12x      | Breakout resistance(5m), Volume spike(1m)   |
| ...         | ...   | ...   | ...       | ...           | ...   | ...   | ...      | ...                                         |
+--------------------------------------------------------------------------+
| Log/Status Messages                                                      |
+--------------------------------------------------------------------------+
| [10:35:12] New LONG suggestion for BTC (Scalp) generated.                |
| [10:33:50] New SHORT suggestion for ETH (Swing) generated.               |
| [10:30:00] Fetching latest market data...                                |
| [10:29:55] Configuration saved (Mode: Scalp).                           |
| [10:28:05] New LONG suggestion for SOL (Scalp) generated.                |
| [10:25:01] Connected to Binance API successfully.                       |
+--------------------------------------------------------------------------+
```

**Mô tả Chi tiết các Thành phần:**

1.  **Header:**
    *   **Tiêu đề ứng dụng:** Hiển thị tên của bot (ví dụ: "Binance Futures AI Bot").
    *   **Trạng thái Kết nối:** Hiển thị trạng thái kết nối hiện tại với API Binance (ví dụ: "Connected ✅", "Connecting...", "Disconnected ❌").

2.  **Token Watchlist:**
    *   Hiển thị danh sách các token được theo dõi (BTC, ETH, SOL) cùng với giá thị trường hiện tại (USDT).
    *   Giá được cập nhật gần với thời gian thực.

3.  **User Configuration:**
    *   **Trading Mode:** Cho phép người dùng chọn chế độ giao dịch mong muốn bằng các nút radio: "Scalp" hoặc "Swing". Lựa chọn này sẽ ảnh hưởng đến logic phân tích và chiến lược.
    *   **Available Capital (USDT):** Ô nhập liệu cho người dùng nhập tổng số vốn khả dụng.
    *   **Target Profit/Trade (USDT):** Ô nhập liệu cho người dùng đặt mức lợi nhuận mục tiêu cho mỗi lệnh. Có thể hiển thị gợi ý dựa trên chế độ đã chọn (ví dụ: "50 (Scalp)").
    *   **Max Loss/Trade (USDT):** Ô nhập liệu cho người dùng đặt mức lỗ tối đa chấp nhận cho mỗi lệnh. Có thể hiển thị gợi ý dựa trên chế độ đã chọn (ví dụ: "25 (Scalp)").

4.  **Trading Suggestions:**
    *   Hiển thị danh sách các đề xuất giao dịch được tạo ra bởi bot dưới dạng bảng.
    *   **Các cột bao gồm:**
        *   `Timestamp`: Thời gian đề xuất được tạo.
        *   `Mode`: Chế độ giao dịch của đề xuất (Scalp/Swing).
        *   `Token`: Mã token (BTC, ETH, SOL).
        *   `Direction`: Hướng lệnh (LONG/SHORT).
        *   `Entry (Limit)`: Giá vào lệnh đề xuất.
        *   `SL`: Giá dừng lỗ đề xuất.
        *   `TP`: Giá chốt lời đề xuất.
        *   `Leverage`: Mức đòn bẩy đề xuất.
        *   `Reason`: Giải thích ngắn gọn về lý do kỹ thuật đưa ra đề xuất (ví dụ: các tín hiệu chỉ báo chính).
    *   Danh sách được cập nhật khi có đề xuất mới, đề xuất mới nhất hiển thị ở trên cùng.

5.  **Log/Status Messages:**
    *   Hiển thị các thông báo trạng thái, log hoạt động của bot, lỗi (nếu có), và thông báo về các đề xuất mới được tạo (bao gồm cả chế độ).
    *   Giúp người dùng theo dõi hoạt động của bot.

