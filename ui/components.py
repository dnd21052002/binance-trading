import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import List, Dict, Optional
from datetime import datetime

from modules.data_models import TradingSuggestion, TokenPrice

def render_header():
    """Render header của ứng dụng"""
    st.set_page_config(
        page_title="Binance Futures AI Bot",
        page_icon="📈",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.title("🤖 Binance Futures AI Bot")
    st.markdown("---")

def render_connection_status(is_connected: bool):
    """Render trạng thái kết nối"""
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("Trạng thái kết nối")
    
    with col2:
        if is_connected:
            st.success("✅ Đã kết nối Binance")
        else:
            st.error("❌ Chưa kết nối Binance")

def render_token_watchlist(prices: Dict[str, TokenPrice]):
    """Render danh sách giá token"""
    st.subheader("📊 Giá Token Hiện tại")
    
    if not prices:
        st.info("Đang tải dữ liệu giá...")
        return
    
    # Tạo 3 cột cho 3 token
    cols = st.columns(3)
    
    tokens = ["BTCUSDT", "ETHUSDT", "SOLUSDT"]
    token_names = {"BTCUSDT": "BTC", "ETHUSDT": "ETH", "SOLUSDT": "SOL"}
    
    for i, token in enumerate(tokens):
        with cols[i]:
            if token in prices:
                price_data = prices[token]
                
                # Xác định màu sắc dựa trên thay đổi 24h
                color = "green" if price_data.change_24h >= 0 else "red"
                change_symbol = "+" if price_data.change_24h >= 0 else ""
                
                st.metric(
                    label=f"{token_names[token]}/USDT",
                    value=f"${price_data.price:,.2f}",
                    delta=f"{change_symbol}{price_data.change_24h:.2f}%"
                )
            else:
                st.metric(
                    label=f"{token_names[token]}/USDT",
                    value="Loading...",
                    delta=None
                )

def render_user_configuration():
    """Render cấu hình người dùng"""
    st.subheader("⚙️ Cấu hình Giao dịch")
    
    # Khởi tạo session state nếu chưa có
    if 'trading_mode' not in st.session_state:
        st.session_state.trading_mode = "Scalp"
    if 'available_capital' not in st.session_state:
        st.session_state.available_capital = 10.0
    
    # Tạo 2 cột
    col1, col2 = st.columns(2)
    
    with col1:
        # Chế độ giao dịch
        current_mode_index = 0 if st.session_state.trading_mode == "Scalp" else 1
        trading_mode = st.radio(
            "Chế độ Giao dịch:",
            options=["Scalp", "Swing"],
            index=current_mode_index,
            help="Scalp: Giao dịch ngắn hạn, lợi nhuận nhỏ, tần suất cao\nSwing: Giao dịch dài hạn, lợi nhuận lớn, tần suất thấp"
        )
        
        # Cập nhật session state
        st.session_state.trading_mode = trading_mode
        
        # Vốn khả dụng
        available_capital = st.number_input(
            "Vốn khả dụng (USDT):",
            min_value=10.0,
            max_value=100000.0,
            value=st.session_state.available_capital,
            step=1.0,
            help="Tổng số vốn bạn muốn sử dụng cho bot"
        )
        
        # Cập nhật session state
        st.session_state.available_capital = available_capital
    
    with col2:
        # Lợi nhuận mục tiêu
        if trading_mode == "Scalp":
            default_profit = 3.0
            profit_help = "Mục tiêu lợi nhuận cho mỗi lệnh Scalp (thường 3-5 USDT)"
        else:
            default_profit = 10.0
            profit_help = "Mục tiêu lợi nhuận cho mỗi lệnh Swing (thường 10-20 USDT)"
        
        target_profit = st.number_input(
            "Lợi nhuận mục tiêu/lệnh (USDT):",
            min_value=1.0,
            max_value=100.0,
            value=default_profit,
            step=1.0,
            help=profit_help
        )
        
        # Lỗ tối đa
        if trading_mode == "Scalp":
            default_loss = 2.0
            loss_help = "Mức lỗ tối đa cho mỗi lệnh Scalp (thường 1-5 USDT)"
        else:
            default_loss = 5.0
            loss_help = "Mức lỗ tối đa cho mỗi lệnh Swing (thường 5-10 USDT)"
        
        max_loss = st.number_input(
            "Lỗ tối đa/lệnh (USDT):",
            min_value=1.0,
            max_value=100.0,
            value=default_loss,
            step=1.0,
            help=loss_help
        )
    
    # Nút lưu cấu hình
    if st.button("💾 Lưu Cấu hình", type="primary"):
        return {
            "trading_mode": trading_mode,
            "available_capital": available_capital,
            "target_profit_per_trade": target_profit,
            "max_loss_per_trade": max_loss
        }
    
    return None

def render_trading_suggestions(suggestions: List[TradingSuggestion]):
    """Render bảng đề xuất giao dịch"""
    st.subheader("💡 Đề xuất Giao dịch")
    
    if not suggestions:
        st.info("Chưa có đề xuất giao dịch nào. Đang phân tích thị trường...")
        return
    
    # Chuyển đổi suggestions thành DataFrame
    data = []
    for suggestion in reversed(suggestions):  # Hiển thị mới nhất trước
        data.append(suggestion.to_dict())
    
    df = pd.DataFrame(data)
    
    # Tùy chỉnh hiển thị
    st.dataframe(
        df,
        use_container_width=True,
        hide_index=True,
        column_config={
            "timestamp": st.column_config.TextColumn("Thời gian", width="small"),
            "mode": st.column_config.TextColumn("Chế độ", width="small"),
            "symbol": st.column_config.TextColumn("Token", width="small"),
            "direction": st.column_config.TextColumn("Hướng", width="small"),
            "entry_price": st.column_config.TextColumn("Entry", width="medium"),
            "stop_loss": st.column_config.TextColumn("SL", width="medium"),
            "take_profit": st.column_config.TextColumn("TP", width="medium"),
            "leverage": st.column_config.TextColumn("Leverage", width="small"),
            "reason": st.column_config.TextColumn("Lý do", width="large")
        }
    )

def render_logs(logs: List[str]):
    """Render log messages"""
    st.subheader("📝 Log Hoạt động")
    
    if not logs:
        st.info("Chưa có log nào.")
        return
    
    # Hiển thị logs trong container có thể scroll
    with st.container():
        # Hiển thị logs mới nhất trước
        for log in reversed(logs[-10:]):  # Chỉ hiển thị 10 log gần nhất
            st.text(log)

def render_price_chart(symbol: str, df: pd.DataFrame):
    """Render biểu đồ giá với chỉ báo"""
    if df is None or len(df) == 0:
        st.info(f"Không có dữ liệu biểu đồ cho {symbol}")
        return
    
    # Tạo subplot với 2 hàng
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.1,
        subplot_titles=(f'{symbol} Price', 'Volume'),
        row_width=[0.7, 0.3]
    )
    
    # Candlestick chart
    fig.add_trace(
        go.Candlestick(
            x=df['timestamp'],
            open=df['open'],
            high=df['high'],
            low=df['low'],
            close=df['close'],
            name='Price'
        ),
        row=1, col=1
    )
    
    # Volume chart
    fig.add_trace(
        go.Bar(
            x=df['timestamp'],
            y=df['volume'],
            name='Volume',
            marker_color='rgba(158,202,225,0.8)'
        ),
        row=2, col=1
    )
    
    # Cập nhật layout
    fig.update_layout(
        title=f'{symbol} Price Chart',
        yaxis_title='Price (USDT)',
        yaxis2_title='Volume',
        xaxis_rangeslider_visible=False,
        height=600
    )
    
    st.plotly_chart(fig, use_container_width=True)

