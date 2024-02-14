from enum import Enum
#
class LoginStatus:
    class Profession(Enum):
        DOCTOR = "Doctor"
        GUEST = "Guest"
        MANAGER = "Manager"
        LOGGED_OUT = "Logged out"

    id = 0
    profession = Profession.LOGGED_OUT

    @staticmethod
    def set(id: int, profesion: Profession):
        LoginStatus.id = id
        LoginStatus.profession = profesion

    @staticmethod
    def reset():
        LoginStatus.id = 0
        LoginStatus.status = LoginStatus.Profession.LOGGED_OUT
    @staticmethod
    def read_profession():
        return LoginStatus.profession.value

    @staticmethod
    def read_id():
        return LoginStatus.id