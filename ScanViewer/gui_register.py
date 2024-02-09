from PySide6 import QtWidgets, QtCore
from status import LoginStatus

class GUI_Register(QtWidgets.QWidget):
    main_window = QtCore.Signal()
    login_window = QtCore.Signal()

    def __init__(self):
        super().__init__()

        # Inicjalizacja elementów interfejsu użytkownika
        self.register_button = QtWidgets.QPushButton("Register")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.username_label = QtWidgets.QLabel("Username:")
        self.password_label = QtWidgets.QLabel("Password:")
        self.confirm_password_label = QtWidgets.QLabel("Confirm Password:")
        self.profession_label = QtWidgets.QLabel("Profession:")
        self.username_entry = QtWidgets.QLineEdit()
        self.password_entry = QtWidgets.QLineEdit()
        self.confirm_password_entry = QtWidgets.QLineEdit()
        self.profession_combo = QtWidgets.QComboBox()  # Lista rozwijana dla profesji
        self.profession_combo.addItems(["Doctor", "Guest", "Manager"])  # Dodanie opcji do listy rozwijanej
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password")  # Przycisk do odkrywania hasła
        self.register_label = QtWidgets.QLabel("Register", alignment=QtCore.Qt.AlignCenter)

        # Połączenia sygnałów z odpowiednimi metodami
        self.register_button.clicked.connect(self.try_register)
        self.cancel_button.clicked.connect(self.login_window.emit)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Układ interfejsu użytkownika
        register_layout = QtWidgets.QVBoxLayout(self)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(300, 170, 300, 100)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.confirm_password_label)
        layout.addWidget(self.confirm_password_entry)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.profession_label)
        layout.addWidget(self.profession_combo)
        layout.addWidget(self.register_button)
        layout.addWidget(self.cancel_button)

        # Dodanie etykiety do głównego układu
        font = self.register_label.font()
        font.setPointSize(30)
        self.register_label.setFont(font)
        register_layout.addWidget(self.register_label)
        register_layout.addLayout(layout)

    def try_register(self):
        # Pobranie danych z pól
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        profession = self.profession_combo.currentText()

        # Sprawdzenie poprawności danych
        if username == "" or password == "" or confirm_password =="":
            QtWidgets.QMessageBox.warning(self, "Registration Failed", "Missing data. Please try again.")
        elif  password == confirm_password:
            # Zapis danych do pliku
            with open("user_manager.txt", "a") as file:
                user_id = len(open("user_manager.txt").readlines()) + 1  # Nowe id użytkownika
                file.write(f"{user_id} {username} {password} {profession}\n")
            LoginStatus.set(user_id, LoginStatus.Profession[profession.upper()])
            self.main_window.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Registration Failed", "Passwords do not match. Please try again.")

    def toggle_password_visibility(self, state):
        # Przełączanie widoczności hasła
        if state:
            self.password_entry.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
            self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
