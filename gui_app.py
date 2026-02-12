import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import threading
import bot
import sys

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Books Wolf Otomasyonu")
        self.root.geometry("600x500")
        
        self.file_path = "veriler.csv"
        self.is_running = False

        # Header
        header = tk.Label(root, text="Books Wolf Bot", font=("Helvetica", 16, "bold"))
        header.pack(pady=10)

        # File Selection Frame
        frame_file = tk.Frame(root)
        frame_file.pack(pady=5, padx=10, fill="x")

        self.btn_browse = tk.Button(frame_file, text="Dosya Seç (CSV/Excel)", command=self.browse_file)
        self.btn_browse.pack(side="left", padx=5)

        self.lbl_file = tk.Label(frame_file, text=self.file_path, fg="gray")
        self.lbl_file.pack(side="left", padx=5)

        # Control Buttons
        frame_ctrl = tk.Frame(root)
        frame_ctrl.pack(pady=10)

        self.btn_start = tk.Button(frame_ctrl, text="BOTU BAŞLAT", bg="green", fg="white", font=("Arial", 12, "bold"), command=self.start_bot, width=15)
        self.btn_start.pack(side="left", padx=10)

        self.btn_stop = tk.Button(frame_ctrl, text="DURDUR", bg="red", fg="white", font=("Arial", 12, "bold"), command=self.stop_bot, state="disabled", width=10)
        self.btn_stop.pack(side="left", padx=10)

        # Log Area
        tk.Label(root, text="İşlem Kayıtları:").pack(anchor="w", padx=10)
        self.txt_log = scrolledtext.ScrolledText(root, state='disabled', height=15)
        self.txt_log.pack(fill="both", expand=True, padx=10, pady=5)
        
        self.log_message("Uygulama hazır. Lütfen dosya seçip başlatın.")

    def browse_file(self):
        filename = filedialog.askopenfilename(filetypes=[("Data Files", "*.csv *.xlsx"), ("All Files", "*.*")])
        if filename:
            self.file_path = filename
            self.lbl_file.config(text=filename)
            self.log_message(f"Dosya seçildi: {filename}")

    def log_message(self, message):
        self.txt_log.config(state='normal')
        self.txt_log.insert(tk.END, str(message) + "\n")
        self.txt_log.see(tk.END)
        self.txt_log.config(state='disabled')

    def start_bot(self):
        if self.is_running: return
        
        self.is_running = True
        self.btn_start.config(state="disabled")
        self.btn_stop.config(state="normal")
        self.log_message("Bot başlatılıyor...")
        
        # Run bot in separate thread to keep GUI responsive
        self.thread = threading.Thread(target=self.run_bot_thread)
        self.thread.daemon = True
        self.thread.start()

    def stop_bot(self):
        if self.is_running:
            bot.STOP_BOT = True
            self.log_message("Durdurma isteği gönderildi...")
            self.btn_stop.config(state="disabled")

    def run_bot_thread(self):
        try:
            # We pass self.log_message directly as callback
            bot.run_bot(self.file_path, log_callback=self.log_callback_safe)
        except Exception as e:
            self.log_callback_safe(f"HATA: {e}")
        finally:
            self.is_running = False
            self.root.after(0, self.reset_buttons)

    def log_callback_safe(self, msg):
        # Update GUI from thread
        self.root.after(0, lambda: self.log_message(msg))

    def reset_buttons(self):
        self.btn_start.config(state="normal")
        self.btn_stop.config(state="disabled")
        self.log_message("Bot işlemi sonlandı.")

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
