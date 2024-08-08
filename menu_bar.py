import os
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QColorDialog, QMessageBox, QTextEdit, QWidget, QVBoxLayout, QPushButton
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QColor
import qdarkstyle
from qdarkstyle import load_stylesheet, LightPalette, DarkPalette

class MenuBar(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_background_color = "#000000"  # Color de fondo inicial (negro)
        self.current_text_color = "#FFFFFF"  # Color de texto inicial (blanco)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.initUI()

    def initUI(self):
        # Crear la barra de menús
        menu_bar = self.menuBar()

        # Crear los menús
        help_menu = menu_bar.addMenu('Ayuda')
        color_menu = menu_bar.addMenu('Colores')
        donate_menu = menu_bar.addMenu('Donar')
        exit_menu = menu_bar.addMenu('Salir')

        # Acciones del menú Ayuda
        help_action = QAction('Ver Ayuda', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        # Acciones del menú Colores
        color_background_action = QAction('Color Fondo', self)
        color_background_action.triggered.connect(lambda: self.change_color('background'))
        color_text_action = QAction('Color Textos', self)
        color_text_action.triggered.connect(lambda: self.change_color('text'))
        reset_colores_action = QAction('Colores por Defecto', self)
        reset_colores_action.triggered.connect(self.reset_colores)
        color_menu.addAction(color_background_action)
        color_menu.addAction(color_text_action)
        color_menu.addAction(reset_colores_action)

        # Acciones del menú Donar
        donate_action = QAction('Ver Donar', self)
        donate_action.triggered.connect(self.show_donate)
        donate_menu.addAction(donate_action)

        # Acciones del menú Salir
        exit_action = QAction('Salir', self)
        exit_action.triggered.connect(self.appCerrar)
        exit_menu.addAction(exit_action)

    def appCerrar(self):
        self.parent().close()

    def show_help(self):
        self.show_text_file(self.scriptDir+os.path.sep+'ayuda.txt', "Ayuda")

    def show_donate(self):
        self.show_text_file(self.scriptDir+os.path.sep+'donar.txt', "Donar")

    def show_text_file(self, file_path, title):
        try:
            with open(file_path, 'r') as file:
                content = file.read()
                text_dialog = QMessageBox(self)
                text_dialog.setWindowTitle(title)
                text_dialog.setText(content)
                text_dialog.exec_()
        except FileNotFoundError:
            QMessageBox.warning(self, "Error", f"No se encontró el archivo {file_path}.")

    def change_color(self, element_type):
        color = QColorDialog.getColor()
        if color.isValid():
            if element_type == 'background':
                self.current_background_color = color.name()  # Guardar el color de fondo actual
                self.parent().setStyleSheet(f"background-color: {color.name()}; color: {self.current_text_color};")
            elif element_type == 'text':
                self.current_text_color = color.name()  # Guardar el color de texto actual
                self.parent().setStyleSheet(f"color: {color.name()}; background-color: {self.current_background_color};")

    def reset_colores(self):
        self.parent().setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))

