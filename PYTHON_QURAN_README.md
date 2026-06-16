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
- ⌨️ Keyboard shortcuts

## Installation

### Requirements
- Python 3.8+
- Tkinter (usually comes with Python)
- PIL/Pillow

### Setup Steps

1. **Install dependencies:**
```bash
pip install Pillow
```

2. **Organize assets:**
   - Create an `assets/quran_pages/` directory
   - Place Quran page images (PNG/JPG format) in this directory
   - Image naming should follow: `B_page_001.png`, `B_page_002.png`, etc.

3. **Run the application:**
```bash
python quran_reader_python.py
```

## Project Structure

```
Quran_Android_Studio/
├── quran_reader_python.py      # Main application entry point
├── quran_database.py           # Quran data management
├── ui_manager.py               # UI styling and theming
├── bookmarks.json              # Saved bookmarks (auto-generated)
├── quran_data.json             # Optional: Quran text data
└── assets/
    └── quran_pages/            # Quran page images (604 pages)
        ├── B_page_001.png
        ├── B_page_002.png
        └── ...
```

## Usage

### Navigation
- **Next/Previous Buttons:** Navigate between pages
- **Page Slider:** Jump to any page
- **Mouse Scroll:** Scroll through pages (forward/backward)

### Bookmarking
- Click "🔖 Bookmark" to save current page
- Click "📋 Bookmarks" to view all bookmarks
- Click on a bookmark to jump to that page

### Settings
- Change theme (Light/Dark/Sepia)
- Adjust font size
- Configure display options

## Image Assets

The application requires high-quality Quran page images. Image naming convention:
- Format: `B_page_XXX.png` (where XXX is 001-604)
- Resolution: 1200x1600px minimum recommended
- Formats: PNG or JPG

### Free Online Sources for Quran Pages:
- [QuranComplex](https://www.qurancorplex.org/)
- [EveryAyah](https://everyayah.com/)
- [Archive.org](https://archive.org/)

## Keyboard Shortcuts (Coming Soon)

- `→` (Right Arrow) - Next page
- `←` (Left Arrow) - Previous page
- `Ctrl+B` - Add/Remove bookmark
- `Ctrl+F` - Open search
- `Ctrl+Q` - Quit application

## Customization

### Adding More Surahs Information
Edit `quran_database.py` and expand the `_load_surahs()` method with all 114 Surahs.

### Adding Quran Text
Create a `quran_data.json` file with format:
```json
{
  "1:1": "بِسْمِ اللَّهِ الرَّحْمَٰنِ الرَّحِيمِ",
  "1:2": "الْحَمْدُ لِلَّهِ رَبِّ الْعَالَمِينَ",
  ...
}
```

### Custom Themes
Add new themes in `ui_manager.py`:
```python
Theme.CUSTOM: {
    "bg": "#your_color",
    "fg": "#your_color",
    "button_bg": "#your_color",
    "accent": "#your_color",
}
```

## Future Enhancements

- [ ] Audio Quran recitation
- [ ] Tafsir (interpretation) display
- [ ] Translation support
- [ ] Dictionary/word meanings
- [ ] Advanced search
- [ ] PDF export
- [ ] Notes and highlights
- [ ] Reading statistics

## Troubleshooting

### Images not displaying
- Check `assets/quran_pages/` directory exists
- Verify images follow naming: `B_page_XXX.png`
- Ensure PNG or JPG format

### Application won't start
- Install Python 3.8+
- Install dependencies: `pip install Pillow`
- On Linux: `sudo apt-get install python3-tk`

### Slow performance
- Reduce image resolution (but maintain readability)
- Use SSD for faster file access

## License

MIT License - Feel free to use and modify

## Acknowledgments

- Islamic content from Quran.com
- Page images from QuranComplex
- Built with ❤️ for the Muslim community

---

**Made with ❤️ by YFA7**

السلام عليكم ورحمة الله وبركاته
