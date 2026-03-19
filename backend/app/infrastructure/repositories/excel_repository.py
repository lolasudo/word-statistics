import pandas as pd
from typing import Dict, Any
import os
import logging
from ...domain.interfaces.statistics_repository import StatisticsRepository

logger = logging.getLogger(__name__)

class ExcelRepository(StatisticsRepository):
    """Реализация репозитория для сохранения в Excel"""
    
    def __init__(self, output_dir: str = "results"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)
        logger.info(f"ExcelRepository инициализирован, папка: {output_dir}")
    
    async def save(self, data: Dict[str, Any], filename: str) -> str:
        """Сохранить статистику в Excel файл"""
        logger.info(f"Сохранение результатов в {filename}")
        
        try:
            rows = []
            for word, word_data in data.items():
                logger.debug(f"Добавление строки: {word_data}")
                rows.append({
                    'Словоформа': word_data['word'],
                    'Кол-во во всём документе': word_data['total_count'],
                    'Кол-во в каждой строке': word_data['line_stats']
                })
            
            logger.info(f"Создано {len(rows)} строк для Excel")
            
            df = pd.DataFrame(rows)
            output_path = os.path.join(self.output_dir, filename)
            
            # Сохраняем в Excel
            df.to_excel(output_path, index=False)
            logger.info(f"Файл сохранен: {output_path}")
            
            # Проверяем, что файл создан
            if os.path.exists(output_path):
                file_size = os.path.getsize(output_path)
                logger.info(f"Файл создан успешно, размер: {file_size} байт")
            else:
                logger.error(f"Файл не создан: {output_path}")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Ошибка при сохранении Excel: {str(e)}")
            raise