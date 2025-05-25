import logging
import sys
from datetime import datetime

def setup_logger(name: str = "binance_bot", level: int = logging.INFO) -> logging.Logger:
    """Thiết lập logger cho ứng dụng"""
    
    # Tạo logger
    logger = logging.getLogger(name)
    logger.setLevel(level)
    
    # Tránh duplicate handlers
    if logger.handlers:
        return logger
    
    # Tạo formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)
    
    # File handler (optional)
    try:
        file_handler = logging.FileHandler(f'logs/bot_{datetime.now().strftime("%Y%m%d")}.log')
        file_handler.setLevel(level)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)
    except:
        pass  # Không tạo được file log thì bỏ qua
    
    return logger 