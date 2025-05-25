import streamlit as st
import asyncio
import threading
import time
from datetime import datetime
import sys
import os

# Thêm thư mục gốc vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import các module
from config.config import ConfigManager, TradingConfig
from modules.data_models import DataStore
from modules.binance_connector import BinanceConnector
from modules.technical_analysis import TechnicalAnalyzer
from modules.trading_strategy import TradingStrategy
from ui.components import *
from utils.logger import setup_logger

# Thiết lập logger
logger = setup_logger()

class TradingBot:
    """Main Trading Bot class"""
    
    def __init__(self):
        self.config_manager = ConfigManager()
        self.data_store = DataStore()
        self.binance_connector = BinanceConnector(self.data_store)
        self.technical_analyzer = TechnicalAnalyzer(self.data_store)
        self.trading_strategy = TradingStrategy(self.data_store, self.config_manager, self.technical_analyzer)
        
        self.is_running = False
        self.background_task = None
        self.loop = None
        
    async def start_async(self):
        """Khởi động bot async"""
        try:
            await self.binance_connector.start()
            self.is_running = True
            
            # Lấy cấu hình
            trading_config = self.config_manager.get_trading_config()
            symbols = trading_config.tokens
            timeframes = trading_config.timeframes
            
            # Chạy data fetcher
            await self.binance_connector.run_data_fetcher(symbols, timeframes)
            
        except Exception as e:
            logger.error(f"Lỗi khởi động bot: {e}")
            self.data_store.add_log(f"Lỗi khởi động bot: {str(e)}")
    
    def start_background_task(self):
        """Khởi động task nền"""
        if self.background_task and self.background_task.is_alive():
            return
        
        def run_async_loop():
            try:
                self.loop = asyncio.new_event_loop()
                asyncio.set_event_loop(self.loop)
                self.loop.run_until_complete(self.start_async())
            except Exception as e:
                logger.error(f"Lỗi trong background task: {e}")
            finally:
                if self.loop:
                    self.loop.close()
        
        self.background_task = threading.Thread(target=run_async_loop, daemon=True)
        self.background_task.start()
        self.data_store.add_log("Bot đã được khởi động")
    
    def stop(self):
        """Dừng bot"""
        self.is_running = False
        if self.loop:
            asyncio.run_coroutine_threadsafe(self.binance_connector.stop(), self.loop)
        self.data_store.add_log("Bot đã được dừng")
    
    def run_analysis(self):
        """Chạy phân tích và tạo đề xuất"""
        try:
            trading_config = self.config_manager.get_trading_config()
            symbols = trading_config.tokens
            trading_mode = trading_config.trading_mode
            
            # Debug log
            self.data_store.add_log(f"🎯 Config hiện tại - Mode: {trading_mode}, Vốn: {trading_config.available_capital}")
            
            self.trading_strategy.run_strategy_analysis(symbols, trading_mode)
            
        except Exception as e:
            logger.error(f"Lỗi chạy phân tích: {e}")
            self.data_store.add_log(f"❌ Lỗi phân tích: {str(e)}")

# Khởi tạo bot (singleton)
@st.cache_resource
def get_trading_bot():
    return TradingBot()

def main():
    """Hàm main của ứng dụng Streamlit"""
    
    # Thiết lập page config nếu chưa có
    try:
        st.set_page_config(
            page_title="Binance Futures AI Bot",
            page_icon="📈",
            layout="wide",
            initial_sidebar_state="expanded"
        )
    except:
        pass  # Page config đã được thiết lập
    
    # Render header
    st.title("🤖 Binance Futures AI Bot")
    st.markdown("---")
    
    # Lấy bot instance
    bot = get_trading_bot()
    
    # Hiển thị panel thông tin
    show_info_panel()
    
    # Sidebar controls
    sidebar_action = render_sidebar_controls()
    
    # Xử lý các action từ sidebar
    if sidebar_action == "start":
        bot.start_background_task()
        st.success("Bot đã được khởi động!")
        time.sleep(1)
        st.rerun()
    elif sidebar_action == "stop":
        bot.stop()
        st.success("Bot đã được dừng!")
        time.sleep(1)
        st.rerun()
    elif sidebar_action == "refresh":
        st.rerun()
    
    # Kiểm tra trạng thái kết nối
    is_connected = bot.is_running and bot.binance_connector.session is not None
    render_connection_status(is_connected)
    
    # Hiển thị giá token
    render_token_watchlist(bot.data_store.current_prices)
    
    st.markdown("---")
    
    # Cấu hình người dùng
    config_data = render_user_configuration()
    if config_data:
        # Cập nhật cấu hình
        new_config = TradingConfig(
            trading_mode=config_data["trading_mode"],
            available_capital=config_data["available_capital"],
            target_profit_per_trade=config_data["target_profit_per_trade"],
            max_loss_per_trade=config_data["max_loss_per_trade"]
        )
        bot.config_manager.update_trading_config(new_config)
        st.success("Cấu hình đã được lưu!")
        time.sleep(1)
        st.rerun()
    
    st.markdown("---")
    
    # Tạo 2 cột chính
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Đề xuất giao dịch
        suggestions = bot.data_store.get_latest_suggestions(10)
        render_trading_suggestions(suggestions)
        
        # Thống kê
        if suggestions:
            render_statistics(suggestions)
    
    with col2:
        # Logs
        logs = bot.data_store.get_logs(15)
        render_logs(logs)
        
        # Nút chạy phân tích thủ công
        if st.button("🔍 Chạy Phân tích", type="secondary"):
            if is_connected:
                bot.run_analysis()
                st.success("Đã chạy phân tích!")
                time.sleep(1)
                st.rerun()
            else:
                st.error("Cần khởi động bot trước!")
    
    # Footer
    render_footer()
    
    # Auto refresh mỗi 30 giây nếu bot đang chạy
    if bot.is_running:
        time.sleep(30)
        st.rerun()

if __name__ == "__main__":
    # Chạy ứng dụng
    main() 