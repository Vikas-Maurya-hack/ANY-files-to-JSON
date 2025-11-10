# Modern GUI - Clean implementation
import tkinter as tk
from tkinter import ttk, filedialog, scrolledtext
from pathlib import Path
import threading
from datetime import datetime
import queue
import ctypes

# Fix blurry text on Windows - Enable DPI awareness
try:
    ctypes.windll.shcore.SetProcessDpiAwareness(1)  # Windows 8.1+
except:
    try:
        ctypes.windll.user32.SetProcessDPIAware()  # Windows Vista+
    except:
        pass

class ModernWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Universal Document Extractor v1.0")
        self.root.geometry("1400x900")
        
        # Dark theme colors
        self.c = {
            'bg1': '#0f172a',
            'bg2': '#1e293b',
            'bg3': '#334155',
            'blue': '#3b82f6',
            'cyan': '#06b6d4',
            'green': '#10b981',
            'red': '#ef4444',
            'orange': '#f59e0b',
            'purple': '#8b5cf6',
            'white': '#f1f5f9',
            'gray': '#94a3b8'
        }
        
        self.root.configure(bg=self.c['bg1'])
        
        # State
        self.selected_files = None
        self.selected_directory = None
        self.is_running = False
        self.msg_queue = queue.Queue()
        
        self.build_ui()
        
        # Start message queue processor
        self._process_queue()
    
    def build_ui(self):
        # Header
        header = tk.Frame(self.root, bg=self.c['blue'], height=80)
        header.pack(fill=tk.X)
        header.pack_propagate(False)
        
        tk.Label(
            header,
            text="📄 Universal Document Extractor",
            font=('Segoe UI', 24, 'bold'),
            bg=self.c['blue'],
            fg=self.c['white']
        ).pack(side=tk.LEFT, padx=30, pady=20)
        
        # Main area
        main = tk.Frame(self.root, bg=self.c['bg1'])
        main.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Left column
        left = tk.Frame(main, bg=self.c['bg1'], width=400)
        left.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 10))
        left.pack_propagate(False)
        
        # Right column
        right = tk.Frame(main, bg=self.c['bg1'])
        right.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # File selection card
        self.make_card(left, "📁 File Selection")
        card1_content = left.winfo_children()[-1]
        
        self.upload_btn = tk.Button(
            card1_content,
            text="📤 Upload Files",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['blue'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.select_files,
            height=2
        )
        self.upload_btn.pack(fill=tk.X, pady=(0, 10))
        
        self.folder_btn = tk.Button(
            card1_content,
            text="📁 Select Folder",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['cyan'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.select_directory,
            height=2
        )
        self.folder_btn.pack(fill=tk.X)
        
        self.status_label = tk.Label(
            card1_content,
            text="No files selected",
            font=('Segoe UI', 9),
            bg=self.c['bg2'],
            fg=self.c['gray']
        )
        self.status_label.pack(fill=tk.X, pady=(10, 0))
        
        # Progress card
        prog_card = tk.Frame(right, bg=self.c['bg2'])
        prog_card.pack(fill=tk.X, pady=(0, 10))
        
        prog_title_bar = tk.Frame(prog_card, bg=self.c['bg3'], height=40)
        prog_title_bar.pack(fill=tk.X)
        prog_title_bar.pack_propagate(False)
        
        tk.Label(
            prog_title_bar,
            text="⚡ Progress",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['bg3'],
            fg=self.c['white']
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        prog_content = tk.Frame(prog_card, bg=self.c['bg2'])
        prog_content.pack(fill=tk.X, padx=15, pady=15)
        
        # Progress bar
        self.prog_var = tk.DoubleVar()
        self.prog_bar = ttk.Progressbar(
            prog_content,
            variable=self.prog_var,
            maximum=100
        )
        self.prog_bar.pack(fill=tk.X, pady=(0, 10))
        
        self.prog_label = tk.Label(
            prog_content,
            text="0%",
            bg=self.c['bg2'],
            fg=self.c['white'],
            font=('Segoe UI', 10, 'bold')
        )
        self.prog_label.pack()
        
        # Buttons
        btn_frame = tk.Frame(prog_content, bg=self.c['bg2'])
        btn_frame.pack(fill=tk.X, pady=(15, 0))
        
        self.start_btn = tk.Button(
            btn_frame,
            text="▶️ Start",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['green'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.start_extraction,
            width=12,
            height=2
        )
        self.start_btn.grid(row=0, column=0, padx=5)
        
        self.stop_btn = tk.Button(
            btn_frame,
            text="⏸️ Stop",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['red'],
            fg='white',
            relief=tk.FLAT,
            cursor='hand2',
            command=self.stop_extraction,
            width=12,
            height=2,
            state=tk.DISABLED
        )
        self.stop_btn.grid(row=0, column=1, padx=5)
        
        tk.Button(
            btn_frame,
            text="🗑️ Clear",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['bg3'],
            fg=self.c['white'],
            relief=tk.FLAT,
            cursor='hand2',
            command=self.clear_log,
            width=12,
            height=2
        ).grid(row=0, column=2, padx=5)
        
        # Log card
        log_card = tk.Frame(right, bg=self.c['bg2'])
        log_card.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        
        log_title_bar = tk.Frame(log_card, bg=self.c['bg3'], height=40)
        log_title_bar.pack(fill=tk.X)
        log_title_bar.pack_propagate(False)
        
        tk.Label(
            log_title_bar,
            text="📝 Activity Log",
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['bg3'],
            fg=self.c['white']
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        log_content = tk.Frame(log_card, bg=self.c['bg2'])
        log_content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        self.log = scrolledtext.ScrolledText(
            log_content,
            wrap=tk.WORD,
            font=('Consolas', 10),
            bg=self.c['bg1'],
            fg=self.c['white'],
            relief=tk.FLAT
        )
        self.log.pack(fill=tk.BOTH, expand=True)
        
        self.log.tag_config('success', foreground=self.c['green'])
        self.log.tag_config('error', foreground=self.c['red'])
        self.log.tag_config('warning', foreground=self.c['orange'])
        self.log.tag_config('info', foreground=self.c['cyan'])
        
        self.log.config(state=tk.DISABLED)
    
    def make_card(self, parent, title):
        card = tk.Frame(parent, bg=self.c['bg2'])
        card.pack(fill=tk.X, pady=(0, 10))
        
        title_bar = tk.Frame(card, bg=self.c['bg3'], height=40)
        title_bar.pack(fill=tk.X)
        title_bar.pack_propagate(False)
        
        tk.Label(
            title_bar,
            text=title,
            font=('Segoe UI', 11, 'bold'),
            bg=self.c['bg3'],
            fg=self.c['white']
        ).pack(side=tk.LEFT, padx=15, pady=10)
        
        content = tk.Frame(card, bg=self.c['bg2'])
        content.pack(fill=tk.BOTH, expand=True, padx=15, pady=15)
        
        return content
    
    def select_files(self):
        files = filedialog.askopenfilenames(
            title="Select Files",
            filetypes=[("All Files", "*.*")]
        )
        if files:
            self.selected_files = list(files)
            self.selected_directory = None
            self.status_label.config(
                text=f"✅ {len(files)} file(s) selected",
                fg=self.c['green']
            )
            self.add_log(f"Selected {len(files)} file(s)", 'info')
    
    def select_directory(self):
        directory = filedialog.askdirectory(title="Select Folder")
        if directory:
            self.selected_directory = directory
            self.selected_files = None
            self.status_label.config(
                text=f"✅ Folder: {Path(directory).name}",
                fg=self.c['green']
            )
            self.add_log(f"Selected folder: {directory}", 'info')
    
    def start_extraction(self):
        if not self.selected_files and not self.selected_directory:
            self.add_log("⚠️ Please select files or folder first", 'warning')
            return
        
        self.is_running = True
        self.start_btn.config(state=tk.DISABLED)
        self.stop_btn.config(state=tk.NORMAL)
        self.add_log("🚀 Starting extraction...", 'info')
        
        threading.Thread(target=self.run_extraction, daemon=True).start()
    
    def stop_extraction(self):
        self.is_running = False
        self.start_btn.config(state=tk.NORMAL)
        self.stop_btn.config(state=tk.DISABLED)
        self.add_log("⏸️ Stopped", 'warning')
    
    def clear_log(self):
        self.log.config(state=tk.NORMAL)
        self.log.delete(1.0, tk.END)
        self.log.config(state=tk.DISABLED)
    
    def run_extraction(self):
        """Run actual document extraction"""
        try:
            # Import the real extraction function
            from main import extract_documents
            
            # Use selected files if available, otherwise use directory
            source = self.selected_files if self.selected_files else self.selected_directory
            
            # Run extraction with message queue for updates
            output_file = extract_documents(source, self.msg_queue)
            
            if output_file:
                self.add_log(f"✅ Output saved to: {output_file}", 'success')
            
        except Exception as e:
            self.add_log(f"❌ Extraction error: {str(e)}", 'error')
        finally:
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
    
    def add_log(self, msg, level='info'):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log.config(state=tk.NORMAL)
        self.log.insert(tk.END, f"[{timestamp}] {msg}\n", level)
        self.log.see(tk.END)
        self.log.config(state=tk.DISABLED)
    
    def _process_queue(self):
        """Process messages from worker threads"""
        try:
            while True:
                message = self.msg_queue.get_nowait()
                self._handle_message(message)
        except queue.Empty:
            pass
        
        # Schedule next check
        self.root.after(100, self._process_queue)
    
    def _handle_message(self, message):
        """Handle different message types from extraction thread"""
        msg_type = message[0]
        
        if msg_type == 'progress':
            # Update progress bar
            progress_data = message[1]
            percent = progress_data.get('progress_percent', 0)
            self.prog_var.set(percent)
            self.prog_label.config(text=f"{percent:.1f}%")
            
            # Update stats in log
            if progress_data.get('current_file'):
                filename = Path(progress_data['current_file']).name
                self.add_log(f"Processing: {filename}", 'info')
        
        elif msg_type == 'log':
            text, level = message[1], message[2]
            # Convert level to our tag names
            level_map = {
                'ERROR': 'error',
                'WARNING': 'warning',
                'SUCCESS': 'success',
                'INFO': 'info'
            }
            self.add_log(text, level_map.get(level, 'info'))
        
        elif msg_type == 'complete':
            output_file = message[1]
            self.add_log(f"🎉 Complete! Saved to: {output_file}", 'success')
            self.is_running = False
            self.start_btn.config(state=tk.NORMAL)
            self.stop_btn.config(state=tk.DISABLED)
            self.prog_var.set(100)
            self.prog_label.config(text="100%")
    
    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = ModernWindow()
    app.run()
