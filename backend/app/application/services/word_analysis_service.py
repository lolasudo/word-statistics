import re
from ...domain.entities.word_statistics import WordStatistics
from ...domain.interfaces.statistics_repository import StatisticsRepository

class WordAnalysisService:
    """Сервис для анализа слов в тексте"""
    
    def __init__(self, repository: StatisticsRepository):
        self.repository = repository
        
        self.word_pattern = re.compile(
            r'\bжител[ьяеиюй]?\b|\bжител[ьяеиюй]?м\b|\bжител[ьяеиюй]?ми\b|\bжител[ьяеиюй]?х\b',
            re.IGNORECASE
        )
    
    async def analyze_text(self, text: str) -> WordStatistics:
        """Анализ текста и подсчет статистики"""
        lines = text.split('\n')
        stats = WordStatistics()
        stats.set_line_count(len(lines))
        
        for line_idx, line in enumerate(lines):
            matches = self.word_pattern.findall(line.lower())
            for match in matches:
                stats.add_word_form(match, line_idx)
        
        return stats
    
    async def analyze_file(self, content: bytes, filename: str) -> str:
        """Анализ файла и сохранение результатов"""
        text = content.decode('utf-8', errors='ignore')
        stats = await self.analyze_text(text)
        output_filename = f"statistics_{filename}.xlsx"
        result_path = await self.repository.save(stats.to_dict(), output_filename)
        return result_path