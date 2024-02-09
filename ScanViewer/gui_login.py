from PySide6 import QtWidgets, QtCore
from status import LoginStatus

class GUI_Login(QtWidgets.QWidget):
    main_window = QtCore.Signal()
    register_window = QtCore.Signal()

    def __init__(self):
        super().__init__()

        # Inicjalizacja elementów interfejsu użytkownika
        self.login_button = QtWidgets.QPushButton("Login")
        self.register_button = QtWidgets.QPushButton("Register")
        self.username_label = QtWidgets.QLabel("Username:")
        self.password_label = QtWidgets.QLabel("Password:")
        self.username_entry = QtWidgets.QLineEdit()
        self.password_entry = QtWidgets.QLineEdit()
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password")
        self.login_label = QtWidgets.QLabel("Login", alignment=QtCore.Qt.AlignCenter)

        # Połączenie sygnałów z odpowiednimi metodami
        self.login_button.clicked.connect(self.try_login)
        self.register_button.clicked.connect(self.register_window.emit)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Układ interfejsu użytkownika
        login_layout = QtWidgets.QVBoxLayout(self)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(300, 170, 300, 200)
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_entry)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_entry)
        layout.addWidget(self.show_password_checkbox)
        layout.addWidget(self.login_button)
        layout.addWidget(self.register_button)

        font = self.login_label.font()
        font.setPointSize(30)
        self.login_label.setFont(font)
        login_layout.addWidget(self.login_label)
        login_layout.addLayout(layout)

    def try_login(self):
        # Logika weryfikacji loginu
        username = self.username_entry.text()
        password = self.password_entry.text()

        # Sprawdzenie czy użytkownik istnieje w pliku
        with open("user_manager.txt", "r") as file:
            for line in file:
                data = line.split()
                if len(data) >= 4 and data[1] == username and data[2] == password:
                    user_id = int(data[0])
                    profession = data[3]
                    LoginStatus.set(user_id, LoginStatus.Profession[profession.upper()])
                    self.main_window.emit()
                    return

        QtWidgets.QMessageBox.warning(self, "Login Failed", "Invalid username or password. Please try again.")

    def toggle_password_visibility(self, state):
        # Przełączanie widoczności hasła
        if state:
            self.password_entry.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
