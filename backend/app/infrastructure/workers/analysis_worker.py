import asyncio
from typing import Dict, Any
import uuid
import logging
from ...application.services.word_analysis_service import WordAnalysisService
from ..repositories.excel_repository import ExcelRepository

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AnalysisWorker:
    """Воркер для обработки больших файлов в фоне"""
    
    def __init__(self, max_concurrent: int = 5):
        self.semaphore = asyncio.Semaphore(max_concurrent)
        self.tasks: Dict[str, Dict[str, Any]] = {}
        self.repository = ExcelRepository()
        logger.info(f"AnalysisWorker инициализирован с max_concurrent={max_concurrent}")
    
    async def submit(self, content: bytes, filename: str) -> str:
        """Отправить задачу на обработку"""
        task_id = str(uuid.uuid4())
        logger.info(f"Новая задача создана: {task_id} для файла {filename}")
        
        self.tasks[task_id] = {
            "status": "queued",
            "progress": 0,
            "message": "Задача добавлена в очередь"
        }
        
        asyncio.create_task(self._process(task_id, content, filename))
        return task_id
    
    async def _process(self, task_id: str, content: bytes, filename: str):
        """Обработка файла"""
        logger.info(f"Начало обработки задачи {task_id}")
        
        async with self.semaphore:
            try:
                logger.info(f"Задача {task_id}: этап 1 - чтение файла")
                self.tasks[task_id].update({
                    "status": "processing",
                    "progress": 25,
                    "message": "Чтение файла"
                })
                
                # Создаем сервис
                service = WordAnalysisService(self.repository)
                
                logger.info(f"Задача {task_id}: этап 2 - анализ текста")
                self.tasks[task_id].update({
                    "progress": 50,
                    "message": "Анализ текста"
                })
                
                # Анализируем файл
                result_path = await service.analyze_file(content, filename)
                logger.info(f"Задача {task_id}: анализ завершен, результат: {result_path}")
                
                logger.info(f"Задача {task_id}: этап 3 - сохранение результатов")
                self.tasks[task_id].update({
                    "progress": 75,
                    "message": "Сохранение результатов"
                })
                
                # Обновляем статус на завершенный
                self.tasks[task_id].update({
                    "status": "completed",
                    "progress": 100,
                    "message": "Готово!",
                    "result_path": result_path,
                    "filename": f"statistics_{filename}.xlsx"
                })
                
                logger.info(f"Задача {task_id}: успешно завершена")
                
            except Exception as e:
                logger.error(f"Задача {task_id}: ошибка - {str(e)}")
                self.tasks[task_id].update({
                    "status": "failed",
                    "error": str(e),
                    "message": f"Ошибка: {str(e)}"
                })
    
    def get_status(self, task_id: str) -> Dict[str, Any]:
        """Получить статус задачи"""
        status = self.tasks.get(task_id, {"status": "not_found"})
        logger.info(f"Запрос статуса для {task_id}: {status}")
        return status