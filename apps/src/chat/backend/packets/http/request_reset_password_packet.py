from ..packet import Packet

class RequestResetPasswordPacket(Packet):

    def __init__(self, username: str, email: str):
        self._username = username
        self._email = email

    def get_type(self):
        return "request_reset_password"

    def to_data(self):
        return {
            "type": self.get_type(),
            "username": self._username,
            "email": self._email
        }

    @staticmethod
    def from_data(data):
        return RequestResetPasswordPacket(data["username"], data["email"])

    def get_username(self) -> str:
        return self._username
    
    def get_email(self) -> str:
        return self._email