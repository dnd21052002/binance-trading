import math
from typing import Dict, List, Optional
from datetime import datetime
import logging

from .data_models import TradingSuggestion, DataStore
from .technical_analysis import TechnicalAnalyzer
from config.config import ConfigManager

class TradingStrategy:
    """Chiến lược giao dịch"""
    
    def __init__(self, data_store: DataStore, config_manager: ConfigManager, technical_analyzer: TechnicalAnalyzer):
        self.data_store = data_store
        self.config_manager = config_manager
        self.technical_analyzer = technical_analyzer
        self.logger = logging.getLogger(__name__)
        
    def calculate_position_size(self, capital: float, risk_per_trade: float, entry_price: float, stop_loss: float) -> float:
        """Tính kích thước vị thế dựa trên quản lý rủi ro"""
        try:
            # Tính toán risk amount
            risk_amount = capital * risk_per_trade
            
            # Tính toán price difference
            price_diff = abs(entry_price - stop_loss)
            if price_diff == 0:
                return 0
            
            # Tính position size
            position_size = risk_amount / price_diff
            
            return position_size
            
        except Exception as e:
            self.logger.error(f"Lỗi tính position size: {e}")
            return 0
    
    def calculate_leverage(self, capital: float, position_size: float, entry_price: float, max_leverage: int = 20) -> int:
        """Tính đòn bẩy phù hợp"""
        try:
            # Tính notional value
            notional_value = position_size * entry_price
            
            # Tính leverage cần thiết
            required_leverage = notional_value / capital
            
            # Giới hạn leverage
            leverage = min(math.ceil(required_leverage), max_leverage)
            leverage = max(leverage, 1)  # Tối thiểu 1x
            
            return leverage
            
        except Exception as e:
            self.logger.error(f"Lỗi tính leverage: {e}")
            return 1
    
    def calculate_take_profit_scalp(self, entry_price: float, direction: str, tp_percentage: float = 0.5) -> float:
        """Tính take profit cho Scalp dựa trên phần trăm (0.3-1%)"""
        try:
            if direction == "LONG":
                return entry_price * (1 + tp_percentage / 100)
            else:  # SHORT
                return entry_price * (1 - tp_percentage / 100)
        except Exception as e:
            self.logger.error(f"Lỗi tính TP scalp: {e}")
            return entry_price
    
    def calculate_stop_loss_scalp(self, entry_price: float, direction: str, sl_percentage: float = 0.3) -> float:
        """Tính stop loss cho Scalp dựa trên phần trăm (0.2-0.5%)"""
        try:
            if direction == "LONG":
                return entry_price * (1 - sl_percentage / 100)
            else:  # SHORT
                return entry_price * (1 + sl_percentage / 100)
        except Exception as e:
            self.logger.error(f"Lỗi tính SL scalp: {e}")
            return entry_price
    
    def calculate_take_profit_swing(self, entry_price: float, direction: str, tp_percentage: float = 3.0) -> float:
        """Tính take profit cho Swing dựa trên phần trăm (2-5%)"""
        try:
            if direction == "LONG":
                return entry_price * (1 + tp_percentage / 100)
            else:  # SHORT
                return entry_price * (1 - tp_percentage / 100)
        except Exception as e:
            self.logger.error(f"Lỗi tính TP swing: {e}")
            return entry_price
    
    def calculate_stop_loss_swing(self, entry_price: float, direction: str, sl_percentage: float = 1.5) -> float:
        """Tính stop loss cho Swing dựa trên phần trăm (1-2%)"""
        try:
            if direction == "LONG":
                return entry_price * (1 - sl_percentage / 100)
            else:  # SHORT
                return entry_price * (1 + sl_percentage / 100)
        except Exception as e:
            self.logger.error(f"Lỗi tính SL swing: {e}")
            return entry_price
    
    def generate_scalp_suggestion(self, symbol: str, analysis: Dict, config: Dict) -> Optional[TradingSuggestion]:
        """Tạo đề xuất giao dịch Scalp"""
        try:
            # Lấy giá hiện tại
            current_price_data = self.data_store.get_price(symbol)
            if not current_price_data:
                return None
            
            current_price = current_price_data.price
            
            # Phân tích tín hiệu trên khung thời gian ngắn (1m, 5m, 15m)
            scalp_timeframes = self.config_manager.get_timeframes_for_mode("scalp")
            
            # Đếm tín hiệu bullish/bearish
            bullish_signals = 0
            bearish_signals = 0
            total_signals = 0
            reasons = []
            
            for tf in scalp_timeframes:
                if tf in analysis['timeframes']:
                    tf_data = analysis['timeframes'][tf]
                    
                    # RSI signal
                    if tf_data['rsi_signal']:
                        total_signals += 1
                        if 'BULLISH' in tf_data['rsi_signal'] or tf_data['rsi_signal'] == 'OVERSOLD':
                            bullish_signals += 1
                            reasons.append(f"RSI({tf}): {tf_data['rsi_signal']}")
                        elif 'BEARISH' in tf_data['rsi_signal'] or tf_data['rsi_signal'] == 'OVERBOUGHT':
                            bearish_signals += 1
                            reasons.append(f"RSI({tf}): {tf_data['rsi_signal']}")
                    
                    # MACD signal
                    if tf_data['macd_signal'] and 'CROSS' in tf_data['macd_signal']:
                        total_signals += 1
                        if 'BULLISH' in tf_data['macd_signal']:
                            bullish_signals += 1
                            reasons.append(f"MACD({tf}): Cross Up")
                        elif 'BEARISH' in tf_data['macd_signal']:
                            bearish_signals += 1
                            reasons.append(f"MACD({tf}): Cross Down")
                    
                    # Trend signal
                    if tf_data['trend']:
                        total_signals += 1
                        if tf_data['trend'] == 'BULLISH':
                            bullish_signals += 1
                            reasons.append(f"Trend({tf}): Up")
                        elif tf_data['trend'] == 'BEARISH':
                            bearish_signals += 1
                            reasons.append(f"Trend({tf}): Down")
            
            # Quyết định hướng giao dịch
            if total_signals < 2:  # Cần ít nhất 2 tín hiệu
                return None
            
            direction = None
            confidence = 0
            
            if bullish_signals >= 2 and bullish_signals > bearish_signals:
                direction = "LONG"
                confidence = bullish_signals / total_signals
            elif bearish_signals >= 2 and bearish_signals > bullish_signals:
                direction = "SHORT"
                confidence = bearish_signals / total_signals
            else:
                return None  # Tín hiệu không rõ ràng
            
            # Tính toán entry, SL, TP cho Scalp
            capital = config.get('available_capital', 10000)
            risk_config = self.config_manager.get_risk_management_config()
            
            # Entry price
            entry_price = current_price
            
            # Tính SL và TP theo phần trăm cho Scalp (nhỏ hơn nhiều)
            stop_loss = self.calculate_stop_loss_scalp(entry_price, direction, 0.3)  # 0.3% SL
            take_profit = self.calculate_take_profit_scalp(entry_price, direction, 0.6)  # 0.6% TP
            
            # Tính position size dựa trên risk management
            position_size = self.calculate_position_size(capital, risk_config.get('risk_per_trade', 0.02), entry_price, stop_loss)
            
            if position_size <= 0:
                return None
            
            # Tính leverage (thường cao hơn cho scalp)
            leverage = min(self.calculate_leverage(capital, position_size, entry_price, risk_config.get('max_leverage', 20)), 20)
            
            # Tạo suggestion
            suggestion = TradingSuggestion(
                timestamp=datetime.now(),
                mode="Scalp",
                symbol=symbol,
                direction=direction,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                leverage=leverage,
                reason=", ".join(reasons[:3]),  # Giới hạn 3 lý do chính
                confidence=confidence
            )
            
            return suggestion
            
        except Exception as e:
            self.logger.error(f"Lỗi tạo đề xuất scalp {symbol}: {e}")
            return None
    
    def generate_swing_suggestion(self, symbol: str, analysis: Dict, config: Dict) -> Optional[TradingSuggestion]:
        """Tạo đề xuất giao dịch Swing"""
        try:
            # Lấy giá hiện tại
            current_price_data = self.data_store.get_price(symbol)
            if not current_price_data:
                return None
            
            current_price = current_price_data.price
            
            # Phân tích tín hiệu trên khung thời gian dài (1h, 4h, 1d)
            swing_timeframes = self.config_manager.get_timeframes_for_mode("swing")
            
            # Đếm tín hiệu bullish/bearish với trọng số khác nhau
            bullish_score = 0
            bearish_score = 0
            total_score = 0
            reasons = []
            
            # Trọng số cho các khung thời gian (1d > 4h > 1h)
            timeframe_weights = {"1d": 3, "4h": 2, "1h": 1}
            
            for tf in swing_timeframes:
                if tf in analysis['timeframes']:
                    tf_data = analysis['timeframes'][tf]
                    weight = timeframe_weights.get(tf, 1)
                    
                    # Trend signal (quan trọng nhất cho swing)
                    if tf_data['trend']:
                        total_score += weight * 2
                        if tf_data['trend'] == 'BULLISH':
                            bullish_score += weight * 2
                            reasons.append(f"Trend({tf}): Bullish")
                        elif tf_data['trend'] == 'BEARISH':
                            bearish_score += weight * 2
                            reasons.append(f"Trend({tf}): Bearish")
                    
                    # RSI signal (với ngưỡng swing)
                    if tf_data['rsi_signal']:
                        total_score += weight
                        if tf_data['rsi_signal'] == 'OVERSOLD':
                            bullish_score += weight
                            reasons.append(f"RSI({tf}): Oversold")
                        elif tf_data['rsi_signal'] == 'OVERBOUGHT':
                            bearish_score += weight
                            reasons.append(f"RSI({tf}): Overbought")
                        elif 'BULLISH' in tf_data['rsi_signal']:
                            bullish_score += weight * 0.5
                        elif 'BEARISH' in tf_data['rsi_signal']:
                            bearish_score += weight * 0.5
                    
                    # MACD signal
                    if tf_data['macd_signal']:
                        total_score += weight
                        if 'BULLISH' in tf_data['macd_signal']:
                            bullish_score += weight
                            reasons.append(f"MACD({tf}): Bullish")
                        elif 'BEARISH' in tf_data['macd_signal']:
                            bearish_score += weight
                            reasons.append(f"MACD({tf}): Bearish")
            
            # Quyết định hướng giao dịch (cần tín hiệu mạnh hơn cho swing)
            if total_score < 3:  # Cần tín hiệu mạnh
                return None
            
            direction = None
            confidence = 0
            
            if bullish_score >= 4 and bullish_score > bearish_score * 1.5:
                direction = "LONG"
                confidence = bullish_score / total_score
            elif bearish_score >= 4 and bearish_score > bullish_score * 1.5:
                direction = "SHORT"
                confidence = bearish_score / total_score
            else:
                return None  # Tín hiệu không đủ mạnh
            
            # Tính toán entry, SL, TP cho Swing
            capital = config.get('available_capital', 10000)
            risk_config = self.config_manager.get_risk_management_config()
            
            # Entry price
            entry_price = current_price
            
            # Tính SL và TP theo phần trăm cho Swing (lớn hơn Scalp)
            stop_loss = self.calculate_stop_loss_swing(entry_price, direction, 1.5)  # 1.5% SL
            take_profit = self.calculate_take_profit_swing(entry_price, direction, 3.0)  # 3% TP
            
            # Tính position size dựa trên risk management
            position_size = self.calculate_position_size(capital, risk_config.get('risk_per_trade', 0.02), entry_price, stop_loss)
            
            if position_size <= 0:
                return None
            
            # Leverage thấp hơn cho swing
            leverage = min(self.calculate_leverage(capital, position_size, entry_price, risk_config.get('max_leverage', 20)), 15)
            
            # Tạo suggestion
            suggestion = TradingSuggestion(
                timestamp=datetime.now(),
                mode="Swing",
                symbol=symbol,
                direction=direction,
                entry_price=entry_price,
                stop_loss=stop_loss,
                take_profit=take_profit,
                leverage=leverage,
                reason=", ".join(reasons[:3]),
                confidence=confidence
            )
            
            return suggestion
            
        except Exception as e:
            self.logger.error(f"Lỗi tạo đề xuất swing {symbol}: {e}")
            return None
    
    def generate_suggestions(self, symbols: List[str], trading_mode: str) -> List[TradingSuggestion]:
        """Tạo đề xuất giao dịch cho tất cả symbols"""
        suggestions = []
        
        try:
            # Lấy cấu hình
            trading_config = self.config_manager.get_trading_config()
            config_dict = {
                'available_capital': trading_config.available_capital,
                'target_profit_per_trade': trading_config.target_profit_per_trade,
                'max_loss_per_trade': trading_config.max_loss_per_trade
            }
            
            # Lấy timeframes phù hợp với mode
            timeframes = self.config_manager.get_timeframes_for_mode(trading_mode)
            
            for symbol in symbols:
                try:
                    # Phân tích đa khung thời gian
                    analysis = self.technical_analyzer.get_multi_timeframe_analysis(symbol, timeframes, trading_mode)
                    
                    # Tạo đề xuất dựa trên mode
                    suggestion = None
                    if trading_mode.lower() == "scalp":
                        suggestion = self.generate_scalp_suggestion(symbol, analysis, config_dict)
                    else:  # swing
                        suggestion = self.generate_swing_suggestion(symbol, analysis, config_dict)
                    
                    if suggestion and suggestion.confidence > 0.6:  # Chỉ lấy đề xuất có độ tin cậy cao
                        suggestions.append(suggestion)
                        self.data_store.add_suggestion(suggestion)
                        self.data_store.add_log(f"Tạo đề xuất {suggestion.direction} {suggestion.symbol.replace('USDT', '')} ({suggestion.mode})")
                        
                except Exception as e:
                    self.logger.error(f"Lỗi tạo đề xuất cho {symbol}: {e}")
                    continue
            
        except Exception as e:
            self.logger.error(f"Lỗi tạo đề xuất: {e}")
        
        return suggestions
    
    def run_strategy_analysis(self, symbols: List[str], trading_mode: str):
        """Chạy phân tích chiến lược"""
        try:
            # Debug log
            self.data_store.add_log(f"🔍 Chạy phân tích với chế độ: {trading_mode}")
            
            # Lấy cấu hình indicators
            indicators_config = self.config_manager.get_indicators_config(trading_mode)
            
            # Lấy timeframes phù hợp
            timeframes = self.config_manager.get_timeframes_for_mode(trading_mode)
            self.data_store.add_log(f"📊 Timeframes cho {trading_mode}: {timeframes}")
            
            # Phân tích kỹ thuật
            self.technical_analyzer.analyze_all_symbols(symbols, timeframes, indicators_config)
            
            # Tạo đề xuất
            suggestions = self.generate_suggestions(symbols, trading_mode)
            
            if suggestions:
                self.data_store.add_log(f"✅ Đã tạo {len(suggestions)} đề xuất {trading_mode}")
                for suggestion in suggestions:
                    self.data_store.add_log(f"   📈 {suggestion.mode}: {suggestion.symbol} {suggestion.direction}")
            else:
                self.data_store.add_log(f"ℹ️ Không có đề xuất {trading_mode} phù hợp")
            
        except Exception as e:
            self.logger.error(f"Lỗi chạy phân tích chiến lược: {e}")
            self.data_store.add_log(f"❌ Lỗi phân tích chiến lược: {str(e)}") 