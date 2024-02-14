from enum import Enum

class LoginStatus:
    """Class representing the login status of users."""

    class Profession(Enum):
        """Enum for user professions."""
        DOCTOR = "Doctor"
        GUEST = "Guest"
        MANAGER = "Manager"
        LOGGED_OUT = "Logged out"

    id = 0
    profession = Profession.LOGGED_OUT

    @staticmethod
    def set(id: int, profession: Profession):
        """Set the login status."""
        LoginStatus.id = id
        LoginStatus.profession = profession

    @staticmethod
    def reset():
        """Reset the login status."""
        LoginStatus.id = 0
        LoginStatus.status = LoginStatus.Profession.LOGGED_OUT

    @staticmethod
    def read_profession():
        """Read the user's profession."""
        return LoginStatus.profession.value

    @staticmethod
    def read_id():
        """Read the user's ID."""
        return LoginStatus.id
