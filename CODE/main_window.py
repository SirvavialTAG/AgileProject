from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QLineEdit, QPushButton, QListWidget, QWidget, QTabWidget, QMessageBox, QLabel, QTextEdit
from database_manager import DatabaseManager
from datetime import datetime, timedelta

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
        self.tab_widget.addTab(self.repetition_tab, "Повторение")

        self.setup_cards_tab()
        self.setup_repetition_tab()

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

    def setup_repetition_tab(self):
        layout = QVBoxLayout()

        self.ready_label = QLabel("Карточек для повторения: 0")
        layout.addWidget(self.ready_label)

        self.start_review_button = QPushButton("Начать повторение")
        self.start_review_button.clicked.connect(self.start_review)
        layout.addWidget(self.start_review_button)

        self.review_front_label = QLabel()
        layout.addWidget(self.review_front_label)

        self.review_back_label = QTextEdit()
        self.review_back_label.setReadOnly(True)
        layout.addWidget(self.review_back_label)

        self.show_answer_button = QPushButton("Показать ответ")
        self.show_answer_button.clicked.connect(self.show_answer)
        layout.addWidget(self.show_answer_button)

        self.feedback_buttons = QWidget()
        feedback_layout = QVBoxLayout()

        self.again_button = QPushButton("Снова")
        self.again_button.clicked.connect(lambda: self.give_feedback("again"))
        feedback_layout.addWidget(self.again_button)

        self.good_button = QPushButton("Хорошо")
        self.good_button.clicked.connect(lambda: self.give_feedback("good"))
        feedback_layout.addWidget(self.good_button)

        self.easy_button = QPushButton("Легко")
        self.easy_button.clicked.connect(lambda: self.give_feedback("easy"))
        feedback_layout.addWidget(self.easy_button)

        self.feedback_buttons.setLayout(feedback_layout)
        layout.addWidget(self.feedback_buttons)

        self.repetition_tab.setLayout(layout)
        self.load_ready_cards()

    def load_ready_cards(self):
        today = datetime.now().date()
        cards = self.db_manager.get_cards()
        ready_count = sum(1 for card in cards if datetime.strptime(card[4], "%Y-%m-%d").date() <= today)
        self.ready_label.setText(f"Карточек для повторения: {ready_count}")

    def start_review(self):
        self.current_review_cards = [
            card for card in self.db_manager.get_cards()
            if datetime.strptime(card[4], "%Y-%m-%d").date() <= datetime.now().date()
        ]
        if not self.current_review_cards:
            QMessageBox.information(self, "Информация", "Нет карточек для повторения.")
            return
        self.current_card_index = 0
        self.show_next_card()

    def show_next_card(self):
        if self.current_card_index < len(self.current_review_cards):
            card = self.current_review_cards[self.current_card_index]
            self.review_front_label.setText(card[1])
            self.review_back_label.clear()
        else:
            QMessageBox.information(self, "Информация", "Повторение завершено.")
            self.load_ready_cards()

    def show_answer(self):
        if self.current_card_index < len(self.current_review_cards):
            card = self.current_review_cards[self.current_card_index]
            self.review_back_label.setText(card[2])

    def give_feedback(self, feedback):
        if self.current_card_index < len(self.current_review_cards):
            card = self.current_review_cards[self.current_card_index]
            card_id = card[0]
            last_interval = card[5]

            if feedback == "again":
                next_interval = 0
                next_review_date = datetime.now().date()
            elif feedback == "good":
                next_interval = 1 if last_interval == 0 else int(last_interval * 1.5)
                next_review_date = datetime.now().date() + timedelta(days=next_interval)
            elif feedback == "easy":
                next_interval = 4 if last_interval == 0 else int(last_interval * 2.5)
                next_review_date = datetime.now().date() + timedelta(days=next_interval)

            self.db_manager.update_card_review_date(card_id, next_review_date, next_interval)
            self.current_card_index += 1
            self.show_next_card()

    def closeEvent(self, event):
        self.db_manager.close()
        event.accept()