import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
import logging

from .data_models import TechnicalIndicators, DataStore

class TechnicalAnalyzer:
    """Phân tích kỹ thuật"""
    
    def __init__(self, data_store: DataStore):
        self.data_store = data_store
        self.logger = logging.getLogger(__name__)
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> pd.Series:
        """Tính RSI"""
        try:
            close = df['close']
            delta = close.diff()
            
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            
            avg_gain = gain.rolling(window=period).mean()
            avg_loss = loss.rolling(window=period).mean()
            
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            
            return rsi
        except Exception as e:
            self.logger.error(f"Lỗi tính RSI: {e}")
            return pd.Series([np.nan] * len(df))
    
    def calculate_moving_averages(self, df: pd.DataFrame, fast_period: int = 10, slow_period: int = 20) -> tuple:
        """Tính Moving Averages"""
        try:
            close = df['close']
            ma_fast = close.rolling(window=fast_period).mean()
            ma_slow = close.rolling(window=slow_period).mean()
            return ma_fast, ma_slow
        except Exception as e:
            self.logger.error(f"Lỗi tính MA: {e}")
            return pd.Series([np.nan] * len(df)), pd.Series([np.nan] * len(df))
    
    def calculate_ema(self, series: pd.Series, period: int) -> pd.Series:
        """Tính Exponential Moving Average"""
        return series.ewm(span=period).mean()
    
    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> tuple:
        """Tính MACD"""
        try:
            close = df['close']
            
            # Tính EMA
            ema_fast = self.calculate_ema(close, fast)
            ema_slow = self.calculate_ema(close, slow)
            
            # MACD line
            macd = ema_fast - ema_slow
            
            # Signal line
            macd_signal = self.calculate_ema(macd, signal)
            
            # Histogram
            macd_histogram = macd - macd_signal
            
            return macd, macd_signal, macd_histogram
            
        except Exception as e:
            self.logger.error(f"Lỗi tính MACD: {e}")
            return (pd.Series([np.nan] * len(df)), 
                   pd.Series([np.nan] * len(df)), 
                   pd.Series([np.nan] * len(df)))
    
    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std: float = 2) -> tuple:
        """Tính Bollinger Bands"""
        try:
            close = df['close']
            
            # Middle band (SMA)
            bb_middle = close.rolling(window=period).mean()
            
            # Standard deviation
            bb_std = close.rolling(window=period).std()
            
            # Upper and lower bands
            bb_upper = bb_middle + (bb_std * std)
            bb_lower = bb_middle - (bb_std * std)
            
            return bb_upper, bb_middle, bb_lower
            
        except Exception as e:
            self.logger.error(f"Lỗi tính Bollinger Bands: {e}")
            return (pd.Series([np.nan] * len(df)), 
                   pd.Series([np.nan] * len(df)), 
                   pd.Series([np.nan] * len(df)))
    
    def analyze_symbol_timeframe(self, symbol: str, timeframe: str, indicators_config: Dict) -> Optional[TechnicalIndicators]:
        """Phân tích một symbol và timeframe"""
        try:
            # Lấy dữ liệu thị trường
            df = self.data_store.get_market_data(symbol, timeframe)
            if df is None or len(df) < 50:  # Cần ít nhất 50 nến để tính chỉ báo
                return None
            
            # Đảm bảo dữ liệu được sắp xếp theo thời gian
            df = df.sort_values('timestamp').reset_index(drop=True)
            
            # Tính các chỉ báo
            rsi = self.calculate_rsi(df, indicators_config.get('rsi_period', 14))
            ma_fast, ma_slow = self.calculate_moving_averages(
                df, 
                indicators_config.get('ma_fast', 10),
                indicators_config.get('ma_slow', 20)
            )
            macd, macd_signal, macd_histogram = self.calculate_macd(
                df,
                indicators_config.get('macd_fast', 12),
                indicators_config.get('macd_slow', 26),
                indicators_config.get('macd_signal', 9)
            )
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(df)
            
            # Lấy giá trị mới nhất
            latest_idx = len(df) - 1
            latest_timestamp = df.iloc[latest_idx]['timestamp']
            
            # Tạo TechnicalIndicators object
            indicators = TechnicalIndicators(
                symbol=symbol,
                timeframe=timeframe,
                timestamp=latest_timestamp,
                rsi=rsi.iloc[latest_idx] if not pd.isna(rsi.iloc[latest_idx]) else None,
                ma_fast=ma_fast.iloc[latest_idx] if not pd.isna(ma_fast.iloc[latest_idx]) else None,
                ma_slow=ma_slow.iloc[latest_idx] if not pd.isna(ma_slow.iloc[latest_idx]) else None,
                macd=macd.iloc[latest_idx] if not pd.isna(macd.iloc[latest_idx]) else None,
                macd_signal=macd_signal.iloc[latest_idx] if not pd.isna(macd_signal.iloc[latest_idx]) else None,
                macd_histogram=macd_histogram.iloc[latest_idx] if not pd.isna(macd_histogram.iloc[latest_idx]) else None,
                bb_upper=bb_upper.iloc[latest_idx] if not pd.isna(bb_upper.iloc[latest_idx]) else None,
                bb_middle=bb_middle.iloc[latest_idx] if not pd.isna(bb_middle.iloc[latest_idx]) else None,
                bb_lower=bb_lower.iloc[latest_idx] if not pd.isna(bb_lower.iloc[latest_idx]) else None
            )
            
            return indicators
            
        except Exception as e:
            self.logger.error(f"Lỗi phân tích {symbol} {timeframe}: {e}")
            return None
    
    def get_trend_direction(self, symbol: str, timeframe: str) -> Optional[str]:
        """Xác định hướng xu hướng dựa trên MA"""
        try:
            indicators = self.data_store.get_indicators(symbol, timeframe)
            if not indicators or indicators.ma_fast is None or indicators.ma_slow is None:
                return None
            
            if indicators.ma_fast > indicators.ma_slow:
                return "BULLISH"
            elif indicators.ma_fast < indicators.ma_slow:
                return "BEARISH"
            else:
                return "SIDEWAYS"
                
        except Exception as e:
            self.logger.error(f"Lỗi xác định xu hướng {symbol} {timeframe}: {e}")
            return None
    
    def get_rsi_signal(self, symbol: str, timeframe: str, mode: str = "scalp") -> Optional[str]:
        """Xác định tín hiệu RSI"""
        try:
            indicators = self.data_store.get_indicators(symbol, timeframe)
            if not indicators or indicators.rsi is None:
                return None
            
            rsi = indicators.rsi
            
            if mode.lower() == "scalp":
                # Scalp: Tín hiệu nhạy hơn
                if rsi > 70:
                    return "OVERBOUGHT"
                elif rsi < 30:
                    return "OVERSOLD"
                elif rsi > 60:
                    return "BULLISH"
                elif rsi < 40:
                    return "BEARISH"
            else:  # swing
                # Swing: Tín hiệu bảo thủ hơn
                if rsi > 80:
                    return "OVERBOUGHT"
                elif rsi < 20:
                    return "OVERSOLD"
                elif rsi > 65:
                    return "BULLISH"
                elif rsi < 35:
                    return "BEARISH"
            
            return "NEUTRAL"
            
        except Exception as e:
            self.logger.error(f"Lỗi tín hiệu RSI {symbol} {timeframe}: {e}")
            return None
    
    def get_macd_signal(self, symbol: str, timeframe: str) -> Optional[str]:
        """Xác định tín hiệu MACD"""
        try:
            indicators = self.data_store.get_indicators(symbol, timeframe)
            if not indicators or indicators.macd is None or indicators.macd_signal is None:
                return None
            
            macd = indicators.macd
            macd_signal = indicators.macd_signal
            macd_histogram = indicators.macd_histogram
            
            # MACD cross over signal line
            if macd > macd_signal and macd_histogram and macd_histogram > 0:
                return "BULLISH_CROSS"
            elif macd < macd_signal and macd_histogram and macd_histogram < 0:
                return "BEARISH_CROSS"
            elif macd > 0 and macd_signal > 0:
                return "BULLISH"
            elif macd < 0 and macd_signal < 0:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except Exception as e:
            self.logger.error(f"Lỗi tín hiệu MACD {symbol} {timeframe}: {e}")
            return None
    
    def get_bollinger_signal(self, symbol: str, timeframe: str) -> Optional[str]:
        """Xác định tín hiệu Bollinger Bands"""
        try:
            indicators = self.data_store.get_indicators(symbol, timeframe)
            current_price = self.data_store.get_price(symbol)
            
            if (not indicators or indicators.bb_upper is None or 
                indicators.bb_lower is None or not current_price):
                return None
            
            price = current_price.price
            
            if price >= indicators.bb_upper:
                return "OVERBOUGHT"
            elif price <= indicators.bb_lower:
                return "OVERSOLD"
            elif price > indicators.bb_middle:
                return "BULLISH"
            elif price < indicators.bb_middle:
                return "BEARISH"
            else:
                return "NEUTRAL"
                
        except Exception as e:
            self.logger.error(f"Lỗi tín hiệu Bollinger {symbol} {timeframe}: {e}")
            return None
    
    def analyze_all_symbols(self, symbols: List[str], timeframes: List[str], indicators_config: Dict):
        """Phân tích tất cả symbols và timeframes"""
        for symbol in symbols:
            for timeframe in timeframes:
                try:
                    indicators = self.analyze_symbol_timeframe(symbol, timeframe, indicators_config)
                    if indicators:
                        self.data_store.add_indicators(indicators)
                except Exception as e:
                    self.logger.error(f"Lỗi phân tích {symbol} {timeframe}: {e}")
    
    def get_multi_timeframe_analysis(self, symbol: str, timeframes: List[str], mode: str = "scalp") -> Dict:
        """Phân tích đa khung thời gian"""
        analysis = {
            'symbol': symbol,
            'mode': mode,
            'timeframes': {},
            'overall_sentiment': 'NEUTRAL',
            'strength': 0.0
        }
        
        bullish_signals = 0
        bearish_signals = 0
        total_signals = 0
        
        for timeframe in timeframes:
            try:
                tf_analysis = {
                    'trend': self.get_trend_direction(symbol, timeframe),
                    'rsi_signal': self.get_rsi_signal(symbol, timeframe, mode),
                    'macd_signal': self.get_macd_signal(symbol, timeframe),
                    'bb_signal': self.get_bollinger_signal(symbol, timeframe)
                }
                
                analysis['timeframes'][timeframe] = tf_analysis
                
                # Đếm tín hiệu
                for signal in tf_analysis.values():
                    if signal:
                        total_signals += 1
                        if 'BULLISH' in signal or signal == 'OVERSOLD':
                            bullish_signals += 1
                        elif 'BEARISH' in signal or signal == 'OVERBOUGHT':
                            bearish_signals += 1
                            
            except Exception as e:
                self.logger.error(f"Lỗi phân tích đa khung thời gian {symbol} {timeframe}: {e}")
        
        # Xác định sentiment tổng thể
        if total_signals > 0:
            bullish_ratio = bullish_signals / total_signals
            bearish_ratio = bearish_signals / total_signals
            
            if bullish_ratio > 0.6:
                analysis['overall_sentiment'] = 'BULLISH'
                analysis['strength'] = bullish_ratio
            elif bearish_ratio > 0.6:
                analysis['overall_sentiment'] = 'BEARISH'
                analysis['strength'] = bearish_ratio
            else:
                analysis['overall_sentiment'] = 'NEUTRAL'
                analysis['strength'] = 0.5
        
        return analysis 