def render_sidebar_controls():
    """Render các điều khiển trong sidebar"""
    st.sidebar.header("🎛️ Điều khiển Bot")
    
    # Nút bắt đầu/dừng bot
    if st.sidebar.button("🚀 Bắt đầu Bot", type="primary"):
        return "start"
    
    if st.sidebar.button("⏹️ Dừng Bot"):
        return "stop"
    
    # Nút làm mới dữ liệu
    if st.sidebar.button("🔄 Làm mới dữ liệu"):
        return "refresh"
    
    # Cài đặt nâng cao
    st.sidebar.header("⚙️ Cài đặt nâng cao")
    
    # Interval cập nhật
    update_interval = st.sidebar.slider(
        "Interval cập nhật (giây):",
        min_value=10,
        max_value=300,
        value=30,
        step=10
    )
    
    # Số lượng đề xuất hiển thị
    max_suggestions = st.sidebar.slider(
        "Số đề xuất hiển thị:",
        min_value=5,
        max_value=50,
        value=10,
        step=5
    )
    
    return {
        "update_interval": update_interval,
        "max_suggestions": max_suggestions
    }

def render_statistics(suggestions: List[TradingSuggestion]):
    """Render thống kê đề xuất"""
    if not suggestions:
        return
    
    st.subheader("📈 Thống kê")
    
    # Tạo 4 cột cho metrics
    col1, col2, col3, col4 = st.columns(4)
    
    # Tổng số đề xuất
    total_suggestions = len(suggestions)
    
    # Đếm theo hướng
    long_count = sum(1 for s in suggestions if s.direction == "LONG")
    short_count = sum(1 for s in suggestions if s.direction == "SHORT")
    
    # Đếm theo chế độ
    scalp_count = sum(1 for s in suggestions if s.mode == "Scalp")
    swing_count = sum(1 for s in suggestions if s.mode == "Swing")
    
    with col1:
        st.metric("Tổng đề xuất", total_suggestions)
    
    with col2:
        st.metric("LONG", long_count)
    
    with col3:
        st.metric("SHORT", short_count)
    
    with col4:
        st.metric("Scalp/Swing", f"{scalp_count}/{swing_count}")

