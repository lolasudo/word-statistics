from dataclasses import dataclass, field
from typing import Dict
from ..value_objects.word_form import WordForm

@dataclass
class WordStatistics:
    """Сущность статистики по словам"""
    word_forms: Dict[str, WordForm] = field(default_factory=dict)
    line_count: int = 0
    
    def add_word_form(self, word: str, line_index: int):
        """Добавить словоформу в статистику"""
        if word not in self.word_forms:
            self.word_forms[word] = WordForm(word, self.line_count)
        self.word_forms[word].add_occurrence(line_index)
    
    def set_line_count(self, count: int):
        """Установить общее количество строк"""
        self.line_count = count
        for word_form in self.word_forms.values():
            word_form.set_total_lines(count)
    
    def to_dict(self) -> dict:
        """Конвертация в словарь для экспорта"""
        return {
            word: form.to_dict() 
            for word, form in self.word_forms.items()
        }