import sys, os
import subprocess
import re
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidget, QTableWidgetItem, QPushButton, QVBoxLayout, QWidget, QLabel, QLineEdit, QHBoxLayout, QFormLayout
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import qdarkstyle
from qdarkstyle import load_stylesheet, LightPalette, DarkPalette
from menu_bar import MenuBar

class SSHGui(QMainWindow):
    def __init__(self):
        super().__init__()
        
        self.setWindowTitle("SSHconGUI Connector")
        self.setGeometry(100, 100, 600, 400)
        self.setFixedWidth(450)
        self.current_background_color = "#000000"  # Color de fondo inicial (negro)
        self.current_text_color = "#FFFFFF"  # Color de texto inicial (blanco)
        '''#BETTHER I LEFT THE MENU COLORES MANAGE THE CUSTOMIZED COLOURS...
        self.setStyleSheet(f"""
            background-color: {self.current_background_color};  /* Fondo negro */
            color: {self.current_text_color};  /* Texto blanco */
        """)
        '''
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.initUI()
        
    def initUI(self):
        # Integrar la barra de menús
        self.menu_bar = MenuBar(self)
        self.setMenuBar(self.menu_bar.menuBar())

        # Central widget and layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)
        
        # Form layout for input fields
        form_layout = QFormLayout()
        
        # Text fields to add new connection details
        self.conn_name_input = QLineEdit()
        self.conn_name_input.setPlaceholderText("Enter connection name")
        form_layout.addRow("Connection Name:",  self.conn_name_input)
        
        self.user_input = QLineEdit()
        self.user_input.setPlaceholderText("Enter username")
        form_layout.addRow("User Name:", self.user_input)
        
        self.ip_input = QLineEdit()
        self.ip_input.setPlaceholderText("Enter IP address")
        form_layout.addRow("IP SSH-Server xxx.xxx.xxx.xxx:", self.ip_input)
        main_layout.addLayout(form_layout)
        
        # Button to save new user and IP
        self.save_button = QPushButton("Add Connection")
        self.save_button.clicked.connect(self.save_user_ip)
        main_layout.addWidget(self.save_button)
        
        # Table to display user and IP
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Connection Name", "Username", "IP Address"])
        self.table.setSelectionBehavior(QTableWidget.SelectRows)
        main_layout.addWidget(self.table)
        
        # Buttons layout
        button_layout = QHBoxLayout()
        
        self.delete_button = QPushButton("Delete Selected")
        self.delete_button.clicked.connect(self.delete_selected)
        button_layout.addWidget(self.delete_button)
        
        self.connect_button = QPushButton("Connect")
        self.connect_button.clicked.connect(self.connect_ssh)
        button_layout.addWidget(self.connect_button)
        
        main_layout.addLayout(button_layout)
        
        # Load saved user and IP from file
        self.load_user_ips()

    def save_user_ip(self):
        conn_name = self.conn_name_input.text().strip()
        user = self.user_input.text().strip()
        ip = self.ip_input.text().strip()
        
        # Validate IP address format
        if re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            if conn_name and user and ip:
                with open(self.scriptDir+os.path.sep+"user_ips.txt", "a") as file:
                    file.write(f"{conn_name},{user},{ip}\n")
                self.conn_name_input.clear()
                self.user_input.clear()
                self.ip_input.clear()
                self.load_user_ips()
        else:
            self.ip_input.setText("Invalid IP format")
        if not re.match(r'^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}$', ip):
            QMessageBox.warning(self, "Error", "Formato de IP inválido.")
            return

    def load_user_ips(self):
        self.table.setRowCount(0)
        try:
            with open(self.scriptDir+os.path.sep+"user_ips.txt", "r") as file:
                lines = file.readlines()
                for line in lines:
                    parts = line.strip().split(',')
                    if len(parts) == 3:
                        conn_name, user, ip = parts
                        row_position = self.table.rowCount()
                        self.table.insertRow(row_position)
                        self.table.setItem(row_position, 0, QTableWidgetItem(conn_name))
                        self.table.setItem(row_position, 1, QTableWidgetItem(user))
                        self.table.setItem(row_position, 2, QTableWidgetItem(ip))
                self.table.resizeColumnsToContents()  # Adjust column widths to fit content
        except FileNotFoundError:
            pass

    def delete_selected(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            selected_row = selected_rows[0].row()
            conn_name = self.table.item(selected_row, 0).text()
            user = self.table.item(selected_row, 1).text()
            ip = self.table.item(selected_row, 2).text()
            
            with open(self.scriptDir+os.path.sep+"user_ips.txt", "r") as file:
                lines = file.readlines()
            with open(self.scriptDir+os.path.sep+"user_ips.txt", "w") as file:
                for line in lines:
                    if line.strip() != f"{conn_name},{user},{ip}":
                        file.write(line)
            self.load_user_ips()

    def connect_ssh(self):
        selected_rows = self.table.selectionModel().selectedRows()
        if selected_rows:
            selected_row = selected_rows[0].row()
            user = self.table.item(selected_row, 1).text()
            ip = self.table.item(selected_row, 2).text()
            command = f"ssh {user}@{ip}"
            subprocess.Popen(['xfce4-terminal', '-e', command])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
    main_win = SSHGui()
    main_win.show()
    sys.exit(app.exec_())
