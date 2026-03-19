from abc import ABC, abstractmethod
from typing import Dict, Any

class StatisticsRepository(ABC):
    """Интерфейс для сохранения статистики"""
    
    @abstractmethod
    async def save(self, data: Dict[str, Any], filename: str) -> str:
        """Сохранить статистику и вернуть путь к файлу"""
        pass