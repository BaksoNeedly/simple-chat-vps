class RouteResolver:

    def __init__(self):
        self._routes = {}
        self._dynamic_handlers = {}

    def register(self, method: str, path: str, handler: callable) -> None:
        self._routes[(method.upper(), path)] = handler

    # def register_dynamic(self, route_key: str, handler: callable) -> None:
    #     self._dynamic_handlers[route_key] = handler

    def resolve(self, method: str, path: str) -> callable|None:
        handler = self._routes.get((method.upper(), path))
        if handler:
            return handler
        
        # dynamic_route = RouteRepository.get_by_path(path)
        # if not dynamic_route:
        #     return None

        # return self._dynamic_handlers.get(dynamic_route.get_route_key())
