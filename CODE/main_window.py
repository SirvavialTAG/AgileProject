from PyQt6.QtWidgets import QMainWindow


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memora - The best memory application")
        self.setGeometry(100, 100, 800, 600)