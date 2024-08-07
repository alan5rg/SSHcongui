import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit

class SSHGui(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SSH Connector")
        self.setGeometry(100, 100, 500, 300)
        
        self.initUI()
        
    def initUI(self):
        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        
        # Label for the table
        self.label = QLabel("User and IP List:")
        layout.addWidget(self.label)
        
        # Table to display user and IP
        self.table = QTableWidget()
        self.table.setColumnCount(2)
        self.table.setHorizontalHeaderLabels(["Username", "IP Address"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        self.table.cellDoubleClicked.connect(self.connect_ssh)
        layout.addWidget(self.table)
        
        # Text fields to add new user and IP
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        layout.addWidget(self.user_input)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address")
        layout.addWidget(self.ip_input)
        
        # Button to save new user and IP
        self.save_button = QPushButton("Save User and IP")
        self.save_button.clicked.connect(self.save_user_ip)
        layout.addWidget(self.save_button)
        
        # Load saved user and IP from file
        self.load_user_ips()

    def save_user_ip(self):
        user = self.user_input.text().strip()
        ip = self.ip_input.text().strip()
        
        if user and ip:
            with open("user_ips.txt", "a") as file:
                file.write(f"{user},{ip}\n")
            self.user_input.clear()
            self.ip_input.clear()
            self.load_user_ips()

    def load_user_ips(self):
        self.table.setRowCount(0)
        try:
            with open("user_ips.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    user, ip = line.strip().split(',')
                    row_position = self.table.rowCount()
                    self.table.insertRow(row_position)
                    self.table.setItem(row_position, 0, QTableWidgetItem(user))
                    self.table.setItem(row_position, 1, QTableWidgetItem(ip))
        except FileNotFoundError:
            pass

    def connect_ssh(self, row, column):
        user_item = self.table.item(row, 0)
        ip_item = self.table.item(row, 1)
        
        if user_item and ip_item:
            user = user_item.text()
            ip = ip_item.text()
            command = f"ssh {user}@{ip}"
            subprocess.Popen(['xfce4-terminal', '-e', command])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    main_win = SSHGui()
    main_win.show()
    sys.exit(app.exec_())
