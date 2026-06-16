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
        
        # Prevent recursion
        self.loading_page = False
        self.pending_page_load = None
        
        # Setup UI FIRST
        self._setup_ui()
        
        # THEN load page after a short delay
        self.root.after(200, self._deferred_load_page)
    
    def _deferred_load_page(self):
        """Deferred page loading to prevent recursion"""
        if not self.loading_page:
            self._load_page(self.current_page)
    
    def _setup_ui(self):
        """Setup the main application UI"""
        try:
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
                text="Loading...",
                relief=tk.SUNKEN
            )
            self.status_label.pack(fill=tk.X)
        except Exception as e:
            print(f"Error setting up UI: {e}")
    
    def _load_page(self, page_num):
        """Load and display a Quran page"""
        try:
            # Prevent recursion
            if self.loading_page:
                return
            
            self.loading_page = True
            
            # Validate components exist
            if not self.canvas or not self.status_label:
                self.loading_page = False
                return
            
            # Validate page number
            if page_num < 1 or page_num > self.total_pages:
                page_num = 1
            
            self.current_page = page_num
            
            # Try to find the image file
            image_path = None
            
            # Try primary naming convention: B_page_XXX.png
            for ext in ['.png', '.jpg', '.jpeg', '.gif']:
                test_path = self.assets_path / f"B_page_{page_num:03d}{ext}"
                if test_path.exists():
                    image_path = test_path
                    break
            
            # If not found, try alternative names
            if not image_path:
                alt_names = [
                    f"page_{page_num:03d}.png",
                    f"page_{page_num}.png",
                    f"intro_{page_num}.png",
                ]
                for alt_name in alt_names:
                    test_path = self.assets_path / alt_name
                    if test_path.exists():
                        image_path = test_path
                        break
            
            # Display the image or show error
            if image_path and image_path.exists():
                self._display_image(image_path, page_num)
            else:
                self.status_label.config(
                    text=f"⚠️ Image not found: assets/quran_pages/B_page_{page_num:03d}.png"
                )
                self.canvas.delete("all")
                self.canvas.create_text(
                    self.canvas.winfo_width() // 2,
                    self.canvas.winfo_height() // 2,
                    text=f"Page {page_num} image not found\n\nPlace images in: assets/quran_pages/",
                    font=("Arial", 14),
                    fill="gray"
                )
            
            self.loading_page = False
            
        except RecursionError:
            self.loading_page = False
            if self.status_label:
                self.status_label.config(text="❌ Recursion error - please restart")
        except Exception as e:
            self.loading_page = False
            print(f"Error in _load_page: {e}")
            try:
                if self.status_label:
                    self.status_label.config(text=f"Error: {str(e)[:50]}")
            except:
                pass
    
    def _display_image(self, image_path, page_num):
        """Display an image on the canvas"""
        try:
            image = Image.open(image_path)
            
            # Get canvas dimensions safely
            self.canvas.update_idletasks()
            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()
            
            if canvas_width > 100 and canvas_height > 100:
                # Resize image to fit canvas
                image.thumbnail(
                    (canvas_width - 20, canvas_height - 20),
                    Image.Resampling.LANCZOS
                )
            
            # Convert to PhotoImage and display
            self.photo_image = ImageTk.PhotoImage(image)
            self.canvas.delete("all")
            self.canvas.create_image(0, 0, image=self.photo_image, anchor=tk.NW)
            self.canvas.config(scrollregion=self.canvas.bbox("all"))
            
            # Update page indicator
            if self.page_slider:
                self.page_slider.set(page_num)
            if self.page_label:
                self.page_label.config(text=f"Page: {page_num}/{self.total_pages}")
            
            # Update status bar
            bookmark_icon = "🔖" if page_num in self.bookmarks else "  "
            if self.status_label:
                self.status_label.config(text=f"{bookmark_icon} Page {page_num}/{self.total_pages}")
            
        except Exception as e:
            print(f"Error displaying image: {e}")
            if self.status_label:
                self.status_label.config(text=f"Error: {str(e)[:50]}")
    
    def next_page(self):
        """Go to next page"""
        if self.current_page < self.total_pages and not self.loading_page:
            self._load_page(self.current_page + 1)
    
    def prev_page(self):
        """Go to previous page"""
        if self.current_page > 1 and not self.loading_page:
            self._load_page(self.current_page - 1)
    
    def on_slider_change(self, value):
        """Handle slider change"""
        try:
            page = int(float(value))
            if not self.loading_page and page != self.current_page:
                self._load_page(page)
        except:
            pass
    
    def on_canvas_scroll(self, event):
        """Handle mouse scroll on canvas"""
        if self.loading_page:
            return
        try:
            if event.num == 5 or event.delta < 0:
                self.next_page()
            elif event.num == 4 or event.delta > 0:
                self.prev_page()
        except:
            pass
    
    def toggle_bookmark(self):
        """Add/remove current page from bookmarks"""
        try:
            if self.current_page in self.bookmarks:
                self.bookmarks.remove(self.current_page)
                messagebox.showinfo("Success", f"Removed bookmark from page {self.current_page}")
            else:
                self.bookmarks.append(self.current_page)
                messagebox.showinfo("Success", f"Bookmarked page {self.current_page}")
            
            self._save_bookmarks()
            
            # Refresh page to update bookmark icon
            if not self.loading_page:
                current = self.current_page
                self.current_page = -1  # Force refresh
                self._load_page(current)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def show_bookmarks(self):
        """Show all bookmarks"""
        if not self.bookmarks:
            messagebox.showinfo("Bookmarks", "No bookmarks saved yet")
            return
        
        try:
            bookmarks_window = tk.Toplevel(self.root)
            bookmarks_window.title("Bookmarks")
            bookmarks_window.geometry("300x400")
            
            # Title
            ttk.Label(bookmarks_window, text="Saved Bookmarks:").pack(pady=5)
            
            # Listbox for bookmarks
            listbox = tk.Listbox(bookmarks_window, font=("Arial", 12))
            listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
            
            for page in sorted(self.bookmarks):
                listbox.insert(tk.END, f"Page {page}")
            
            def go_to_bookmark():
                selection = listbox.curselection()
                if selection:
                    page = sorted(self.bookmarks)[selection[0]]
                    self._load_page(page)
                    bookmarks_window.destroy()
            
            ttk.Button(
                bookmarks_window,
                text="Go To Selected",
                command=go_to_bookmark
            ).pack(pady=5)
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def open_settings(self):
        """Open settings dialog"""
        messagebox.showinfo(
            "Settings",
            "Settings coming soon!\n\nPlanned features:\n- Font size\n- Theme selection\n- Display options"
        )
    
    def show_info(self):
        """Show application info"""
        info_text = """Quran Reader - Python Edition

Version 1.0

Features:
• 604 Pages of the Quran
• Bookmark Management
• Mouse Navigation
• High-Quality Images

Image Location:
assets/quran_pages/

Image Format:
B_page_001.png to B_page_604.png

© 2026
السلام عليكم ورحمة الله وبركاته"""
        messagebox.showinfo("About", info_text)
    
    def _load_bookmarks(self):
        """Load bookmarks from file"""
        bookmarks_file = Path("bookmarks.json")
        if bookmarks_file.exists():
            try:
                with open(bookmarks_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    return data if isinstance(data, list) else []
            except:
                return []
        return []
    
    def _save_bookmarks(self):
        """Save bookmarks to file"""
        try:
            with open("bookmarks.json", 'w', encoding='utf-8') as f:
                json.dump(self.bookmarks, f)
        except Exception as e:
            print(f"Error saving bookmarks: {e}")


def main():
    root = tk.Tk()
    app = QuranApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
