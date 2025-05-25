# Tài liệu Đặc tả Yêu cầu Phần mềm (SRS) - Bot Trading AI Binance Futures

**Phiên bản:** 1.1
**Ngày:** 25 tháng 5 năm 2025

## Mục lục
1.  Giới thiệu
    1.1. Mục đích
    1.2. Phạm vi
    1.3. Định nghĩa, Từ viết tắt và Chữ viết tắt
    1.4. Tài liệu tham khảo
    1.5. Tổng quan
2.  Mô tả Tổng thể
    2.1. Bối cảnh Sản phẩm
    2.2. Chức năng Sản phẩm
    2.3. Đặc điểm Người dùng
    2.4. Môi trường Vận hành
    2.5. Ràng buộc Thiết kế và Triển khai
    2.6. Giả định và Phụ thuộc
3.  Yêu cầu Cụ thể
    3.1. Yêu cầu Chức năng
        3.1.1. Kết nối và Lấy Dữ liệu Binance
        3.1.2. Phân tích Kỹ thuật Đa khung thời gian
        3.1.3. Cấu hình Người dùng
        3.1.4. Logic Chiến lược Giao dịch
        3.1.5. Tạo Đề xuất Giao dịch
        3.1.6. Giao diện Người dùng (UI)
    3.2. Yêu cầu Giao diện Bên ngoài
        3.2.1. Giao diện Người dùng (UI)
        3.2.2. Giao diện Phần cứng
        3.2.3. Giao diện Phần mềm (API Binance)
        3.2.4. Giao diện Truyền thông
    3.3. Yêu cầu Phi chức năng
        3.3.1. Yêu cầu Hiệu năng
        3.3.2. Yêu cầu Bảo mật
        3.3.3. Yêu cầu Độ tin cậy
        3.3.4. Yêu cầu Khả năng Bảo trì
        3.3.5. Yêu cầu Khả năng Sử dụng
4.  Các Yêu cầu Khác

---

## 1. Giới thiệu

### 1.1. Mục đích
Tài liệu này mô tả các yêu cầu phần mềm cho hệ thống Bot Trading AI Binance Futures (sau đây gọi là "Hệ thống"). Mục đích của Hệ thống là cung cấp các đề xuất giao dịch futures trên sàn Binance cho các token BTC, SOL, ETH dựa trên phân tích kỹ thuật thời gian thực và cấu hình do người dùng xác định.

### 1.2. Phạm vi
Hệ thống sẽ thực hiện các chức năng sau:
*   Kết nối với API Binance Futures để lấy dữ liệu thị trường thời gian thực (giá, khối lượng) cho các cặp BTCUSDT, SOLUSDT, ETHUSDT.
*   Phân tích dữ liệu trên nhiều khung thời gian (1m, 5m, 15m, 30m, 1h, 4h, 1d).
*   Cho phép người dùng lựa chọn chế độ giao dịch: **Scalp** (ngắn hạn) hoặc **Swing** (dài hạn hơn).
*   Cho phép người dùng nhập vốn, mức lợi nhuận mong muốn và mức lỗ tối đa cho mỗi lệnh.
*   Áp dụng các chỉ báo và chiến lược phân tích kỹ thuật **phù hợp với chế độ giao dịch đã chọn** để xác định các cơ hội giao dịch (Long/Short).
*   Đưa ra các đề xuất giao dịch chi tiết bao gồm điểm vào lệnh (entry), dừng lỗ (stop loss), chốt lời (take profit), mức đòn bẩy đề xuất, và **chế độ giao dịch tương ứng (Scalp/Swing)**.
*   Cung cấp lý do phân tích kỹ thuật cho mỗi đề xuất.
*   Hoạt động ban đầu trên môi trường cục bộ (local laptop).

