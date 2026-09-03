from simple_framework.session.client_session import ClientSession
from simple_framework.session.session import Session
from simple_framework.websocket.broadcaster import WebSocketBroadcaster
from simple_framework.websocket.router import WebSocketRouter
from simple_framework.websocket.server import WebSocketServer
from simple_framework.session.client_session_manager import ClientSessionManager
from simple_framework.utils.time_utils import TimeUtils

from ..models.message import Message
from ..models.room import Room
from ..packets.websocket.join_message_packet import JoinMessagePacket
from ..packets.websocket.leave_room_packet import LeaveRoomPacket
from ..packets.websocket.message_packet import MessagePacket
from ..packets.websocket.total_user_packet import TotalUserPacket
from ..packets.websocket.update_status_packet import UpdateStatusPacket
from ..packets.websocket.user_enter_room_packet import UserEnterRoomPacket
from ..repositories.message_read_repository import MessageReadRepository
from ..repositories.message_repository import MessageRepository
from ..repositories.room_repository import RoomRepository
from ..repositories.user_repository import UserRepository


class WebSocketRouteRegistrar:
    def __init__(self, websocket_server: WebSocketServer):
        self._websocket_server = websocket_server
        self._router = websocket_server.get_router()

    def register(self) -> None:
        self.register_routes()
        self.register_access_hooks()

    def register_routes(self) -> None:
        self._router.register("join", self.handle_join)
        self._router.register("enter_room", self.handle_enter_room)
        self._router.register("leave_room", self.handle_leave_room)
        self._router.register("global_join", self.handle_global_join)
        self._router.register("ping", self.handle_global_join)
        self._router.register("join_message", self.handle_join_message)
        self._router.register("message", self.handle_message)

    def register_access_hooks(self) -> None:
        self._websocket_server.add_access_hook(self.access_hook)

    @staticmethod
    def access_hook(session: Session | None) -> bool:
        return session is not None and session.is_authenticated()

    def handle_join(self, client_session: ClientSession, payload: dict) -> None:
        # Reserved for the initial WebSocket join event.
        pass

    def handle_enter_room(self, client_session: ClientSession, payload: dict) -> None:
        target_username = payload.get("target_username")
        target_user = UserRepository.get_by_username(target_username)

        if not target_user:
            return

        calculated_id = RoomRepository.calculate(
            client_session.get_username(),
            target_username
        )
        room = RoomRepository.get_by_id(calculated_id)

        if not room:
            room = Room(calculated_id)
            RoomRepository.create(
                room,
                [client_session.get_username(), target_username]
            )

        if (
            not client_session.get_current_room_id()
            or client_session.get_current_room_id() != room.get_id()
        ):
            client_session.set_current_room_id(room.get_id())
            WebSocketBroadcaster.send_to_all(
                UserEnterRoomPacket(target_username),
                [client_session.get_username()]
            )

        for message in MessageRepository.get_messages_by_sender_id(
            str(target_user.get_id())
        ):
            MessageReadRepository.mark_as_read(
                message.get_id(),
                TimeUtils.get_current_time_stamp()
            )

    def handle_leave_room(self, client_session: ClientSession, payload: dict) -> None:
        current_room_id = client_session.get_current_room_id()
        if not current_room_id:
            return

        client_session.set_current_room_id(None)
        WebSocketBroadcaster.send(
            client_session.get_socket(),
            LeaveRoomPacket(client_session.get_username())
        )

    def handle_global_join(self, client_session: ClientSession, payload: dict) -> None:
        WebSocketBroadcaster.send_to_all(
            UpdateStatusPacket(client_session.get_username())
        )
        WebSocketBroadcaster.send_to_all(
            TotalUserPacket(len(ClientSessionManager.get_all()))
        )

    def handle_join_message(self, client_session: ClientSession, payload: dict) -> None:
        current_room_id = client_session.get_current_room_id()
        if not current_room_id:
            return

        room = RoomRepository.get_by_id(current_room_id)
        if not room:
            return

        packet = JoinMessagePacket(client_session.get_username())
        for member in room.get_online_members():
            if member.get_current_room_id() != room.get_id():
                continue

            if member.get_username() == client_session.get_username():
                continue

            WebSocketBroadcaster.send(member.get_socket(), packet)

    def handle_message(self, client_session: ClientSession, payload: dict) -> None:
        content = payload.get("content")
        created_at = payload.get("timestamp")
        file = payload.get("file")

        if content is None or created_at is None:
            return

        current_room_id = client_session.get_current_room_id()
        if not current_room_id:
            return

        room = RoomRepository.get_by_id(current_room_id)
        if not room:
            return

        message = Message(
            room_id=room.get_id(),
            content=content,
            created_at=created_at,
            sender_id=client_session.get_serial_id()
        )
        message = MessageRepository.add_message(message)

        packet = MessagePacket(
            content,
            created_at,
            client_session.get_username(),
            file,
            MessageReadRepository.exists(message.get_id())
        )

        for member in room.get_online_members():
            if (
                member.get_current_room_id() == room.get_id()
                and member.get_serial_id() != client_session.get_serial_id()
            ):
                MessageReadRepository.mark_as_read(
                    message.get_id(),
                    TimeUtils.get_current_time_stamp()
                )
                packet.read()

            if (
                member.get_current_room_id()
                != RoomRepository.calculate(
                    member.get_username(),
                    member.get_username()
                )
            ):
                WebSocketBroadcaster.send(member.get_socket(), packet)
