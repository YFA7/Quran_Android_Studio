"""
Quran Database Module
Handles Quran data management, search, and retrieval
"""

import json
from pathlib import Path
from typing import List, Dict, Tuple, Optional


class QuranDatabase:
    """Database class for Quran information and metadata"""
    
    def __init__(self, data_file="quran_data.json"):
        self.data_file = Path(data_file)
        self.quran_data = self._load_quran_data()
        self.surahs = self._load_surahs()
        
    def _load_quran_data(self) -> Dict:
        """Load Quran data from JSON file"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except Exception as e:
                print(f"Error loading Quran data: {e}")
                return {}
        return {}
    
    def _load_surahs(self) -> List[Dict]:
        """Load Surah (Chapter) information - All 114 Surahs"""
        surahs = [
            {"number": 1, "name": "الفاتحة", "english": "Al-Fatiha", "meaning": "The Opening", "ayahs": 7, "type": "Meccan"},
            {"number": 2, "name": "البقرة", "english": "Al-Baqarah", "meaning": "The Cow", "ayahs": 286, "type": "Medinan"},
            {"number": 3, "name": "آل عمران", "english": "Ali Imran", "meaning": "The Family of Imran", "ayahs": 200, "type": "Medinan"},
            {"number": 4, "name": "النساء", "english": "An-Nisa", "meaning": "The Women", "ayahs": 176, "type": "Medinan"},
            {"number": 5, "name": "المائدة", "english": "Al-Ma'idah", "meaning": "The Table", "ayahs": 120, "type": "Medinan"},
            {"number": 6, "name": "الأنعام", "english": "Al-An'am", "meaning": "The Cattle", "ayahs": 165, "type": "Meccan"},
            {"number": 7, "name": "الأعراف", "english": "Al-A'raf", "meaning": "The Heights", "ayahs": 206, "type": "Meccan"},
            {"number": 8, "name": "الأنفال", "english": "Al-Anfal", "meaning": "The Spoils of War", "ayahs": 75, "type": "Medinan"},
            {"number": 9, "name": "التوبة", "english": "At-Tawbah", "meaning": "The Repentance", "ayahs": 129, "type": "Medinan"},
            {"number": 10, "name": "يونس", "english": "Yunus", "meaning": "Jonah", "ayahs": 109, "type": "Meccan"},
            # ... Add remaining 104 surahs
        ]
        return surahs
    
    def get_surah_info(self, surah_num: int) -> Optional[Dict]:
        """Get information about a specific Surah"""
        for surah in self.surahs:
            if surah["number"] == surah_num:
                return surah
        return None
    
    def get_all_surahs(self) -> List[Dict]:
        """Get all Surah information"""
        return self.surahs
    
    def search_text(self, keyword: str) -> List[Dict]:
        """Search for keyword in Quran text"""
        results = []
        if self.quran_data:
            for ayah in self.quran_data.get("ayahs", []):
                if keyword.lower() in ayah.get("text", "").lower():
                    results.append(ayah)
        return results
    
    def get_ayah(self, surah: int, ayah: int) -> str:
        """Get a specific ayah (verse)"""
        if self.quran_data:
            return self.quran_data.get(f"{surah}:{ayah}", "")
        return ""
    
    def get_surah_text(self, surah_num: int) -> List[str]:
        """Get all ayahs of a specific Surah"""
        ayahs = []
        if self.quran_data:
            for ayah_num in range(1, 300):  # Max ayahs in a surah
                ayah = self.quran_data.get(f"{surah_num}:{ayah_num}", "")
                if ayah:
                    ayahs.append(ayah)
                else:
                    break
        return ayahs
    
    def get_tafsir(self, surah: int, ayah: int) -> str:
        """Get tafsir (interpretation) of an ayah"""
        return "Tafsir not available in this version"


class PageMapper:
    """Maps Quran content to physical pages (Standard Mushaf)"""
    
    # Mapping of page number to (surah, ayah_start)
    # This is a partial mapping - expand with full 604 pages
    PAGE_SURAH_MAP = {
        1: (1, 1),      # Page 1: Surah Al-Fatiha
        2: (1, 6),
        3: (2, 1),
        4: (2, 26),
        # ... expand with remaining pages
    }
    
    @staticmethod
    def get_page_range(page_num: int) -> Tuple[int, int]:
        """Get surah and ayah range for a page"""
        return PageMapper.PAGE_SURAH_MAP.get(page_num, (1, 1))
    
    @staticmethod
    def get_page_for_ayah(surah: int, ayah: int) -> int:
        """Get page number for a specific ayah"""
        for page, (s, a) in PageMapper.PAGE_SURAH_MAP.items():
            if s == surah and a <= ayah:
                continue
            return page - 1
        return 1
