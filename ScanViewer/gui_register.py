from PySide6 import QtWidgets, QtCore
from status import LoginStatus
from storage import Storage

class GUI_Register(QtWidgets.QWidget):
    """Class representing the registration GUI."""

    # Signals for navigation between windows
    main_window = QtCore.Signal()
    login_window = QtCore.Signal()

    def __init__(self):
        """Initialize the registration GUI."""
        super().__init__()

        # Initialize user interface elements
        self.register_button = QtWidgets.QPushButton("Register")
        self.cancel_button = QtWidgets.QPushButton("Cancel")
        self.username_label = QtWidgets.QLabel("Username:")
        self.password_label = QtWidgets.QLabel("Password:")
        self.confirm_password_label = QtWidgets.QLabel("Confirm Password:")
        self.profession_label = QtWidgets.QLabel("Profession:")
        self.username_entry = QtWidgets.QLineEdit()
        self.password_entry = QtWidgets.QLineEdit()
        self.confirm_password_entry = QtWidgets.QLineEdit()
        self.profession_combo = QtWidgets.QComboBox()  # Dropdown list for professions
        self.profession_combo.addItems(["Doctor", "Patient", "Physician"])  # Adding options to the dropdown list
        self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
        self.show_password_checkbox = QtWidgets.QCheckBox("Show Password")  # Button to reveal password
        self.register_label = QtWidgets.QLabel("Register", alignment=QtCore.Qt.AlignCenter)

        # Connect signals to corresponding methods
        self.register_button.clicked.connect(self.try_register)
        self.cancel_button.clicked.connect(self.login_window.emit)
        self.show_password_checkbox.stateChanged.connect(self.toggle_password_visibility)

        # Layout of the user interface
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

        # Add label to the main layout
        font = self.register_label.font()
        font.setPointSize(30)
        self.register_label.setFont(font)
        register_layout.addWidget(self.register_label)
        register_layout.addLayout(layout)

    def try_register(self):
        """Attempt to register a new user."""
        # Get data from fields
        username = self.username_entry.text()
        password = self.password_entry.text()
        confirm_password = self.confirm_password_entry.text()
        profession = self.profession_combo.currentText()

        # Check data validity
        if username == "" or password == "" or confirm_password =="":
            QtWidgets.QMessageBox.warning(self, "Registration Failed", "Missing data. Please try again.")
        elif  password == confirm_password:
            # Save data to file
            Storage.add_user_to_file(username, password, profession)
            self.main_window.emit()
        else:
            QtWidgets.QMessageBox.warning(self, "Registration Failed", "Passwords do not match. Please try again.")

    def toggle_password_visibility(self, state):
        """Toggle password visibility."""
        if state:
            self.password_entry.setEchoMode(QtWidgets.QLineEdit.Normal)
            self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Normal)
        else:
            self.password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
            self.confirm_password_entry.setEchoMode(QtWidgets.QLineEdit.Password)
