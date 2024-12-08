import os
import subprocess
import socket
import requests
from PyQt5 import QtWidgets, QtGui, QtCore

class SubdomainScanner(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Subdomain Scanner")
        self.setGeometry(100, 100, 800, 600)

        # Domain giriş alanı
        self.domain_label = QtWidgets.QLabel("Enter Domain:", self)
        self.domain_label.setGeometry(20, 20, 100, 30)
        
        self.domain_input = QtWidgets.QLineEdit(self)
        self.domain_input.setGeometry(130, 20, 400, 30)
        
        # Başlat düğmesi
        self.start_button = QtWidgets.QPushButton("Start Scan", self)
        self.start_button.setGeometry(550, 20, 100, 30)
        self.start_button.clicked.connect(self.start_scan)
        
        # Tablo
        self.result_table = QtWidgets.QTableWidget(self)
        self.result_table.setGeometry(20, 70, 760, 500)
        self.result_table.setColumnCount(4)
        self.result_table.setHorizontalHeaderLabels(["Subdomain", "Status Code", "IP Address", "Server"])
        self.result_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def start_scan(self):
        domain = self.domain_input.text().strip()
        if not domain:
            QtWidgets.QMessageBox.warning(self, "Error", "Please enter a domain!")
            return

        self.result_table.setRowCount(0)
        
        # Subfinder veya Amass ile subdomain taraması
        subdomains = self.get_subdomains(domain)
        if not subdomains:
            QtWidgets.QMessageBox.warning(self, "Error", "No subdomains found!")
            return

        for subdomain in subdomains:
            ip = self.resolve_ip(subdomain)
            status_code, server = self.fetch_info(subdomain)
            
            row_position = self.result_table.rowCount()
            self.result_table.insertRow(row_position)
            self.result_table.setItem(row_position, 0, QtWidgets.QTableWidgetItem(subdomain))
            self.result_table.setItem(row_position, 1, QtWidgets.QTableWidgetItem(str(status_code)))
            self.result_table.setItem(row_position, 2, QtWidgets.QTableWidgetItem(ip))
            self.result_table.setItem(row_position, 3, QtWidgets.QTableWidgetItem(server))

    def get_subdomains(self, domain):
        try:
            # Subfinder veya Amass çağrısı (dış araç)
            process = subprocess.run(["subfinder", "-d", domain], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
            subdomains = process.stdout.splitlines()
            return subdomains
        except Exception as e:
            print(f"Error running subfinder: {e}")
            return []

    def resolve_ip(self, domain):
        try:
            return socket.gethostbyname(domain)
        except socket.gaierror:
            return "Resolution Failed"

    def fetch_info(self, subdomain):
        try:
            response = requests.get(f"http://{subdomain}", timeout=5)
            return response.status_code, response.headers.get('Server', 'Unknown')
        except requests.exceptions.RequestException:
            return "N/A", "N/A"

# Uygulama başlatma
if __name__ == "__main__":
    app = QtWidgets.QApplication([])
    scanner = SubdomainScanner()
    scanner.show()
    app.exec_()
