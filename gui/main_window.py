# ============================================================================
# GUI - Main application window
# ============================================================================

import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from pathlib import Path
import threading
from typing import Optional
import queue

class MainWindow:
    """Main GUI window for document extractor"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Universal Document Extractor v1.0")
        self.root.geometry("1100x800")
        self.root.minsize(900, 700)
        
        # Set modern theme colors
        self.colors = {
            'primary': '#2196F3',
            'success': '#4CAF50',
            'warning': '#FF9800',
            'error': '#F44336',
            'bg': '#f5f5f5',
            'text': '#333333'
        }
        
        # Configure style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # State
        self.selected_directory = None
        self.selected_files = None
        self.extraction_thread = None
        self.is_running = False
        self.message_queue = queue.Queue()
        
        # Build UI
        self._build_ui()
        
        # Start queue processor
        self._process_queue()
    
    def _build_ui(self):
        """Build the user interface"""
        # Configure root background
        self.root.configure(bg=self.colors['bg'])
        
        # Main container with padding
        main_container = ttk.Frame(self.root, padding="20")
        main_container.pack(fill=tk.BOTH, expand=True)
        
        # Header Section
        header_frame = tk.Frame(main_container, bg=self.colors['primary'], relief=tk.RAISED, bd=2)
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = tk.Label(
            header_frame,
            text="📄 Universal Document Extractor",
            font=("Segoe UI", 24, "bold"),
            fg="white",
            bg=self.colors['primary'],
            pady=15
        )
        title_label.pack()
        
        subtitle_label = tk.Label(
            header_frame,
            text="Extract content from 80+ file types • AI Training Ready • 100% Accurate",
            font=("Segoe UI", 11),
            fg="white",
            bg=self.colors['primary']
        )
        subtitle_label.pack(pady=15)
        
        # Quick Info Panel
        info_frame = tk.Frame(main_container, bg='white', relief=tk.GROOVE, bd=2)
        info_frame.pack(fill=tk.X, pady=(0, 15))
        
        info_text = tk.Label(
            info_frame,
            text="✓ Markdown  ✓ PDF  ✓ Word  ✓ Images  ✓ Code Files  ✓ Archives  ✓ Text Files",
            font=("Segoe UI", 10),
            fg=self.colors['text'],
            bg='white'
        )
        info_text.pack(pady=10)
        
        # File Selection Section
        selection_frame = ttk.LabelFrame(main_container, text=" 📂 Select Your Files ", padding="15")
        selection_frame.pack(fill=tk.X, pady=(0, 15))
        
        # Selection info
        self.dir_label = tk.Label(
            selection_frame,
            text="No files or folder selected",
            font=("Segoe UI", 10),
            fg="gray",
            bg='white',
            anchor='w'
        )
        self.dir_label.pack(fill=tk.X, pady=10)
        
        # Button container with better layout
        btn_container = tk.Frame(selection_frame, bg='white')
        btn_container.pack(fill=tk.X)
        
        # Create custom styled buttons
        self.select_files_btn = tk.Button(
            btn_container,
            text="📄 Select Files",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['primary'],
            fg='white',
            activebackground='#1976D2',
            activeforeground='white',
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2',
            command=self._browse_files
        )
        self.select_files_btn.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        
        self.select_folder_btn = tk.Button(
            btn_container,
            text="📁 Select Folder",
            font=("Segoe UI", 11, "bold"),
            bg=self.colors['primary'],
            fg='white',
            activebackground='#1976D2',
            activeforeground='white',
            relief=tk.FLAT,
            padx=30,
            pady=12,
            cursor='hand2',
            command=self._browse_directory
        )
        self.select_folder_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Stats Section
        stats_frame = ttk.LabelFrame(main_container, text=" 📊 File Statistics ", padding="15")
        stats_frame.pack(fill=tk.X, pady=(0, 15))
        
        self.stats_label = tk.Label(
            stats_frame,
            text="No files scanned yet",
            font=("Segoe UI", 10),
            fg=self.colors['text'],
            bg='white',
            justify='left',
            anchor='w'
        )
        self.stats_label.pack(fill=tk.X)
        
        # Progress Section
        progress_frame = ttk.LabelFrame(main_container, text=" ⚡ Extraction Progress ", padding="15")
        progress_frame.pack(fill=tk.BOTH, expand=True, pady=(0, 15))
        
        # Progress bar with custom style
        self.style.configure("Custom.Horizontal.TProgressbar", 
                           troughcolor='#e0e0e0', 
                           background=self.colors['success'],
                           thickness=25)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(
            progress_frame,
            variable=self.progress_var,
            maximum=100,
            mode='determinate',
            style="Custom.Horizontal.TProgressbar"
        )
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Progress percentage
        self.progress_percent = tk.Label(
            progress_frame,
            text="0%",
            font=("Segoe UI", 12, "bold"),
            fg=self.colors['success'],
            bg='white'
        )
        self.progress_percent.pack()
        
        # Progress stats
        self.progress_stats = tk.Label(
            progress_frame,
            text="Ready to start extraction",
            font=("Segoe UI", 10),
            fg=self.colors['text'],
            bg='white'
        )
        self.progress_stats.pack(pady=5)
        
        # Current file
        self.current_file_label = tk.Label(
            progress_frame,
            text="",
            font=("Segoe UI", 9, "italic"),
            fg=self.colors['primary'],
            bg='white',
            wraplength=1000
        )
        self.current_file_label.pack(pady=2)
        
        # Log area with custom styling
        log_header = tk.Label(
            progress_frame,
            text="📋 Activity Log",
            font=("Segoe UI", 11, "bold"),
            fg=self.colors['text'],
            bg='white',
            anchor='w'
        )
        log_header.pack(anchor=tk.W, pady=(10, 5))
        
        self.log_text = scrolledtext.ScrolledText(
            progress_frame,
            height=12,
            wrap=tk.WORD,
            state=tk.DISABLED,
            font=("Consolas", 9),
            bg='#f9f9f9',
            fg='#333333',
            relief=tk.SUNKEN,
            bd=2
        )
        self.log_text.pack(fill=tk.BOTH, expand=True, pady=(0, 10))
        
        # Control buttons with modern styling
        button_frame = tk.Frame(main_container, bg=self.colors['bg'])
        button_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Start button
        self.start_btn = tk.Button(
            button_frame,
            text="▶ Start Extraction",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['success'],
            fg='white',
            activebackground='#45a049',
            activeforeground='white',
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor='hand2',
            state=tk.DISABLED,
            command=self._start_extraction
        )
        self.start_btn.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        
        # Stop button
        self.stop_btn = tk.Button(
            button_frame,
            text="⏸ Stop",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['error'],
            fg='white',
            activebackground='#da190b',
            activeforeground='white',
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor='hand2',
            state=tk.DISABLED,
            command=self._stop_extraction
        )
        self.stop_btn.pack(side=tk.LEFT, padx=(0, 10), expand=True, fill=tk.X)
        
        # Clear button
        self.clear_btn = tk.Button(
            button_frame,
            text="🗑 Clear Log",
            font=("Segoe UI", 12, "bold"),
            bg=self.colors['warning'],
            fg='white',
            activebackground='#e68900',
            activeforeground='white',
            relief=tk.FLAT,
            padx=40,
            pady=15,
            cursor='hand2',
            command=self._clear_log
        )
        self.clear_btn.pack(side=tk.LEFT, expand=True, fill=tk.X)
        
        # Footer / Status bar with modern look
        footer_frame = tk.Frame(self.root, bg='#263238', relief=tk.FLAT, height=40)
        footer_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        self.status_bar = tk.Label(
            footer_frame,
            text="Ready • Select files or folder to begin",
            fg='white',
            bg='#263238',
            anchor=tk.W,
            font=("Segoe UI", 9)
        )
        self.status_bar.pack(fill=tk.BOTH, padx=20, pady=10)
    
    def _browse_directory(self):
        """Open directory browser"""
        directory = filedialog.askdirectory(
            title="Select Folder to Scan (All files in folder will be processed)"
        )
        
        if directory:
            self.selected_directory = Path(directory)
            self.selected_files = None  # Clear file selection
            self.dir_label.config(
                text=f"📁 Folder: {self.selected_directory}",
                fg=self.colors['success']
            )
            self._scan_files()
    
    def _browse_files(self):
        """Open file browser to select multiple files"""
        files = filedialog.askopenfilenames(
            title="Select Files to Extract",
            filetypes=[
                ("All Supported", "*.md *.markdown *.pdf *.docx *.doc *.png *.jpg *.jpeg *.txt *.json *.zip *.gz *.7z *.tar"),
                ("Markdown", "*.md *.markdown"),
                ("PDF", "*.pdf"),
                ("Word", "*.docx *.doc"),
                ("Images", "*.png *.jpg *.jpeg *.bmp *.gif *.tiff *.jfif"),
                ("Text", "*.txt *.log *.json *.xml *.csv"),
                ("Archives", "*.zip *.gz *.7z *.tar *.rar"),
                ("All Files", "*.*")
            ]
        )
        
        if files:
            self.selected_files = [Path(f) for f in files]
            self.selected_directory = None  # Clear folder selection
            self.dir_label.config(
                text=f"📄 {len(self.selected_files)} file(s) selected",
                fg=self.colors['success']
            )
            self._update_file_list()
    
    def _update_file_list(self):
        """Update the file list when files are selected"""
        if not self.selected_files:
            return
        
        self._log(f"✓ Selected {len(self.selected_files)} files:", "SUCCESS")
        for file_path in self.selected_files[:10]:  # Show first 10
            self._log(f"  • {file_path.name}")
        
        if len(self.selected_files) > 10:
            self._log(f"  ... and {len(self.selected_files) - 10} more files")
        
        self.status_bar.config(text=f"Ready • {len(self.selected_files)} files selected")
        self.start_btn.config(state=tk.NORMAL)
    
    def _scan_files(self):
        """Scan directory for supported files"""
        if not self.selected_directory:
            return
        
        self._log("Scanning directory for supported files...")
        self.status_bar.config(text="Scanning...")
        
        # Run scan in thread to keep UI responsive
        def scan_thread():
            from utils.file_scanner import FileScanner
            
            scanner = FileScanner()
            files = scanner.scan_directory(self.selected_directory)
            stats = scanner.get_file_stats(files)
            
            # Update UI
            self.message_queue.put(('scan_complete', files, stats))
        
        threading.Thread(target=scan_thread, daemon=True).start()
    
    def _start_extraction(self):
        """Start extraction process"""
        if (not self.selected_directory and not self.selected_files) or self.is_running:
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        
        # Import main processor
        from main import extract_documents
        
        # Use selected files if available, otherwise use directory
        source = self.selected_files if self.selected_files else self.selected_directory
        
        # Start extraction in thread
        self.extraction_thread = threading.Thread(
            target=extract_documents,
            args=(source, self.message_queue),
            daemon=True
        )
        self.extraction_thread.start()
        
        self._log("Extraction started...")
    
    def _stop_extraction(self):
        """Stop extraction process"""
        self.is_running = False
        self.stop_btn.config(state=tk.DISABLED)
        self._log("Stopping extraction...")
    
    def _clear_log(self):
        """Clear the log area"""
        self.log_text.config(state=tk.NORMAL)
        self.log_text.delete(1.0, tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _log(self, message: str, level: str = "INFO"):
        """Add message to log"""
        self.log_text.config(state=tk.NORMAL)
        
        # Color code by level
        if level == "ERROR":
            tag = "error"
            self.log_text.tag_config(tag, foreground="red")
        elif level == "WARNING":
            tag = "warning"
            self.log_text.tag_config(tag, foreground="orange")
        elif level == "SUCCESS":
            tag = "success"
            self.log_text.tag_config(tag, foreground="green")
        else:
            tag = "info"
        
        self.log_text.insert(tk.END, f"{message}\n", tag)
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
    
    def _process_queue(self):
        """Process messages from worker threads"""
        try:
            while True:
                message = self.message_queue.get_nowait()
                self._handle_message(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self._process_queue)
    
    def _handle_message(self, message):
        """Handle different message types"""
        msg_type = message[0]
        
        if msg_type == 'scan_complete':
            files, stats = message[1], message[2]
            self._handle_scan_complete(files, stats)
        
        elif msg_type == 'progress':
            progress_data = message[1]
            self._update_progress(progress_data)
        
        elif msg_type == 'log':
            text, level = message[1], message[2]
            self._log(text, level)
        
        elif msg_type == 'complete':
            self._handle_extraction_complete(message[1])
    
    def _handle_scan_complete(self, files, stats):
        """Handle scan completion"""
        stats_text = (
            f"✓ Found {stats['total_files']} files "
            f"({stats['total_size_human']}) in {len(stats['by_type'])} file types"
        )
        self.stats_label.config(text=stats_text)
        self.status_bar.config(text="Ready to extract • Click 'Start Extraction' to begin")
        self.start_btn.config(state=tk.NORMAL)
        self._log(f"Scan complete: {stats_text}", "SUCCESS")
    
    def _update_progress(self, data):
        """Update progress display"""
        percent = data['progress_percent']
        self.progress_var.set(percent)
        self.progress_percent.config(text=f"{percent:.1f}%")
        
        stats_text = (
            f"Processed: {data['processed']}/{data['total']} • "
            f"✓ Success: {data['successful']} • "
            f"✗ Failed: {data['failed']} • "
            f"⚡ {data['speed']} files/sec • "
            f"ETA: {data['eta']}"
        )
        self.progress_stats.config(text=stats_text)
        
        if data['current_file']:
            self.current_file_label.config(text=f"⚙ Processing: {data['current_file']}")
        
        self.status_bar.config(text=f"Extracting... {percent:.1f}% complete")
    
    def _handle_extraction_complete(self, output_file):
        """Handle extraction completion"""
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.progress_var.set(100)
        self.progress_percent.config(text="100%")
        self.status_bar.config(text="✓ Extraction complete!")
        self._log(f"✓ Extraction complete! Output saved to: {output_file}", "SUCCESS")
    
    def run(self):
        """Start the GUI"""
        self.root.mainloop()
