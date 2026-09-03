from simple_framework.utils.json_parser import JSONParser

from .packet import Packet


class LoginPacket(Packet):

    def __init__(self, username: str, password: str):
        self._username = username
        self._password = password

    def get_type(self) -> str:
        return "login"

    def to_data(self) -> dict:
        return {
            "type": self.get_type(),
            "username": self._username,
            "password": self._password,
        }

    @staticmethod
    def from_data(data: bytes) -> LoginPacket | None:
        data = JSONParser.parse(data)
        if data.get("type") != "login":
            return None
        return LoginPacket(data["username"], data["password"])

    def get_username(self) -> str:
        return self._username

    def get_password(self) -> str:
        return self._password
