from ..models.room import Room

from simple_framework.http.response import HTTPResponse
from simple_framework.http.request import HTTPRequest
from simple_framework.utils.json_parser import JSONParser

from ..repositories.room_repository import RoomRepository
from simple_framework.session.session_manager import SessionManager
from simple_framework.session.client_session_manager import ClientSessionManager

from ..repositories.message_repository import MessageRepository
from ..repositories.message_read_repository import MessageReadRepository

from ..repositories.user_repository import UserRepository

from ..packets.message_packet import MessagePacket

class RoomController:

    @staticmethod
    def load_message(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        session_id = session.get_session_id()

        client_session = ClientSessionManager.get(session_id)

        if not client_session:
            return HTTPResponse(
                status="404",
                reason_phrase="Not Found"
            )

        packet = JSONParser.parse(request.get_body())
        
        
        target_user = UserRepository.get_by_username(packet["identifier"])
        if not target_user:
            return HTTPResponse(status="404", reason_phrase="Not Found")
        
        
        calculated_id = RoomRepository.calculate(client_session.get_username(), target_user.get_username())
        room = RoomRepository.get_by_id(calculated_id)
        if not room:            
            RoomRepository.create(
                Room(calculated_id),
                [client_session.get_username(), target_user.get_username()]
            )
        
        messages = [
            MessagePacket(
                content=message.get_content(),
                created_at=message.get_created_at(),
                sender=UserRepository.get_by_id(message.get_sender_id()).get_username(),
                file="",
                is_read=MessageReadRepository.exists(message.get_id())
            ).to_data()
            for message in MessageRepository.get_messages_by_room_id(room_id=room.get_id())
        ]

        # DEBUG
        # print("ROOM CONTROLLER: ", messages)

        return HTTPResponse(
            body=JSONParser.stringify(messages)
        )