**Ngoài phạm vi:**
*   Tự động thực hiện giao dịch trên Binance (giai đoạn đầu chỉ đưa ra đề xuất).
*   Quản lý danh mục đầu tư phức tạp.
*   Phân tích cơ bản hoặc tin tức thị trường.
*   Hỗ trợ các sàn giao dịch khác ngoài Binance Futures.
*   Hỗ trợ các token khác ngoài BTC, SOL, ETH.
*   Triển khai trên môi trường cloud (sẽ xem xét trong giai đoạn sau).

### 1.3. Định nghĩa, Từ viết tắt và Chữ viết tắt
*   **AI:** Artificial Intelligence (Trí tuệ nhân tạo)
*   **API:** Application Programming Interface (Giao diện lập trình ứng dụng)
*   **BTC:** Bitcoin
*   **ETH:** Ethereum
*   **SOL:** Solana
*   **USDT:** Tether (một loại stablecoin)
*   **Futures:** Hợp đồng tương lai
*   **SRS:** Software Requirements Specification (Đặc tả Yêu cầu Phần mềm)
*   **UI:** User Interface (Giao diện người dùng)
*   **OHLCV:** Open, High, Low, Close, Volume (Dữ liệu nến)
*   **MA:** Moving Average (Đường trung bình động)
*   **RSI:** Relative Strength Index (Chỉ số sức mạnh tương đối)
*   **MACD:** Moving Average Convergence Divergence (Trung bình động hội tụ phân kỳ)
*   **SL:** Stop Loss (Dừng lỗ)
*   **TP:** Take Profit (Chốt lời)
*   **Entry:** Điểm vào lệnh
*   **Leverage:** Đòn bẩy
*   **Long:** Lệnh mua (kỳ vọng giá tăng)
*   **Short:** Lệnh bán (kỳ vọng giá giảm)
*   **Scalp:** Phong cách giao dịch tần suất cao, nhằm kiếm lợi nhuận nhỏ từ các biến động giá ngắn hạn.
*   **Swing:** Phong cách giao dịch nhằm nắm bắt các "dao động" giá lớn hơn trong một xu hướng, thường kéo dài vài ngày đến vài tuần.

### 1.4. Tài liệu tham khảo
*   Yêu cầu ban đầu của người dùng (bao gồm yêu cầu bổ sung về Scalp/Swing).
*   Tài liệu API Binance Futures.
*   Danh sách tính năng chi tiết (features.md - v1.1).

### 1.5. Tổng quan
Tài liệu này được chia thành các phần chính: Giới thiệu, Mô tả Tổng thể, Yêu cầu Cụ thể (bao gồm chức năng và phi chức năng), và Các Yêu cầu Khác. Phần Mô tả Tổng thể cung cấp cái nhìn chung về sản phẩm, người dùng và môi trường hoạt động. Phần Yêu cầu Cụ thể đi sâu vào chi tiết các chức năng, giao diện, hiệu năng, bảo mật và các yêu cầu phi chức năng khác.

## 2. Mô tả Tổng thể

### 2.1. Bối cảnh Sản phẩm
Hệ thống là một ứng dụng độc lập, chạy trên máy tính cá nhân của người dùng. Nó tương tác với API công khai của Binance Futures để lấy dữ liệu và cung cấp thông tin phân tích, đề xuất giao dịch cho người dùng thông qua giao diện đồ họa.

### 2.2. Chức năng Sản phẩm
Các chức năng chính của sản phẩm bao gồm:
*   **Phân tích Dữ liệu Thời gian thực:** Lấy và xử lý dữ liệu giá OHLCV từ Binance cho BTC, SOL, ETH trên các khung thời gian 1m, 5m, 15m, 30m, 1h, 4h, 1d. Tính toán các chỉ báo kỹ thuật cần thiết.
*   **Cấu hình Giao dịch:** Cho phép người dùng chọn chế độ giao dịch (Scalp/Swing), định nghĩa vốn, mục tiêu lợi nhuận/lệnh, và mức lỗ tối đa/lệnh.
*   **Đề xuất Giao dịch:** Dựa trên phân tích và cấu hình (bao gồm chế độ giao dịch), hệ thống đưa ra các đề xuất Long/Short với thông tin chi tiết (Entry, SL, TP, Leverage, Mode) và lý do.
*   **Giao diện Người dùng:** Hiển thị dữ liệu, cấu hình (bao gồm lựa chọn chế độ), và các đề xuất giao dịch một cách rõ ràng.

