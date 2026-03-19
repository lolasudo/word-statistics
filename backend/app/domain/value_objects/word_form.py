from dataclasses import dataclass, field
from typing import List

@dataclass
class WordForm:
    """Объект-значение для словоформы"""
    word: str
    total_lines: int
    occurrences: List[int] = field(default_factory=list)
    
    def __post_init__(self):
        self.total_count = 0
    
    def add_occurrence(self, line_index: int):
        """Добавить вхождение в конкретной строке"""
        self.occurrences.append(line_index)
        self.total_count = len(self.occurrences)
    
    def set_total_lines(self, total: int):
        """Установить общее количество строк"""
        self.total_lines = total
    
    def get_line_stats(self) -> str:
        """Получить статистику по строкам в виде строки"""
        line_stats = [0] * self.total_lines
        for line_num in self.occurrences:
            line_stats[line_num] += 1
        return ','.join(map(str, line_stats))
    
    def to_dict(self) -> dict:
        return {
            'word': self.word,
            'total_count': self.total_count,
            'line_stats': self.get_line_stats()
        }