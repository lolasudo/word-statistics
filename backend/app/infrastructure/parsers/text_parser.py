from typing import List
import re

class TextParser:
    """Парсер для текстовых файлов"""
    
    @staticmethod
    async def parse(content: bytes) -> str:
        """Парсинг текстового файла"""
        return content.decode('utf-8', errors='ignore')
    
    @staticmethod
    async def split_into_lines(text: str) -> List[str]:
        """Разделение текста на строки"""
        return text.split('\n')