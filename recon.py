import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import threading
import socket
import requests

results = []
scan_process = None
is_scanning = False
cancel_scan_flag = False
selected_status_codes = [200, 403]
total_domains = 0
processed_domains = 0

def start_scan():
    global is_scanning, cancel_scan_flag, total_domains, processed_domains
    domain = domain_entry.get()
    if not domain:
        messagebox.showerror("Hata", "Lütfen bir alan adı girin.")
        return

    if is_scanning:
        messagebox.showinfo("Bilgi", "Tarama zaten devam ediyor.")
        return

    is_scanning = True
    cancel_scan_flag = False
    processed_domains = 0
    total_domains = 0
    start_button.config(state="disabled", bg="lightblue")
    stop_button.config(state="normal", bg="red")
    refresh_button.config(state="disabled", bg="orange")
    progress_label.config(text="Tarama yapılıyor...")
    progress_bar["value"] = 0
    results.clear()
    update_table()

    threading.Thread(target=run_scan, args=(domain,), daemon=True).start()

def run_scan(domain):
    global scan_process, cancel_scan_flag, total_domains, processed_domains
    try:
        command = ["subfinder", "-d", domain, "-o", "subdomains.txt"]
        scan_process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

        subdomain_list = []
        for line in scan_process.stdout:
            if cancel_scan_flag:
                scan_process.terminate()
                break

            line = line.decode("utf-8").strip()
            if line:
                subdomain_list.append(line)

        total_domains = len(subdomain_list)
        progress_bar["maximum"] = total_domains

        for line in subdomain_list:
            ip = get_ip(line)
            status_code = get_status_code(line)
            technology = get_technology(line)
            server = get_server(line)
            
            if status_code in selected_status_codes:
                results.append((line, ip, status_code, technology, server))
                update_table()

            processed_domains += 1
            progress_bar["value"] = processed_domains
            progress_label.config(text=f"{processed_domains}/{total_domains} Subdomain tarandı.")

        is_scanning = False
        progress_label.config(text="Tarama Tamamlandı")
        messagebox.showinfo("Bilgi", "Subdomain taraması tamamlandı.")

    except Exception as e:
        messagebox.showerror("Hata", f"Tarama sırasında hata oluştu: {e}")
        is_scanning = False

def get_ip(subdomain):
    try:
        ip = socket.gethostbyname(subdomain)
        return ip
    except socket.gaierror:
        return "IP bulunamadı"

def get_status_code(subdomain):
    try:
        response = requests.get(f"http://{subdomain}")
        return response.status_code
    except requests.exceptions.RequestException:
        return "Hata"

def get_technology(subdomain):
    return "Teknoloji bilgisi bulunamadı"

def get_server(subdomain):
    try:
        response = requests.get(f"http://{subdomain}")
        return response.headers.get("Server", "Bilinmiyor")
    except requests.exceptions.RequestException:
        return "Hata"

def update_table():
    for item in table.get_children():
        table.delete(item)
    for result in results:
        table.insert("", "end", values=result)

def stop_scan():
    global cancel_scan_flag
    cancel_scan_flag = True
    stop_button.config(state="disabled", bg="red")
    refresh_button.config(state="normal", bg="orange")
    progress_label.config(text="Tarama durduruldu")

def refresh_scan():
    global results, is_scanning, processed_domains, total_domains
    results.clear()
    update_table()
    progress_bar["value"] = 0
    domain_entry.delete(0, tk.END)
    start_button.config(state="normal", bg="lightblue")
    stop_button.config(state="disabled", bg="red")
    refresh_button.config(state="disabled", bg="orange")
    progress_label.config(text="Tarama Başlatılmadı")
    processed_domains = 0
    total_domains = 0
    is_scanning = False

def show_details(event):
    item = table.item(table.focus())
    subdomain, ip, status_code, technology, server = item["values"]
    
    try:
        response = requests.get(f"http://{subdomain}")
        request_info = f"GET http://{subdomain} HTTP/1.1\nHost: {subdomain}\nUser-Agent: Subdomain-Scanner"
        response_info = f"HTTP/1.1 {response.status_code} {response.reason}\nHeaders: {response.headers}\nBody: {response.text[:200]}..."
        
        details_text = f"Subdomain: {subdomain}\nIP: {ip}\nStatus Code: {status_code}\nTechnology: {technology}\nServer: {server}\n\nRequest:\n{request_info}\n\nResponse:\n{response_info}"
    except requests.exceptions.RequestException:
        details_text = f"Subdomain: {subdomain}\nIP: {ip}\nStatus Code: {status_code}\nTechnology: {technology}\nServer: {server}\n\nRequest: Hata oluştu\nResponse: Hata oluştu"
    
    details_window = tk.Toplevel(root)
    details_window.title("Detaylı Bilgiler")
    
    details_text_widget = tk.Text(details_window, wrap="word", height=20, width=100, bg="black", fg="white", font=("Courier", 10))
    details_text_widget.insert("1.0", details_text)
    details_text_widget.config(state="normal")
    details_text_widget.pack(padx=10, pady=10)

    copy_button = tk.Button(details_window, text="Kopyala", command=lambda: copy_text(details_text_widget), bg="lightblue", font=("Arial", 10))
    copy_button.pack(pady=5)

def copy_text(text_widget):
    text_widget.clipboard_clear()
    text_widget.clipboard_append(text_widget.get("1.0", "end-1c"))
    messagebox.showinfo("Bilgi", "Metin kopyalandı!")

root = tk.Tk()
root.title("Subdomain Tarama Aracı")
root.configure(bg="black")

instagram_label = tk.Label(root, text="Instagram Adresi: @oktay.py", fg="white", bg="black", font=("Arial", 12))
instagram_label.pack(pady=5)

domain_label = tk.Label(root, text="Hedef Alan Adı", fg="white", bg="black", font=("Arial", 10))
domain_label.pack(pady=5)
domain_entry = tk.Entry(root, width=50)
domain_entry.pack(pady=5)

button_frame = tk.Frame(root, bg="black")
button_frame.pack(pady=5)

start_button = tk.Button(button_frame, text="Tarama Başlat", command=start_scan, state="normal", bg="lightblue", font=("Arial", 10))
start_button.grid(row=0, column=0, padx=10)

stop_button = tk.Button(button_frame, text="Tarama Durdur", command=stop_scan, state="disabled", bg="red", font=("Arial", 10))
stop_button.grid(row=0, column=1, padx=10)

refresh_button = tk.Button(button_frame, text="Yenile", command=refresh_scan, state="disabled", bg="orange", font=("Arial", 10))
refresh_button.grid(row=0, column=2, padx=10)

progress_label = tk.Label(root, text="Tarama Başlatılmadı", fg="white", bg="black")
progress_label.pack(pady=10)

progress_bar = ttk.Progressbar(root, length=300, mode="determinate")
progress_bar.pack(pady=5)

columns = ("Subdomain", "IP", "Status Code", "Technology", "Server")
table = ttk.Treeview(root, columns=columns, show="headings", height=10)
for col in columns:
    table.heading(col, text=col)
table.pack(pady=10)

table.bind("<Double-1>", show_details)

root.mainloop()
