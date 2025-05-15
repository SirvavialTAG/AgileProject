from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget, QTabWidget


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memora - The best memory application")
        self.setGeometry(100, 100, 800, 600)

        self.tab_widget = QTabWidget()
        self.setCentralWidget(self.tab_widget)

        self.cards_tab = QWidget()
        self.repetition_tab = QWidget()

        self.tab_widget.addTab(self.cards_tab, "Карточки")

        self.setup_cards_tab()

    def setup_cards_tab(self):
        layout = QVBoxLayout()

        self.front_input = QLineEdit()
        self.front_input.setPlaceholderText("Лицевая сторона")
        layout.addWidget(self.front_input)

        self.back_input = QLineEdit()
        self.back_input.setPlaceholderText("Обратная сторона")
        layout.addWidget(self.back_input)

        self.add_button = QPushButton("Добавить карточку")
        self.add_button.clicked.connect(self.add_card)
        layout.addWidget(self.add_button)

        self.cards_list = QListWidget()
        layout.addWidget(self.cards_list)

        self.delete_button = QPushButton("Удалить выбранную")
        self.delete_button.clicked.connect(self.delete_card)
        layout.addWidget(self.delete_button)

        self.cards_tab.setLayout(layout)
        self.load_cards()

    def add_card(self):
        pass

    def load_cards(self):
        pass

    def delete_card(self):
        pass