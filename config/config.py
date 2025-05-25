import json
import os
from typing import Dict, Any, List
from dataclasses import dataclass

@dataclass
class TradingConfig:
    """Cấu hình giao dịch"""
    trading_mode: str = "Scalp"
    available_capital: float = 10000.0
    target_profit_per_trade: float = 50.0
    max_loss_per_trade: float = 25.0
    tokens: List[str] = None
    timeframes: List[str] = None
    
    def __post_init__(self):
        if self.tokens is None:
            self.tokens = ["BTCUSDT", "SOLUSDT", "ETHUSDT"]
        if self.timeframes is None:
            self.timeframes = ["1m", "5m", "15m", "30m", "1h", "4h", "1d"]

class ConfigManager:
    """Quản lý cấu hình ứng dụng"""
    
    def __init__(self, config_file: str = "config/settings.json"):
        self.config_file = config_file
        self.config = self.load_config()
        
    def load_config(self) -> Dict[str, Any]:
        """Tải cấu hình từ file"""
        try:
            if os.path.exists(self.config_file):
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            else:
                return self.get_default_config()
        except Exception as e:
            print(f"Lỗi khi tải cấu hình: {e}")
            return self.get_default_config()
    
    def save_config(self) -> bool:
        """Lưu cấu hình vào file"""
        try:
            os.makedirs(os.path.dirname(self.config_file), exist_ok=True)
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(self.config, f, indent=4, ensure_ascii=False)
            return True
        except Exception as e:
            print(f"Lỗi khi lưu cấu hình: {e}")
            return False
    
    def get_default_config(self) -> Dict[str, Any]:
        """Trả về cấu hình mặc định"""
        return {
            "trading_mode": "Scalp",
            "available_capital": 10000,
            "target_profit_per_trade": 50,
            "max_loss_per_trade": 25,
            "tokens": ["BTCUSDT", "SOLUSDT", "ETHUSDT"],
            "timeframes": ["1m", "5m", "15m", "30m", "1h", "4h", "1d"],
            "scalp_timeframes": ["1m", "5m", "15m"],
            "swing_timeframes": ["1h", "4h", "1d"],
            "indicators": {
                "scalp": {
                    "rsi_period": 14,
                    "ma_fast": 10,
                    "ma_slow": 20,
                    "macd_fast": 12,
                    "macd_slow": 26,
                    "macd_signal": 9
                },
                "swing": {
                    "rsi_period": 14,
                    "ma_fast": 20,
                    "ma_slow": 50,
                    "macd_fast": 12,
                    "macd_slow": 26,
                    "macd_signal": 9
                }
            },
            "risk_management": {
                "max_leverage": 20,
                "default_leverage": 10,
                "risk_per_trade": 0.02
            }
        }
    
    def get_trading_config(self) -> TradingConfig:
        """Trả về cấu hình giao dịch"""
        return TradingConfig(
            trading_mode=self.config.get("trading_mode", "Scalp"),
            available_capital=self.config.get("available_capital", 10000.0),
            target_profit_per_trade=self.config.get("target_profit_per_trade", 50.0),
            max_loss_per_trade=self.config.get("max_loss_per_trade", 25.0),
            tokens=self.config.get("tokens", ["BTCUSDT", "SOLUSDT", "ETHUSDT"]),
            timeframes=self.config.get("timeframes", ["1m", "5m", "15m", "30m", "1h", "4h", "1d"])
        )
    
    def update_trading_config(self, config: TradingConfig):
        """Cập nhật cấu hình giao dịch"""
        self.config.update({
            "trading_mode": config.trading_mode,
            "available_capital": config.available_capital,
            "target_profit_per_trade": config.target_profit_per_trade,
            "max_loss_per_trade": config.max_loss_per_trade,
            "tokens": config.tokens,
            "timeframes": config.timeframes
        })
        self.save_config()
    
    def get_timeframes_for_mode(self, mode: str) -> List[str]:
        """Trả về khung thời gian phù hợp với chế độ giao dịch"""
        if mode.lower() == "scalp":
            return self.config.get("scalp_timeframes", ["1m", "5m", "15m"])
        else:  # swing
            return self.config.get("swing_timeframes", ["1h", "4h", "1d"])
    
    def get_indicators_config(self, mode: str) -> Dict[str, Any]:
        """Trả về cấu hình chỉ báo cho chế độ giao dịch"""
        indicators = self.config.get("indicators", {})
        return indicators.get(mode.lower(), indicators.get("scalp", {}))
    
    def get_risk_management_config(self) -> Dict[str, Any]:
        """Trả về cấu hình quản lý rủi ro"""
        return self.config.get("risk_management", {
            "max_leverage": 20,
            "default_leverage": 10,
            "risk_per_trade": 0.02
        }) 