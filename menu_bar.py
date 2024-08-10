import os
from PyQt5.QtWidgets import QMenuBar, QMainWindow, QAction,  QColorDialog, QMessageBox #, QTextEdit, QWidget, QVBoxLayout, QPushButton,QFileDialog
#from PyQt5.QtCore import QFile, QTextStream
#from PyQt5.QtGui import QColor
import qdarkstyle
from qdarkstyle import load_stylesheet, LightPalette, DarkPalette

class MenuBar(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.menu_bar = QMenuBar(parent)
        self.current_background_color = "#19232d"  # Color de fondo inicial (el de qdarkstyle)
        self.current_text_color = "#FFFFFF"  # Color de texto inicial (blanco)
        self.scriptDir = os.path.dirname(os.path.realpath(__file__))
        self.initUI()

    def initUI(self):
        # Crear la barra de menús
        self.menu_bar = self.menuBar()

        # Crear los menús
        help_menu = self.menu_bar.addMenu('Ayuda')
        color_menu = self.menu_bar.addMenu('Colores')
        donate_menu = self.menu_bar.addMenu('Donar')
        exit_menu = self.menu_bar.addMenu('Salir')

        # Acciones del menú Ayuda
        help_action = QAction('Ver Ayuda', self)
        help_action.triggered.connect(self.show_help)
        help_menu.addAction(help_action)

        # Acciones del menú Colores
        color_background_action = QAction('Color Fondo', self)
        color_background_action.triggered.connect(lambda: self.open_color_dialog('background'))
        color_text_action = QAction('Color Textos', self)
        color_text_action.triggered.connect(lambda: self.open_color_dialog('text'))
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

    def open_color_dialog(self, element_type):
        # Obtener el color de fondo actual de un QPushButton específico
        self.button_bar_color = self.parent().save_button.palette().color(self.parent().save_button.backgroundRole()).name()
                
        # Almacenar el color previo de la ui
        previous_background_color = self.current_background_color
        previous_text_color = self.current_text_color

        color_dialog = QColorDialog()
        color_dialog.setOption(QColorDialog.ShowAlphaChannel, False)
        
        # Conectar la señal `currentColorChanged` para aplicar el color en tiempo real
        if element_type == 'background':
            color_dialog.currentColorChanged.connect(lambda color: self.apply_color(color, 'background'))
        elif element_type == 'text':
            color_dialog.currentColorChanged.connect(lambda color: self.apply_color(color, 'text'))
        
        # Ejecutar el diálogo para permitir la selección de color
        if color_dialog.exec_():
            selected_color = color_dialog.selectedColor()
            self.apply_color(selected_color, element_type)
        else:
            # Revertir los colores si el usuario cancela
            self.current_background_color = previous_background_color
            self.current_text_color = previous_text_color
            self.parent().setStyleSheet(f"background-color: {self.current_background_color}; color: {self.current_text_color};")

    def apply_color(self, color, element_type):
        if color.isValid():
            if element_type == 'background':
                self.current_background_color = color.name()  # Guardar el color de fondo actual
                self.parent().setStyleSheet(f"background-color: {self.current_background_color}; color: {self.current_text_color};")
            elif element_type == 'text':
                self.current_text_color = color.name()  # Guardar el color de texto actual
                self.parent().setStyleSheet(f"color: {self.current_text_color}; background-color: {self.current_background_color};")
        
        # Aplicar colores persistentes al estilo qdarkstyle
        self.menu_bar.setStyleSheet(f"background-color: {self.button_bar_color};")
        self.parent().save_button.setStyleSheet(f"background-color: {self.button_bar_color};")
        self.parent().delete_button.setStyleSheet(f"background-color: {self.button_bar_color};")
        self.parent().connect_button.setStyleSheet(f"background-color: {self.button_bar_color};")
    
    def menuBar(self):
        return self.menu_bar
    
    def reset_colores(self):
        self.parent().setStyleSheet(qdarkstyle.load_stylesheet(DarkPalette))
        # Vuelve al color de fondo y texto de qdarkstyle
        self.current_background_color = "#19232d"
        self.current_text_color = "#FFFFFF"  # Color de texto inicial (blanco)        
        

