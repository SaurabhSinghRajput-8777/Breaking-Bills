import sys
from PyQt5.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QLabel, 
                             QPushButton, QLineEdit, QTextEdit, QMessageBox, 
                             QWidget, QHBoxLayout)
from PyQt5.QtGui import QPalette, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Breaking Bill$")
        self.setGeometry(100, 100, 900, 400)
        self.setStyleSheet("background-color: #f0f8ff;")  # Light blue background

        # Layouts
        main_layout = QVBoxLayout()
        people_layout = QHBoxLayout()
        transaction_layout = QHBoxLayout()

        # Widgets for adding people
        self.person_entry = QLineEdit(self)
        self.person_entry.setPlaceholderText("Person Name")
        self.person_entry.setStyleSheet("border: 2px solid #4682b4; padding: 5px;")
        self.person_add_button = QPushButton("Add Person", self)
        self.person_add_button.setStyleSheet("background-color: #ff6347; color: white; padding: 10px;")
        self.person_remove_button = QPushButton("Remove Person", self)
        self.person_remove_button.setStyleSheet("background-color: #ff6347; color: white; padding: 10px;")
        self.person_clear_button = QPushButton("Clear People", self)
        self.person_clear_button.setStyleSheet("background-color: #ff6347; color: white; padding: 10px;")
        self.people_list = QTextEdit(self)
        self.people_list.setReadOnly(True)
        self.people_list.setStyleSheet("border: 2px solid #4682b4; padding: 5px;")

        people_layout.addWidget(self.person_entry)
        people_layout.addWidget(self.person_add_button)
        people_layout.addWidget(self.person_remove_button)
        people_layout.addWidget(self.person_clear_button)

        # Widgets for adding transactions
        self.payer_entry = QLineEdit(self)
        self.payer_entry.setPlaceholderText("Payer")
        self.payer_entry.setStyleSheet("border: 2px solid #4682b4; padding: 5px;")
        self.receiver_entry = QLineEdit(self)
        self.receiver_entry.setPlaceholderText("Receiver")
        self.receiver_entry.setStyleSheet("border: 2px solid #4682b4; padding: 5px;")
        self.amount_entry = QLineEdit(self)
        self.amount_entry.setPlaceholderText("Amount")
        self.amount_entry.setStyleSheet("border: 2px solid #4682b4; padding: 5px;")
        self.transaction_add_button = QPushButton("Add Transaction", self)
        self.transaction_add_button.setStyleSheet("background-color: #ff6347; color: white; padding: 10px;")
        self.transaction_remove_button = QPushButton("Remove Transaction", self)
        self.transaction_remove_button.setStyleSheet("background-color: #ff6347; color: white; padding: 10px;")
        self.transaction_clear_button = QPushButton("Clear Transactions", self)
        self.transaction_clear_button.setStyleSheet("background-color: #ff6347; color: white; padding: 10px;")
        self.transactions_list = QTextEdit(self)
        self.transactions_list.setReadOnly(True)
        self.transactions_list.setStyleSheet("border: 2px solid #4682b4; padding: 5px;")

        transaction_layout.addWidget(self.payer_entry)
        transaction_layout.addWidget(self.receiver_entry)
        transaction_layout.addWidget(self.amount_entry)
        transaction_layout.addWidget(self.transaction_add_button)
        transaction_layout.addWidget(self.transaction_remove_button)
        transaction_layout.addWidget(self.transaction_clear_button)

        # Calculate button
        self.calculate_button = QPushButton("Calculate Result", self)
        self.calculate_button.setStyleSheet("background-color: #4682b4; color: white; padding: 10px;")

        # Adding Widgets to main layout
        main_layout.addLayout(people_layout)
        main_layout.addWidget(self.people_list)
        main_layout.addLayout(transaction_layout)
        main_layout.addWidget(self.transactions_list)
        main_layout.addWidget(self.calculate_button)

        # Set the central widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

        # Data structures
        self.people_names = []
        self.people_indices = {}
        self.transactions = []

        # Connect signals and slots
        self.person_add_button.clicked.connect(self.add_person)
        self.person_remove_button.clicked.connect(self.remove_person)
        self.person_clear_button.clicked.connect(self.clear_people)
        self.transaction_add_button.clicked.connect(self.add_transaction)
        self.transaction_remove_button.clicked.connect(self.remove_transaction)
        self.transaction_clear_button.clicked.connect(self.clear_transactions)
        self.calculate_button.clicked.connect(self.calculate_result)

    def add_person(self):
        name = self.person_entry.text().strip()
        if not name:
            self.show_error("Name cannot be empty.")
            return
        if name in self.people_indices:
            self.show_error("Name already exists.")
            return
        self.people_names.append(name)
        self.people_indices[name] = len(self.people_names) - 1
        self.update_people_list()
        self.person_entry.clear()

    def update_people_list(self):
        self.people_list.setPlainText("\n".join(self.people_names))

    def remove_person(self):
        name = self.person_entry.text().strip()
        if not name:
            self.show_error("Name cannot be empty.")
            return
        if name not in self.people_indices:
            self.show_error("Name not found.")
            return
        self.people_names.remove(name)
        del self.people_indices[name]
        for i, name in enumerate(self.people_names):
            self.people_indices[name] = i
        self.update_people_list()
        self.person_entry.clear()

    def clear_people(self):
        self.people_names.clear()
        self.people_indices.clear()
        self.update_people_list()

    def add_transaction(self):
        try:
            payer = self.payer_entry.text().strip()
            receiver = self.receiver_entry.text().strip()
            amount = int(self.amount_entry.text().strip())
            if payer not in self.people_indices or receiver not in self.people_indices:
                raise ValueError("Payer or receiver name not recognized.")
            if amount <= 0:
                raise ValueError("Amount must be a positive integer.")
            self.transactions.append((payer, receiver, amount))
            self.update_transactions_list()
            self.payer_entry.clear()
            self.receiver_entry.clear()
            self.amount_entry.clear()
        except ValueError as e:
            self.show_error(f"Invalid input: {e}")

    def update_transactions_list(self):
        transactions_text = "\n".join(f"{t[0]} pays {t[2]} to {t[1]}" for t in self.transactions)
        self.transactions_list.setPlainText(transactions_text)

    def remove_transaction(self):
        try:
            payer = self.payer_entry.text().strip()
            receiver = self.receiver_entry.text().strip()
            amount = int(self.amount_entry.text().strip())
            if (payer, receiver, amount) not in self.transactions:
                raise ValueError("Transaction not found.")
            self.transactions.remove((payer, receiver, amount))
            self.update_transactions_list()
            self.payer_entry.clear()
            self.receiver_entry.clear()
            self.amount_entry.clear()
        except ValueError as e:
            self.show_error(f"Invalid input: {e}")

    def clear_transactions(self):
        self.transactions.clear()
        self.update_transactions_list()

    def calculate_net_balances(self):
        num_people = len(self.people_indices)
        net_balance = [0] * num_people
        for transaction in self.transactions:
            payer, receiver, amount = transaction
            net_balance[self.people_indices[payer]] -= amount
            net_balance[self.people_indices[receiver]] += amount
        return net_balance

    def get_min_index(self, balances):
        return balances.index(min(balances))

    def get_max_index(self, balances):
        return balances.index(max(balances))

    def minimize_cash_flow(self, net_balance):
        results = []

        def settle_debts():
            max_credit = self.get_max_index(net_balance)
            max_debit = self.get_min_index(net_balance)

            if net_balance[max_credit] == 0 and net_balance[max_debit] == 0:
                return

            min_amount = min(-net_balance[max_debit], net_balance[max_credit])
            net_balance[max_credit] -= min_amount
            net_balance[max_debit] += min_amount

            results.append(f"{self.people_names[max_credit]} pays {min_amount} to {self.people_names[max_debit]}")
            settle_debts()

        settle_debts()
        return results

    def calculate_result(self):
        if len(self.people_names) < 2:
            self.show_error("At least 2 people are required for cash flow minimization.")
            return

        net_balance = self.calculate_net_balances()
        if all(balance == 0 for balance in net_balance):
            self.show_info("No payments required, all balances are settled.")
        else:
            result = self.minimize_cash_flow(net_balance)
            result_message = '\n'.join(result)
            self.show_info(result_message)

    def show_error(self, message):
        QMessageBox.critical(self, "Error", message)

    def show_info(self, message):
        QMessageBox.information(self, "Result", message)

app = QApplication(sys.argv)
window = MainWindow()
window.show()
sys.exit(app.exec_())