(Chi tiết xem trong file features.md v1.1 và Mục 3.1 Yêu cầu Chức năng)

### 2.3. Đặc điểm Người dùng
Người dùng mục tiêu là các nhà giao dịch cá nhân (traders) có kiến thức cơ bản về giao dịch crypto futures và phân tích kỹ thuật, muốn có một công cụ hỗ trợ đưa ra quyết định giao dịch dựa trên dữ liệu và thuật toán, với khả năng lựa chọn phong cách giao dịch Scalp hoặc Swing.

### 2.4. Môi trường Vận hành
*   **Hệ điều hành:** Windows, macOS, hoặc Linux (cần xác định rõ hơn hoặc đảm bảo tương thích đa nền tảng).
*   **Phần cứng:** Máy tính cá nhân (laptop/desktop) có kết nối internet ổn định.
*   **Phần mềm phụ thuộc:** Có thể yêu cầu cài đặt môi trường chạy (ví dụ: Python) và các thư viện cần thiết.

### 2.5. Ràng buộc Thiết kế và Triển khai
*   **Ngôn ngữ lập trình/Công nghệ:** Sẽ được đề xuất (xem tài liệu tech_stack_architecture.md).
*   **API Binance:** Hệ thống phụ thuộc vào tính khả dụng và các quy tắc của API Binance Futures. Cần tuân thủ giới hạn tỷ lệ yêu cầu (rate limits) của API.
*   **Chạy cục bộ:** Giai đoạn đầu, hệ thống chỉ chạy trên máy cục bộ, không có thành phần server/cloud.
*   **Bảo mật API Key:** Nếu trong tương lai có chức năng đặt lệnh tự động, cần cơ chế bảo mật API key của người dùng.
*   **Không đảm bảo lợi nhuận:** Hệ thống chỉ cung cấp đề xuất dựa trên phân tích kỹ thuật, không đảm bảo lợi nhuận và người dùng chịu trách nhiệm cuối cùng cho quyết định giao dịch của mình.

### 2.6. Giả định và Phụ thuộc
*   Người dùng có tài khoản Binance Futures và hiểu cách sử dụng nền tảng này.
*   Người dùng có kiến thức cơ bản về các khái niệm trading (Long, Short, SL, TP, Leverage, Scalp, Swing).
*   API Binance Futures hoạt động ổn định và cung cấp dữ liệu chính xác.
*   Người dùng có kết nối internet ổn định để hệ thống lấy dữ liệu thời gian thực.

## 3. Yêu cầu Cụ thể

### 3.1. Yêu cầu Chức năng

#### 3.1.1. Kết nối và Lấy Dữ liệu Binance (FUNC-DATA-01)
*   **Mô tả:** Hệ thống phải kết nối đến API Binance Futures và lấy dữ liệu OHLCV cho các cặp BTCUSDT, SOLUSDT, ETHUSDT trên các khung thời gian 1m, 5m, 15m, 30m, 1h, 4h, 1d.
*   **Đầu vào:** Danh sách token, danh sách khung thời gian.
*   **Xử lý:** Gọi API Binance, xử lý phản hồi, lưu trữ/cập nhật dữ liệu cục bộ.
*   **Đầu ra:** Dữ liệu OHLCV được cấu trúc cho từng token và khung thời gian.
*   **Tiêu chí chấp nhận:** Dữ liệu được cập nhật gần với thời gian thực (độ trễ chấp nhận được, ví dụ: vài giây) và chính xác so với dữ liệu trên sàn Binance.

