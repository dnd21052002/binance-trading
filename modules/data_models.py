from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime
import pandas as pd

@dataclass
class MarketData:
    """Dữ liệu thị trường"""
    symbol: str
    timeframe: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float

@dataclass
class TechnicalIndicators:
    """Chỉ báo kỹ thuật"""
    symbol: str
    timeframe: str
    timestamp: datetime
    rsi: Optional[float] = None
    ma_fast: Optional[float] = None
    ma_slow: Optional[float] = None
    macd: Optional[float] = None
    macd_signal: Optional[float] = None
    macd_histogram: Optional[float] = None
    bb_upper: Optional[float] = None
    bb_middle: Optional[float] = None
    bb_lower: Optional[float] = None

@dataclass
class TradingSuggestion:
    """Đề xuất giao dịch"""
    timestamp: datetime
    mode: str  # Scalp hoặc Swing
    symbol: str
    direction: str  # LONG hoặc SHORT
    entry_price: float
    stop_loss: float
    take_profit: float
    leverage: int
    reason: str
    confidence: float = 0.0  # Độ tin cậy từ 0-1
    
    def to_dict(self) -> Dict:
        """Chuyển đổi thành dictionary"""
        return {
            'timestamp': self.timestamp.strftime('%H:%M:%S'),
            'mode': self.mode,
            'symbol': self.symbol.replace('USDT', ''),
            'direction': self.direction,
            'entry_price': f"{self.entry_price:.2f}",
            'stop_loss': f"{self.stop_loss:.2f}",
            'take_profit': f"{self.take_profit:.2f}",
            'leverage': f"{self.leverage}x",
            'reason': self.reason
        }

@dataclass
class TokenPrice:
    """Giá token hiện tại"""
    symbol: str
    price: float
    change_24h: float = 0.0
    timestamp: datetime = None
    
    def __post_init__(self):
        if self.timestamp is None:
            self.timestamp = datetime.now()

class DataStore:
    """Lưu trữ dữ liệu trong bộ nhớ"""
    
    def __init__(self):
        self.market_data: Dict[str, Dict[str, pd.DataFrame]] = {}  # symbol -> timeframe -> DataFrame
        self.indicators: Dict[str, Dict[str, TechnicalIndicators]] = {}  # symbol -> timeframe -> indicators
        self.suggestions: List[TradingSuggestion] = []
        self.current_prices: Dict[str, TokenPrice] = {}
        self.logs: List[str] = []
        
    def add_market_data(self, data: MarketData):
        """Thêm dữ liệu thị trường"""
        if data.symbol not in self.market_data:
            self.market_data[data.symbol] = {}
        
        if data.timeframe not in self.market_data[data.symbol]:
            self.market_data[data.symbol][data.timeframe] = pd.DataFrame()
        
        # Thêm dữ liệu mới vào DataFrame
        new_row = {
            'timestamp': data.timestamp,
            'open': data.open,
            'high': data.high,
            'low': data.low,
            'close': data.close,
            'volume': data.volume
        }
        
        df = self.market_data[data.symbol][data.timeframe]
        df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
        
        # Giữ chỉ 1000 nến gần nhất
        if len(df) > 1000:
            df = df.tail(1000).reset_index(drop=True)
        
        self.market_data[data.symbol][data.timeframe] = df
    
    def get_market_data(self, symbol: str, timeframe: str) -> Optional[pd.DataFrame]:
        """Lấy dữ liệu thị trường"""
        return self.market_data.get(symbol, {}).get(timeframe)
    
    def add_indicators(self, indicators: TechnicalIndicators):
        """Thêm chỉ báo kỹ thuật"""
        if indicators.symbol not in self.indicators:
            self.indicators[indicators.symbol] = {}
        
        self.indicators[indicators.symbol][indicators.timeframe] = indicators
    
    def get_indicators(self, symbol: str, timeframe: str) -> Optional[TechnicalIndicators]:
        """Lấy chỉ báo kỹ thuật"""
        return self.indicators.get(symbol, {}).get(timeframe)
    
    def add_suggestion(self, suggestion: TradingSuggestion):
        """Thêm đề xuất giao dịch"""
        self.suggestions.append(suggestion)
        
        # Giữ chỉ 100 đề xuất gần nhất
        if len(self.suggestions) > 100:
            self.suggestions = self.suggestions[-100:]
    
    def get_latest_suggestions(self, limit: int = 10) -> List[TradingSuggestion]:
        """Lấy các đề xuất gần nhất"""
        return self.suggestions[-limit:] if self.suggestions else []
    
    def update_price(self, symbol: str, price: float, change_24h: float = 0.0):
        """Cập nhật giá hiện tại"""
        self.current_prices[symbol] = TokenPrice(symbol, price, change_24h)
    
    def get_price(self, symbol: str) -> Optional[TokenPrice]:
        """Lấy giá hiện tại"""
        return self.current_prices.get(symbol)
    
    def add_log(self, message: str):
        """Thêm log"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        log_message = f"[{timestamp}] {message}"
        self.logs.append(log_message)
        
        # Giữ chỉ 100 log gần nhất
        if len(self.logs) > 100:
            self.logs = self.logs[-100:]
    
    def get_logs(self, limit: int = 10) -> List[str]:
        """Lấy các log gần nhất"""
        return self.logs[-limit:] if self.logs else [] 