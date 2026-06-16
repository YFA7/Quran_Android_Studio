#!/usr/bin/env python3
"""
Quran Reader Application - Python Version
Main entry point for the GUI application
"""

import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
from pathlib import Path
import json

class QuranApp:
    def __init__(self, root):
        self.root = root
        self.root.title("قارئ القرآن - Quran Reader")
        self.root.geometry("1000x700")
        self.root.configure(bg="#f5f5dc")
        
        # Current state
        self.current_page = 1
        self.total_pages = 604
        self.bookmarks = self._load_bookmarks()
        self.assets_path = Path("assets/quran_pages")
        
        # Initialize UI components as None
        self.canvas = None
        self.page_label = None
        self.page_slider = None
        self.status_label = None
        self.photo_image = None
        
        # Setup UI FIRST
        self._setup_ui()
        
        # THEN load page
        self.root.after(100, lambda: self._load_page(self.current_page))
    
    def _setup_ui(self):
        """Setup the main application UI"""
        # Top Navigation Bar
        top_frame = ttk.Frame(self.root)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(
            top_frame,
            text="القرآن الكريم",
            font=("Arial", 28, "bold"),
            bg="#f5f5dc",
            fg="#2c3e50"
        )
        title_label.pack(anchor=tk.CENTER)
        
        # Control Frame
        control_frame = ttk.Frame(self.root)
        control_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Previous button
        ttk.Button(
            control_frame,
            text="◀ Previous",
            command=self.prev_page,
            width=12
        ).pack(side=tk.LEFT, padx=5)
        
        # Page indicator
        self.page_label = ttk.Label(
            control_frame,
            text=f"Page: {self.current_page}/{self.total_pages}"
        )
        self.page_label.pack(side=tk.LEFT, padx=20)
        
        # Page slider
        self.page_slider = ttk.Scale(
            control_frame,
            from_=1,
            to=self.total_pages,
            orient=tk.HORIZONTAL,
            command=self.on_slider_change
        )
        self.page_slider.set(self.current_page)
        self.page_slider.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        # Next button
        ttk.Button(
            control_frame,
            text="Next ▶",
            command=self.next_page,
            width=12
        ).pack(side=tk.RIGHT, padx=5)
        
        # Menu Bar
        menu_frame = ttk.Frame(self.root)
        menu_frame.pack(fill=tk.X, padx=10, pady=5)
        
        ttk.Button(
            menu_frame,
            text="🔖 Bookmark",
            command=self.toggle_bookmark
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            menu_frame,
            text="📋 Bookmarks",
            command=self.show_bookmarks
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            menu_frame,
            text="⚙️ Settings",
            command=self.open_settings
        ).pack(side=tk.LEFT, padx=3)
        
        ttk.Button(
            menu_frame,
            text="ℹ️ Info",
            command=self.show_info
        ).pack(side=tk.LEFT, padx=3)
        
        # Main Content Frame
        content_frame = ttk.Frame(self.root)
        content_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Canvas for page image
        self.canvas = tk.Canvas(
            content_frame,
            bg="white",
            highlightthickness=1,
            highlightbackground="#bdc3c7"
        )
        scrollbar = ttk.Scrollbar(content_frame, command=self.canvas.yview)
        self.canvas.configure(yscrollcommand=scrollbar.set)
        
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        # Bind mouse wheel
        self.canvas.bind("<MouseWheel>", self.on_canvas_scroll)
        self.canvas.bind("<Button-4>", self.on_canvas_scroll)
        self.canvas.bind("<Button-5>", self.on_canvas_scroll)
        
        # Status Bar
        status_frame = ttk.Frame(self.root)
        status_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.status_label = ttk.Label(
            status_frame,
            text="Ready",
            relief=tk.SUNKEN
        )
        self.status_label.pack(fill=tk.X)
    
    def _load_page(self, page_num):
        """Load and display a Quran page"""
        try:
            if page_num < 1 or page_num > self.total_pages:
                self.status_label.config(text=f"Invalid page: {page_num}")
                return
            
            self.current_page = page_num
            
            # Try multiple image formats
            image_path = None
            for ext in ['.png', '.jpg', '.jpeg', '.gif']:
                potential_path = self.assets_path / f"B_page_{page_num:03d}{ext}"
                if potential_path.exists():
                    image_path = potential_path
                    break
            
            if not image_path:
                # Try alternative naming patterns
                for naming_pattern in [f"A_intro_{page_num}.png", f"page_{page_num}.png", f"page_{page_num:03d}.png"]:
                    potential_path = self.assets_path / naming_pattern
                    if potential_path.exists():
                        image_path = potential_path
                        break
            
            if image_path and image_path.exists():
                try:
                    image = Image.open(image_path)
                    
                    # Get canvas dimensions
                    self.canvas.update()
                    canvas_width = self.canvas.winfo_width()
                    canvas_height = self.canvas.winfo_height()
                    
                    if canvas_width > 1 and canvas_height > 1:
                        image.thumbnail((canvas_width - 20, canvas_height - 20), Image.Resampling.LANCZOS)
                    
                    self.photo_image = ImageTk.PhotoImage(image)
                    self.canvas.delete("all")
                    self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
                    self.canvas.config(scrollregion=self.canvas.bbox("all"))
                    
                    # Update UI
                    if self.page_slider:
                        self.page_slider.set(page_num)
                    if self.page_label:
                        self.page_label.config(text=f"Page: {page_num}/{self.total_pages}")
                    
                    # Update status
                    bookmark_status = "🔖" if page_num in self.bookmarks else ""
                    if self.status_label:
                        self.status_label.config(text=f"Page {page_num} {bookmark_status}")
                    
                except Exception as e:
                    if self.status_label:
                        self.status_label.config(text=f"Error loading image: {str(e)}")
            else:
                if self.status_label:
                    self.status_label.config(text=f"Image not found for page {page_num}. Check assets/quran_pages/")
        except Exception as e:
            print(f"Error in _load_page: {e}")
            if self.status_label:
                self.status_label.config(text=f"Error: {str(e)}")
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages:
            self._load_page(self.current_page + 1)
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1:
            self._load_page(self.current_page - 1)
    
    def on_slider_change(self, value):
        """Handle slider change"""
        try:
            page = int(float(value))
            self._load_page(page)
        except:
            pass
    
    def on_canvas_scroll(self, event):
        """Handle mouse scroll on canvas"""
        try:
            if event.num == 5 or event.delta < 0:
                self.next_page()
            elif event.num == 4 or event.delta > 0:
                self.prev_page()
        except:
            pass
    
    def toggle_bookmark(self):
        """Add/remove current page from bookmarks"""
        if self.current_page in self.bookmarks:
            self.bookmarks.remove(self.current_page)
            messagebox.showinfo("Bookmark Removed", f"Page {self.current_page} removed from bookmarks")
        else:
            self.bookmarks.append(self.current_page)
            messagebox.showinfo("Bookmark Added", f"Page {self.current_page} bookmarked!")
        
        self._save_bookmarks()
        self._load_page(self.current_page)
    
    def show_bookmarks(self):
        """Show all bookmarks"""
        if not self.bookmarks:
            messagebox.showinfo("Bookmarks", "No bookmarks yet")
            return
        
        bookmarks_window = tk.Toplevel(self.root)
        bookmarks_window.title("Bookmarks")
        bookmarks_window.geometry("300x400")
        
        listbox = tk.Listbox(bookmarks_window)
        listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        for page in sorted(self.bookmarks):
            listbox.insert(tk.END, f"Page {page}")
        
        def go_to_bookmark():
            selection = listbox.curselection()
            if selection:
                page = sorted(self.bookmarks)[selection[0]]
                self._load_page(page)
                bookmarks_window.destroy()
        
        ttk.Button(bookmarks_window, text="Go To", command=go_to_bookmark).pack(pady=5)
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo("Settings", "Settings coming soon!\n\nFuture features:\n- Font size adjustment\n- Theme selection\n- Display options")
    
    def show_info(self):
        """Show application info"""
        info_text = """Quran Reader - Python Edition

Version 1.0
Islamic learning application

Features:
• Page-based Quran navigation (604 pages)
• Bookmark management
• Mouse wheel navigation
• Settings and customization

© 2026 - All rights reserved
Made with ❤️

السلام عليكم ورحمة الله وبركاته"""
        messagebox.showinfo("About Quran Reader", info_text)
    
    def _load_bookmarks(self):
        """Load bookmarks from file"""
        bookmarks_file = Path("bookmarks.json")
        if bookmarks_file.exists():
            try:
                with open(bookmarks_file, 'r') as f:
                    return json.load(f)
            except:
                return []
        return []
    
    def _save_bookmarks(self):
        """Save bookmarks to file"""
        try:
            with open("bookmarks.json", 'w') as f:
                json.dump(self.bookmarks, f)
        except Exception as e:
            print(f"Error saving bookmarks: {e}")


def main():
    root = tk.Tk()
    app = QuranApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