#### 3.1.2. Phân tích Kỹ thuật Đa khung thời gian (FUNC-ANALYSIS-01)
*   **Mô tả:** Hệ thống phải tính toán các chỉ báo kỹ thuật (ví dụ: MA, RSI, MACD, Bollinger Bands - danh sách cụ thể sẽ được hoàn thiện) từ dữ liệu OHLCV đã lấy được trên tất cả các khung thời gian yêu cầu. **Các tham số của chỉ báo và việc ưu tiên khung thời gian có thể được điều chỉnh dựa trên chế độ giao dịch (Scalp/Swing) do người dùng chọn.**
*   **Đầu vào:** Dữ liệu OHLCV, Chế độ giao dịch đã chọn.
*   **Xử lý:** Áp dụng công thức tính toán cho từng chỉ báo trên từng khung thời gian, có thể điều chỉnh tham số hoặc tập trung vào các khung thời gian cụ thể tùy theo chế độ Scalp/Swing.
*   **Đầu ra:** Giá trị của các chỉ báo kỹ thuật.
*   **Tiêu chí chấp nhận:** Các giá trị chỉ báo được tính toán chính xác theo công thức chuẩn. **Việc phân tích thích ứng phù hợp với chế độ giao dịch đã chọn.**

#### 3.1.3. Cấu hình Người dùng (FUNC-CONFIG-01)
*   **Mô tả:** Hệ thống phải cung cấp giao diện cho người dùng **lựa chọn Chế độ Giao dịch (Scalp/Swing)** và nhập các thông số: Vốn hiện có (USDT), Lợi nhuận mục tiêu/lệnh (USDT), Lỗ tối đa/lệnh (USDT).
*   **Đầu vào:** **Lựa chọn chế độ (Scalp/Swing)** và giá trị số do người dùng nhập.
*   **Xử lý:** Xác thực đầu vào (ví dụ: vốn, TP, SL phải là số dương), **lưu trữ lựa chọn chế độ giao dịch**, lưu trữ cấu hình (ví dụ: vào file cấu hình).
*   **Đầu ra:** Cấu hình (bao gồm chế độ giao dịch) được lưu trữ và sẵn sàng sử dụng cho các module khác.
*   **Tiêu chí chấp nhận:** Người dùng có thể dễ dàng nhập/chọn, xem và cập nhật cấu hình. **Người dùng có thể dễ dàng chọn chế độ giao dịch.** Cấu hình được lưu lại giữa các phiên làm việc và **ảnh hưởng đến các module khác (Phân tích, Chiến lược, Đề xuất).**

#### 3.1.4. Logic Chiến lược Giao dịch (FUNC-STRATEGY-01)
*   **Mô tả:** Hệ thống phải triển khai logic chiến lược giao dịch **thích ứng** dựa trên **chế độ giao dịch (Scalp/Swing) được chọn** và tín hiệu từ các chỉ báo kỹ thuật đa khung thời gian để xác định cơ hội vào lệnh Long/Short.
*   **Đầu vào:** Giá trị các chỉ báo kỹ thuật, cấu hình người dùng (vốn, TP, SL), **chế độ giao dịch đã chọn (Scalp/Swing)**.
*   **Xử lý:** Áp dụng các quy tắc logic của chiến lược **phù hợp với chế độ đã chọn** (ví dụ: Scalp ưu tiên khung thời gian thấp, chỉ báo nhạy; Swing ưu tiên khung thời gian cao, xu hướng lớn). Tính toán điểm Entry, SL, TP tiềm năng **với các mục tiêu khác nhau cho Scalp/Swing**. Tính toán mức đòn bẩy đề xuất dựa trên quy tắc quản lý rủi ro.
*   **Đầu ra:** Danh sách các cơ hội giao dịch tiềm năng, **phù hợp với chế độ đã chọn**.
*   **Tiêu chí chấp nhận:** Logic chiến lược được triển khai đúng như thiết kế. Các tính toán quản lý rủi ro phù hợp với cấu hình người dùng. **Logic chiến lược và các tham số (khung thời gian ưu tiên, chỉ báo sử dụng, mục tiêu TP/SL) thay đổi một cách rõ ràng và phù hợp khi người dùng chuyển đổi giữa chế độ Scalp và Swing.**

