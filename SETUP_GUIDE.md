# Quran Reader - Python Edition

A modern desktop application for reading the Quran with page-based navigation, built with Python and Tkinter.

## Features

✨ **Core Features:**
- 📖 Page-based navigation (604 pages)
- 🔖 Bookmark management
- 🎨 Multiple themes (Light, Dark, Sepia)
- 🔍 Search functionality
- ⚡ Fast page loading
- 📱 Responsive UI
- 🌍 Support for Arabic text

## Installation

### Requirements
- Python 3.8+
- Tkinter (usually comes with Python)
- PIL/Pillow

### Setup Steps

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Organize assets:**
   - Quran page images should be in `assets/quran_pages/`
   - Use naming: `B_page_001.png` to `B_page_604.png`

3. **Run the application:**
```bash
python quran_reader_python.py
```

## Project Structure

```
├── quran_reader_python.py  # Main application
├── quran_database.py       # Data management
├── ui_manager.py           # UI styling
├── requirements.txt        # Dependencies
└── assets/quran_pages/     # Page images
```

## Usage

### Navigation
- **Next/Previous Buttons:** Navigate between pages
- **Page Slider:** Jump to any page
- **Mouse Scroll:** Forward/backward through pages

### Bookmarking
- Click "🔖 Bookmark" to save current page
- Click "📋 Bookmarks" to view all saved pages

## Getting Quran Page Images

Free online sources:
- [QuranComplex](https://www.qurancorpus.org/)
- [EveryAyah](https://everyayah.com/)
- [Archive.org](https://archive.org/)

**Format:** PNG or JPG, 1200x1600px minimum recommended

## Customization

Edit `ui_manager.py` to add custom themes or modify styling.

## License

MIT License - Open source and free to use

---

**Made with ❤️ by YFA7**

السلام عليكم ورحمة الله وبركاته
