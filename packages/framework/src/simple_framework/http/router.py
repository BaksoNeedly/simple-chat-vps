from .request import HTTPRequest
from .response import HTTPResponse

class HTTPRouter:

    def __init__(self):
        self._routes = {}
        self._dynamic_handlers = {}


    def get(self, path: str, handler: callable):
        self.register("GET", path, handler)

    def post(self, path: str, handler: callable):
        self.register("POST", path, handler)

    def route(self, request: HTTPRequest) -> HTTPResponse | None:
        method = request.get_method()
        path = request.get_url().get_path()

        handler = self.resolve(method, path)
        if not handler:
            return None

        return handler(request)
    
    def register(self, method: str, path: str, handler: callable) -> None:
        self._routes[(method.upper(), path)] = handler

    def resolve(self, method: str, path: str) -> callable|None:
        handler = self._routes.get((method.upper(), path))
        if handler:
            return handler
