import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import client.protocol as protocol
import threading
import os
import datetime


class ClientGUI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Secure File Transfer")
        self.root.geometry("460x430")
        self.root.resizable(False, False)
        self.failed_attempts = 0
        self.selected_files = []

        # Açık tema
        self.root.configure(bg="#F6F6F6")
        style = ttk.Style(self.root)
        style.theme_use('clam')
        style.configure("TLabel", background="#F6F6F6", foreground="#222831")
        style.configure("TButton", background="#E3F2FD", foreground="#222831", padding=4)
        style.configure("TProgressbar", background="#2196F3", troughcolor="#E0E0E0")

        ttk.Label(self.root, text="Sunucu IP:").grid(row=0, column=0, sticky="e", pady=2)
        self.server_ip_entry = ttk.Entry(self.root)
        self.server_ip_entry.insert(0, "127.0.0.1")
        self.server_ip_entry.grid(row=0, column=1, padx=7, pady=2, sticky="ew")

        ttk.Label(self.root, text="Kullanıcı Adı:").grid(row=1, column=0, sticky="e", pady=2)
        self.username_entry = ttk.Entry(self.root)
        self.username_entry.grid(row=1, column=1, padx=7, pady=2, sticky="ew")

        ttk.Label(self.root, text="Şifre:").grid(row=2, column=0, sticky="e", pady=2)
        self.password_entry = ttk.Entry(self.root, show="*")
        self.password_entry.grid(row=2, column=1, padx=7, pady=2, sticky="ew")

        # Protokol seçimi (yalnızca TCP aktif)
        self.protocol_var = tk.StringVar(value="TCP")
        ttk.Label(self.root, text="Protokol:").grid(row=3, column=0, sticky="e", pady=2)
        ttk.Radiobutton(self.root, text="TCP", variable=self.protocol_var, value="TCP").grid(row=3, column=1, sticky="w")
        ttk.Radiobutton(self.root, text="UDP (yakında)", variable=self.protocol_var, value="UDP", state=tk.DISABLED).grid(row=3, column=1, padx=70, sticky="w")

        self.file_label = ttk.Label(self.root, text="Henüz dosya seçilmedi", anchor="w")
        self.file_label.grid(row=4, column=0, columnspan=2, sticky="w", padx=10)

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=380, mode="determinate")
        self.progress.grid(row=5, column=0, columnspan=2, padx=10, pady=5)

        self.log_text = tk.Text(self.root, height=7, width=58, state=tk.DISABLED, bg="#F2F2F2", fg="#222831")
        self.log_text.grid(row=9, column=0, columnspan=2, padx=10, pady=6)

        self.select_btn = ttk.Button(self.root, text="Dosya(ları) Seç", command=self.choose_files)
        self.select_btn.grid(row=6, column=0, pady=8, sticky="ew", padx=10)

        self.send_btn = ttk.Button(self.root, text="Gönder", command=self.send_files, state=tk.DISABLED)
        self.send_btn.grid(row=6, column=1, pady=8, sticky="ew", padx=10)

        self.success_label = ttk.Label(self.root, text="", font=("Arial", 16), background="#F6F6F6", foreground="#2196F3")
        self.success_label.grid(row=7, column=0, columnspan=2)

        self.root.grid_columnconfigure(1, weight=1)
        self.root.mainloop()

    def log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.log_to_file(msg)

    def log_to_file(self, msg):
        with open("transfer_log.txt", "a", encoding="utf-8") as f:
            now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            f.write(f"[{now}] {msg}\n")

    def choose_files(self):
        paths = filedialog.askopenfilenames()
        if paths:
            self.selected_files = list(paths)
            if len(self.selected_files) == 1:
                self.file_label.config(text=f"Seçilen: {os.path.basename(self.selected_files[0])}")
            else:
                self.file_label.config(text=f"{len(self.selected_files)} dosya seçildi")
            self.send_btn.config(state=tk.NORMAL)
            self.log(f"{len(self.selected_files)} dosya seçildi")
        else:
            self.selected_files = []
            self.file_label.config(text="Henüz dosya seçilmedi")
            self.send_btn.config(state=tk.DISABLED)

    def send_files(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        server_ip = self.server_ip_entry.get()
        proto = self.protocol_var.get()
        files = self.selected_files

        if not username or not password:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre boş olamaz!")
            return
        if not files:
            messagebox.showerror("Hata", "Lütfen önce dosya seçin!")
            return
        if self.failed_attempts >= 3:
            messagebox.showerror("Kilit", "3 defa yanlış şifre girildi! Uygulama kilitlendi.")
            return

        self.progress["value"] = 0
        self.success_label.config(text="")
        self.send_btn.config(state=tk.DISABLED)
        self.select_btn.config(state=tk.DISABLED)

        threading.Thread(target=self.transfer_all_files, args=(files, username, password, server_ip, proto)).start()

    def transfer_all_files(self, files, username, password, server_ip, proto):
        toplam = len(files)
        for idx, file_path in enumerate(files, start=1):
            try:
                def progress_callback(ratio):
                    self.progress["value"] = int(ratio * 100)
                self.log(f"[{idx}/{toplam}] Gönderiliyor: {os.path.basename(file_path)}")
                # Şimdilik sadece TCP
                protocol.secure_send(file_path, username, password, server_ip=server_ip, progress_callback=progress_callback)
                self.progress["value"] = 100
                self.success_label.config(text="✔ Başarılı!")
                self.log(f"[{idx}/{toplam}] Başarılı: {os.path.basename(file_path)}")
                self.failed_attempts = 0
            except PermissionError:
                self.failed_attempts += 1
                self.log(f"[{idx}/{toplam}] Hatalı şifre ({self.failed_attempts}/3)")
                messagebox.showerror("Hata", f"{idx}. dosyada kullanıcı adı veya şifre yanlış!")
                if self.failed_attempts >= 3:
                    self.log("3 defa yanlış şifre! Giriş kilitlendi.")
                    messagebox.showerror("Kilit", "3 defa yanlış şifre girildi! Uygulama kilitlendi.")
                    break
            except Exception as e:
                self.log(f"[{idx}/{toplam}] HATA: {e}")
                messagebox.showerror("Hata", f"{idx}. dosya gönderilemedi: {e}")
        self.send_btn.config(state=tk.NORMAL if self.failed_attempts < 3 else tk.DISABLED)
        self.select_btn.config(state=tk.NORMAL)
        self.selected_files = []
        self.file_label.config(text="Henüz dosya seçilmedi")


if __name__ == "__main__":
    ClientGUI()