def show_info_panel():
    """Hiển thị panel thông tin hướng dẫn"""
    with st.expander("ℹ️ Hướng dẫn sử dụng", expanded=False):
        st.markdown("""
        ### Cách sử dụng Bot Trading AI:
        
        1. **Cấu hình giao dịch:**
           - Chọn chế độ Scalp (ngắn hạn) hoặc Swing (dài hạn)
           - Nhập vốn khả dụng và mục tiêu lợi nhuận/lỗ
           - Nhấn "Lưu cấu hình"
        
        2. **Khởi động bot:**
           - Nhấn "Bắt đầu Bot" trong sidebar
           - Bot sẽ tự động phân tích thị trường và tạo đề xuất
        
        3. **Theo dõi đề xuất:**
           - Xem các đề xuất giao dịch trong bảng
           - Mỗi đề xuất bao gồm: Entry, SL, TP, Leverage, Lý do
        
        4. **Lưu ý quan trọng:**
           - Bot chỉ đưa ra đề xuất, không tự động giao dịch
           - Bạn cần tự quyết định có thực hiện giao dịch hay không
           - Luôn quản lý rủi ro và không đầu tư quá khả năng chịu đựng
        """)
        
        st.warning("⚠️ **Tuyên bố miễn trừ trách nhiệm:** Bot này chỉ là công cụ hỗ trợ phân tích kỹ thuật. Không đảm bảo lợi nhuận và mọi rủi ro giao dịch thuộc về người dùng.")

def render_footer():
    """Render footer"""
    st.markdown("---")
    st.markdown(
        "<div style='text-align: center; color: gray;'>"
        "Binance Futures AI Bot v1.1 - Phát triển bởi AI Assistant"
        "</div>",
        unsafe_allow_html=True
    ) 