#### 3.1.5. Tạo Đề xuất Giao dịch (FUNC-SUGGEST-01)
*   **Mô tả:** Với mỗi cơ hội giao dịch được xác định, hệ thống phải tạo và hiển thị một đề xuất chi tiết, **bao gồm cả chế độ giao dịch (Scalp/Swing) mà đề xuất đó thuộc về**.
*   **Đầu vào:** Cơ hội giao dịch tiềm năng từ FUNC-STRATEGY-01.
*   **Xử lý:** Định dạng thông tin đề xuất bao gồm: Token, **Chế độ (Scalp/Swing)**, Hướng (Long/Short), Entry (Limit), SL, TP, Đòn bẩy. Soạn thảo phần giải thích lý do dựa trên các tín hiệu kỹ thuật **và chế độ giao dịch** đã kích hoạt đề xuất.
*   **Đầu ra:** Đề xuất giao dịch (bao gồm thông tin Chế độ) được hiển thị rõ ràng trên UI.
*   **Tiêu chí chấp nhận:** Thông tin đề xuất đầy đủ, chính xác và dễ hiểu. Phần giải thích lý do logic và phù hợp với tín hiệu phân tích và chế độ giao dịch. **Đề xuất hiển thị rõ ràng chế độ giao dịch (Scalp/Swing) tương ứng.**

#### 3.1.6. Giao diện Người dùng (UI) (FUNC-UI-01)
*   **Mô tả:** Hệ thống phải có giao diện người dùng (UI) để hiển thị thông tin và cho phép tương tác.
*   **Chức năng con:**
    *   Hiển thị trạng thái kết nối API Binance.
    *   Hiển thị giá hiện tại của các token.
    *   **Khu vực cho phép người dùng chọn Chế độ Giao dịch (Scalp/Swing).**
    *   Khu vực nhập và hiển thị cấu hình người dùng (vốn, TP/lệnh, SL/lệnh).
    *   Khu vực hiển thị danh sách các đề xuất giao dịch mới nhất, bao gồm tất cả thông tin chi tiết (kể cả chế độ) và lý do.
    *   (Tùy chọn) Hiển thị biểu đồ giá cơ bản với một số chỉ báo.
*   **Tiêu chí chấp nhận:** Giao diện trực quan, dễ sử dụng, thông tin được trình bày rõ ràng, cập nhật kịp thời. **Người dùng có thể dễ dàng chọn chế độ giao dịch.**

### 3.2. Yêu cầu Giao diện Bên ngoài

#### 3.2.1. Giao diện Người dùng (UI)
*   Giao diện sẽ được thiết kế (mockup) ở bước sau. Ưu tiên sự rõ ràng, dễ đọc, dễ thao tác. Sẽ là giao diện đồ họa (GUI).

#### 3.2.2. Giao diện Phần cứng
*   Không có yêu cầu giao diện phần cứng đặc biệt ngoài máy tính cá nhân tiêu chuẩn và kết nối mạng.

#### 3.2.3. Giao diện Phần mềm (API Binance)
*   Hệ thống sẽ sử dụng REST API hoặc WebSocket API của Binance Futures để lấy dữ liệu thị trường (OHLCV, giá hiện tại).
*   Hệ thống phải tuân thủ các quy tắc, định dạng dữ liệu và giới hạn tốc độ (rate limits) do Binance quy định.
*   Cần xử lý các lỗi kết nối hoặc lỗi phản hồi từ API Binance một cách hợp lý.

