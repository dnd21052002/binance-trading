import asyncio
import aiohttp
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional
import time
import logging

from .data_models import MarketData, DataStore

class BinanceConnector:
    """Kết nối và lấy dữ liệu từ Binance API"""
    
    def __init__(self, data_store: DataStore):
        self.data_store = data_store
        self.base_url = "https://fapi.binance.com"
        self.session = None
        self.is_running = False
        
        # Thiết lập logging
        self.logger = logging.getLogger(__name__)
        
    async def start(self):
        """Khởi động connector"""
        self.session = aiohttp.ClientSession()
        self.is_running = True
        self.data_store.add_log("Đang kết nối đến Binance API...")
        
        # Test kết nối
        if await self.test_connection():
            self.data_store.add_log("Kết nối Binance API thành công ✅")
        else:
            self.data_store.add_log("Lỗi kết nối Binance API ❌")
            
    async def stop(self):
        """Dừng connector"""
        self.is_running = False
        if self.session:
            await self.session.close()
            
    async def test_connection(self) -> bool:
        """Test kết nối API"""
        try:
            url = f"{self.base_url}/fapi/v1/ping"
            async with self.session.get(url) as response:
                return response.status == 200
        except Exception as e:
            self.logger.error(f"Lỗi test kết nối: {e}")
            return False
    
    async def get_current_price(self, symbol: str) -> Optional[float]:
        """Lấy giá hiện tại của symbol"""
        try:
            url = f"{self.base_url}/fapi/v1/ticker/price"
            params = {"symbol": symbol}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    data = await response.json()
                    return float(data["price"])
                else:
                    self.logger.error(f"Lỗi lấy giá {symbol}: {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Lỗi lấy giá {symbol}: {e}")
            return None
    
    async def get_24h_ticker(self, symbol: str) -> Optional[Dict]:
        """Lấy thông tin ticker 24h"""
        try:
            url = f"{self.base_url}/fapi/v1/ticker/24hr"
            params = {"symbol": symbol}
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Lỗi lấy ticker 24h {symbol}: {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Lỗi lấy ticker 24h {symbol}: {e}")
            return None
    
    async def get_klines(self, symbol: str, interval: str, limit: int = 500) -> Optional[List]:
        """Lấy dữ liệu nến (klines)"""
        try:
            url = f"{self.base_url}/fapi/v1/klines"
            params = {
                "symbol": symbol,
                "interval": interval,
                "limit": limit
            }
            
            async with self.session.get(url, params=params) as response:
                if response.status == 200:
                    return await response.json()
                else:
                    self.logger.error(f"Lỗi lấy klines {symbol} {interval}: {response.status}")
                    return None
        except Exception as e:
            self.logger.error(f"Lỗi lấy klines {symbol} {interval}: {e}")
            return None
    
    def parse_klines_data(self, klines_data: List, symbol: str, timeframe: str) -> List[MarketData]:
        """Chuyển đổi dữ liệu klines thành MarketData"""
        market_data_list = []
        
        for kline in klines_data:
            try:
                timestamp = datetime.fromtimestamp(kline[0] / 1000)
                market_data = MarketData(
                    symbol=symbol,
                    timeframe=timeframe,
                    timestamp=timestamp,
                    open=float(kline[1]),
                    high=float(kline[2]),
                    low=float(kline[3]),
                    close=float(kline[4]),
                    volume=float(kline[5])
                )
                market_data_list.append(market_data)
            except Exception as e:
                self.logger.error(f"Lỗi parse kline data: {e}")
                continue
                
        return market_data_list
    
    async def fetch_historical_data(self, symbols: List[str], timeframes: List[str]):
        """Lấy dữ liệu lịch sử cho tất cả symbols và timeframes"""
        self.data_store.add_log("Đang tải dữ liệu lịch sử...")
        
        for symbol in symbols:
            for timeframe in timeframes:
                try:
                    klines_data = await self.get_klines(symbol, timeframe, 200)
                    if klines_data:
                        market_data_list = self.parse_klines_data(klines_data, symbol, timeframe)
                        
                        # Thêm vào data store
                        for market_data in market_data_list:
                            self.data_store.add_market_data(market_data)
                        
                        self.data_store.add_log(f"Đã tải {len(market_data_list)} nến {symbol} {timeframe}")
                    
                    # Tránh rate limit
                    await asyncio.sleep(0.1)
                    
                except Exception as e:
                    self.logger.error(f"Lỗi tải dữ liệu {symbol} {timeframe}: {e}")
                    self.data_store.add_log(f"Lỗi tải dữ liệu {symbol} {timeframe}")
    
    async def update_current_prices(self, symbols: List[str]):
        """Cập nhật giá hiện tại cho tất cả symbols"""
        for symbol in symbols:
            try:
                # Lấy ticker 24h để có thêm thông tin change
                ticker_data = await self.get_24h_ticker(symbol)
                if ticker_data:
                    price = float(ticker_data["lastPrice"])
                    change_24h = float(ticker_data["priceChangePercent"])
                    self.data_store.update_price(symbol, price, change_24h)
                
                # Tránh rate limit
                await asyncio.sleep(0.05)
                
            except Exception as e:
                self.logger.error(f"Lỗi cập nhật giá {symbol}: {e}")
    
    async def fetch_latest_klines(self, symbols: List[str], timeframes: List[str]):
        """Lấy dữ liệu nến mới nhất"""
        for symbol in symbols:
            for timeframe in timeframes:
                try:
                    # Chỉ lấy 2 nến mới nhất để cập nhật
                    klines_data = await self.get_klines(symbol, timeframe, 2)
                    if klines_data:
                        market_data_list = self.parse_klines_data(klines_data, symbol, timeframe)
                        
                        # Chỉ thêm nến mới nhất (nến cuối có thể chưa đóng)
                        if market_data_list:
                            latest_data = market_data_list[-1]
                            self.data_store.add_market_data(latest_data)
                    
                    # Tránh rate limit
                    await asyncio.sleep(0.05)
                    
                except Exception as e:
                    self.logger.error(f"Lỗi cập nhật klines {symbol} {timeframe}: {e}")
    
    async def run_data_fetcher(self, symbols: List[str], timeframes: List[str], update_interval: int = 30):
        """Chạy vòng lặp cập nhật dữ liệu"""
        # Tải dữ liệu lịch sử lần đầu
        await self.fetch_historical_data(symbols, timeframes)
        
        last_price_update = 0
        last_klines_update = 0
        
        while self.is_running:
            try:
                current_time = time.time()
                
                # Cập nhật giá mỗi 5 giây
                if current_time - last_price_update >= 5:
                    await self.update_current_prices(symbols)
                    last_price_update = current_time
                
                # Cập nhật klines mỗi 30 giây
                if current_time - last_klines_update >= update_interval:
                    await self.fetch_latest_klines(symbols, timeframes)
                    last_klines_update = current_time
                    self.data_store.add_log("Đã cập nhật dữ liệu thị trường")
                
                await asyncio.sleep(1)
                
            except Exception as e:
                self.logger.error(f"Lỗi trong vòng lặp cập nhật dữ liệu: {e}")
                self.data_store.add_log(f"Lỗi cập nhật dữ liệu: {str(e)}")
                await asyncio.sleep(5)  # Chờ 5 giây trước khi thử lại 