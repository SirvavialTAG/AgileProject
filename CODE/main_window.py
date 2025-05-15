from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget, QTabWidget, QMessageBox
from database_manager import DatabaseManager


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Memora - The best memory application")
        self.setGeometry(100, 100, 800, 600)

        self.db_manager = DatabaseManager()

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
        front = self.front_input.text().strip()
        back = self.back_input.text().strip()

        if not front or not back:
            QMessageBox.warning(self, "Ошибка", "Оба поля должны быть заполнены.")
            return

        self.db_manager.add_card(front, back)
        self.front_input.clear()
        self.back_input.clear()
        self.load_cards()


    def load_cards(self):
        self.cards_list.clear()
        cards = self.db_manager.get_cards()
        for card in cards:
            self.cards_list.addItem(f"{card[0]}: {card[1]}")


    def delete_card(self):
        selected_item = self.cards_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Ошибка", "Выберите карточку для удаления.")
            return

        card_id = int(selected_item.text().split(":")[0])
        self.db_manager.delete_card(card_id)
        self.load_cards()
