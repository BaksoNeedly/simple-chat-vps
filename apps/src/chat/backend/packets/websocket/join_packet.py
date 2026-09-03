from ..packet import Packet

class JoinPacket(Packet):

    def __init__(self, username: str):
        self._username = username

    def to_data(self):
        return {
            "username": self._username,
            "type": "join"
        }

    @staticmethod
    def from_data(data):
        return JoinPacket(
            data["username"]
        )