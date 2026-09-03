from ..packet import Packet

class ResetPasswordPacket(Packet):

    def __init__(self, password: str, confirm_password: str, token: str):
        self._password = password
        self._confirm_password = confirm_password
        self._token = token

    def get_type(self):
        return "reset_password"

    def to_data(self):
        return {
            "type": self.get_type(),
            "password": self._password,
            "confirm_password": self._confirm_password,
            "token": self._token
        }

    @staticmethod
    def from_data(data):
        return ResetPasswordPacket(data["password"], data["confirm_password"], data["token"])

    def get_password(self) -> str:
        return self._password
    
    def get_confirm_password(self) -> str:
        return self._confirm_password
    
    def get_token(self) -> str:
        return self._token