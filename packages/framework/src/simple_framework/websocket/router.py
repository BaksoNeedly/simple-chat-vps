from ..utils.json_parser import JSONParser
from .frame import WebSocketFrame
from ..session.client_session import ClientSession
from .router_registry import WebSocketRouteRegistry


class WebSocketRouter:

    def __init__(self):
        self._handlers: dict[str, callable] = {}
            
    def register(self, id: str, handler: callable) -> None:
        self._handlers[id.strip().lower()] = handler
        
    def get(self, id: str) -> callable | None:
        return self._handlers.get(id)

    def route(self, frame: bytes, client_session: ClientSession) -> None:
        raw_payload = WebSocketFrame.parse(frame)
        payload = JSONParser.parse(raw_payload)
        message_type = str(payload.get("type", "")).strip().lower()

        if not message_type:
            return

        handler = self.get(message_type)
        if handler is not None:
            handler(client_session, payload)
