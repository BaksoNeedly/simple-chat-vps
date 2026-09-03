class WebSocketRouteRegistry:
    
    def __init__(self):
        self._handlers: dict[str, callable] = {}
        
    def register(self, id: str, handler: callable) -> None:
        self._handlers[id.strip().lower()] = handler
        
    def get(self, id: str) -> callable | None:
        return self._handlers.get(id)
