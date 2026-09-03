from simple_framework.utils.json_parser import JSONParser

from .packet import Packet


class RegisterPacket(Packet):

    def __init__(
        self,
        username: str,
        email: str,
        password: str,
        confirm_password: str,
    ):
        self._username = username
        self._email = email
        self._password = password
        self._confirm_password = confirm_password

    def get_type(self) -> str:
        return "register"

    def to_data(self) -> dict:
        return {
            "type": self.get_type(),
            "username": self._username,
            "email": self._email,
            "password": self._password,
            "confirm_password": self._confirm_password,
        }

    @staticmethod
    def from_data(data: bytes) -> RegisterPacket | None:
        data = JSONParser.parse(data)
        if data.get("type") != "register":
            return None
        return RegisterPacket(
            data["username"],
            data["email"],
            data["password"],
            data["confirm_password"],
        )

    def get_username(self) -> str:
        return self._username

    def get_email(self) -> str:
        return self._email

    def get_password(self) -> str:
        return self._password

    def get_confirm_password(self) -> str:
        return self._confirm_password