#### 3.2.4. Giao diện Truyền thông
*   Hệ thống yêu cầu kết nối Internet (HTTPS) để giao tiếp với API Binance.

### 3.3. Yêu cầu Phi chức năng

#### 3.3.1. Yêu cầu Hiệu năng (PERF-01)
*   **Phân tích thời gian thực:** Dữ liệu thị trường và các chỉ báo kỹ thuật cần được cập nhật với độ trễ thấp (ví dụ: dưới 5 giây so với thời gian thực của sàn) để đảm bảo tính kịp thời của phân tích, đặc biệt quan trọng cho chế độ Scalp.
*   **Phản hồi UI:** Giao diện người dùng phải phản hồi nhanh chóng với các thao tác của người dùng (ví dụ: nhập cấu hình, chọn chế độ, xem đề xuất).
*   **Sử dụng tài nguyên:** Hệ thống nên hoạt động hiệu quả, không chiếm dụng quá nhiều CPU, bộ nhớ hoặc băng thông mạng của máy người dùng.

#### 3.3.2. Yêu cầu Bảo mật (SEC-01)
*   **API Key (Nếu có):** Nếu trong tương lai tích hợp chức năng đặt lệnh, API key và secret key của người dùng phải được lưu trữ an toàn (ví dụ: mã hóa) trên máy cục bộ và không được truyền đi nếu không cần thiết.
*   **Dữ liệu người dùng:** Cấu hình do người dùng nhập/chọn (chế độ, vốn, TP, SL) cần được bảo vệ, tránh bị truy cập trái phép từ các ứng dụng khác.

#### 3.3.3. Yêu cầu Độ tin cậy (REL-01)
*   **Xử lý lỗi:** Hệ thống cần có cơ chế xử lý lỗi robust, ví dụ: mất kết nối mạng, lỗi API Binance, dữ liệu không hợp lệ. Hệ thống nên cố gắng phục hồi tự động khi có thể (ví dụ: kết nối lại API) và thông báo lỗi rõ ràng cho người dùng khi không thể phục hồi.
*   **Hoạt động ổn định:** Hệ thống nên hoạt động ổn định trong thời gian dài mà không bị treo hoặc crash.

#### 3.3.4. Yêu cầu Khả năng Bảo trì (MAINT-01)
*   **Code rõ ràng:** Mã nguồn cần được viết rõ ràng, có cấu trúc tốt, dễ đọc và dễ hiểu để thuận tiện cho việc sửa lỗi và nâng cấp sau này.
*   **Cấu hình linh hoạt:** Các tham số quan trọng (ví dụ: danh sách chỉ báo sử dụng, tham số của chỉ báo, quy tắc chiến lược) nên dễ dàng cấu hình (ví dụ: qua file config) thay vì hard-code. **Các tham số chiến lược riêng cho chế độ Scalp và Swing nên dễ dàng cấu hình.**

#### 3.3.5. Yêu cầu Khả năng Sử dụng (USE-01)
*   **Dễ cài đặt:** Quá trình cài đặt và thiết lập ban đầu nên đơn giản.
*   **Dễ sử dụng:** Giao diện người dùng (GUI) phải trực quan, dễ hiểu đối với người dùng mục tiêu, **bao gồm cả việc lựa chọn chế độ giao dịch.**
*   **Thông tin rõ ràng:** Các đề xuất giao dịch và lý do phải được trình bày rõ ràng, không gây nhầm lẫn.

## 4. Các Yêu cầu Khác
*   **Tuân thủ pháp luật:** Người dùng chịu trách nhiệm đảm bảo việc sử dụng bot tuân thủ các quy định pháp luật tại khu vực của họ liên quan đến giao dịch tiền điện tử.
*   **Tuyên bố miễn trừ trách nhiệm:** Cần có tuyên bố rõ ràng rằng hệ thống chỉ là công cụ hỗ trợ, không đảm bảo lợi nhuận và mọi rủi ro giao dịch thuộc về người dùng.
