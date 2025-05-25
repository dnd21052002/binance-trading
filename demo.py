#!/usr/bin/env python3
"""
Demo script để test các module của Bot Trading AI
"""

import asyncio
import sys
import os

# Thêm thư mục gốc vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config.config import ConfigManager
from modules.data_models import DataStore
from modules.binance_connector import BinanceConnector
from modules.technical_analysis import TechnicalAnalyzer
from modules.trading_strategy import TradingStrategy
from utils.logger import setup_logger

async def test_binance_connection():
    """Test kết nối Binance API"""
    print("🔗 Testing Binance connection...")
    
    data_store = DataStore()
    connector = BinanceConnector(data_store)
    
    try:
        await connector.start()
        
        # Test lấy giá hiện tại
        price = await connector.get_current_price("BTCUSDT")
        if price:
            print(f"✅ BTC price: ${price:,.2f}")
        
        # Test lấy dữ liệu klines
        klines = await connector.get_klines("BTCUSDT", "1h", 5)
        if klines:
            print(f"✅ Got {len(klines)} klines for BTCUSDT 1h")
        
        await connector.stop()
        print("✅ Binance connection test passed!")
        
    except Exception as e:
        print(f"❌ Binance connection test failed: {e}")

def test_config_manager():
    """Test ConfigManager"""
    print("\n⚙️ Testing ConfigManager...")
    
    try:
        config_manager = ConfigManager()
        
        # Test lấy cấu hình
        trading_config = config_manager.get_trading_config()
        print(f"✅ Trading mode: {trading_config.trading_mode}")
        print(f"✅ Capital: ${trading_config.available_capital:,.2f}")
        
        # Test lấy timeframes cho mode
        scalp_tf = config_manager.get_timeframes_for_mode("scalp")
        swing_tf = config_manager.get_timeframes_for_mode("swing")
        print(f"✅ Scalp timeframes: {scalp_tf}")
        print(f"✅ Swing timeframes: {swing_tf}")
        
        print("✅ ConfigManager test passed!")
        
    except Exception as e:
        print(f"❌ ConfigManager test failed: {e}")

def test_data_store():
    """Test DataStore"""
    print("\n💾 Testing DataStore...")
    
    try:
        from datetime import datetime
        from modules.data_models import MarketData, TradingSuggestion
        
        data_store = DataStore()
        
        # Test thêm market data
        market_data = MarketData(
            symbol="BTCUSDT",
            timeframe="1h",
            timestamp=datetime.now(),
            open=50000.0,
            high=51000.0,
            low=49000.0,
            close=50500.0,
            volume=1000.0
        )
        data_store.add_market_data(market_data)
        
        # Test lấy market data
        df = data_store.get_market_data("BTCUSDT", "1h")
        if df is not None and len(df) > 0:
            print(f"✅ Market data stored: {len(df)} rows")
        
        # Test thêm suggestion
        suggestion = TradingSuggestion(
            timestamp=datetime.now(),
            mode="Scalp",
            symbol="BTCUSDT",
            direction="LONG",
            entry_price=50500.0,
            stop_loss=49500.0,
            take_profit=51500.0,
            leverage=10,
            reason="Test suggestion"
        )
        data_store.add_suggestion(suggestion)
        
        # Test lấy suggestions
        suggestions = data_store.get_latest_suggestions(5)
        if suggestions:
            print(f"✅ Suggestions stored: {len(suggestions)}")
        
        # Test logs
        data_store.add_log("Test log message")
        logs = data_store.get_logs(5)
        if logs:
            print(f"✅ Logs stored: {len(logs)}")
        
        print("✅ DataStore test passed!")
        
    except Exception as e:
        print(f"❌ DataStore test failed: {e}")

async def test_full_workflow():
    """Test workflow hoàn chỉnh"""
    print("\n🔄 Testing full workflow...")
    
    try:
        # Khởi tạo các components
        config_manager = ConfigManager()
        data_store = DataStore()
        connector = BinanceConnector(data_store)
        analyzer = TechnicalAnalyzer(data_store)
        strategy = TradingStrategy(data_store, config_manager, analyzer)
        
        # Kết nối và lấy dữ liệu
        await connector.start()
        
        # Lấy dữ liệu cho 1 symbol
        symbols = ["BTCUSDT"]
        timeframes = ["1h"]
        
        print("📊 Fetching market data...")
        await connector.fetch_historical_data(symbols, timeframes)
        
        # Kiểm tra dữ liệu
        df = data_store.get_market_data("BTCUSDT", "1h")
        if df is not None and len(df) > 50:
            print(f"✅ Got {len(df)} candles for analysis")
            
            # Chạy phân tích kỹ thuật
            print("🔍 Running technical analysis...")
            indicators_config = config_manager.get_indicators_config("scalp")
            analyzer.analyze_all_symbols(symbols, timeframes, indicators_config)
            
            # Kiểm tra indicators
            indicators = data_store.get_indicators("BTCUSDT", "1h")
            if indicators:
                print(f"✅ Technical indicators calculated")
                print(f"   RSI: {indicators.rsi:.2f}" if indicators.rsi else "   RSI: N/A")
                print(f"   MA Fast: {indicators.ma_fast:.2f}" if indicators.ma_fast else "   MA Fast: N/A")
                print(f"   MA Slow: {indicators.ma_slow:.2f}" if indicators.ma_slow else "   MA Slow: N/A")
            
            # Chạy chiến lược
            print("💡 Running trading strategy...")
            strategy.run_strategy_analysis(symbols, "Scalp")
            
            # Kiểm tra đề xuất
            suggestions = data_store.get_latest_suggestions(5)
            if suggestions:
                print(f"✅ Generated {len(suggestions)} trading suggestions")
                for suggestion in suggestions:
                    print(f"   {suggestion.direction} {suggestion.symbol} @ {suggestion.entry_price}")
            else:
                print("ℹ️ No trading suggestions generated (market conditions may not be suitable)")
        
        await connector.stop()
        print("✅ Full workflow test completed!")
        
    except Exception as e:
        print(f"❌ Full workflow test failed: {e}")

async def main():
    """Hàm main để chạy tất cả tests"""
    print("🚀 Starting Bot Trading AI Demo\n")
    
    # Setup logger
    logger = setup_logger()
    
    # Chạy các tests
    test_config_manager()
    test_data_store()
    await test_binance_connection()
    await test_full_workflow()
    
    print("\n🎉 Demo completed!")
    print("\n📝 Next steps:")
    print("1. Run 'streamlit run app.py' to start the web interface")
    print("2. Configure your trading settings")
    print("3. Start the bot and monitor suggestions")
    print("\n⚠️ Remember: This bot only provides suggestions, not automatic trading!")

if __name__ == "__main__":
    asyncio.run(main()) 