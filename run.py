from chat.backend.http.router_registrar import HttpRouterRegistrar
from simple_framework.http.server import HTTPServer
from simple_framework.database.database_manager import DatabaseManager
from chat.backend.database.database_registrar import DatabaseRegistrar
from chat.backend.repositories.password_reset_token_repository import PasswordResetTokenRepository
from chat.backend.websocket.route_registrar import WebSocketRouteRegistrar
from simple_framework.utils.time_utils import TimeUtils

DatabaseManager.connect()
DatabaseRegistrar.register()

http_server = HTTPServer()

http_server.get_lifecycle().add_startup_hook(lambda: PasswordResetTokenRepository.delete_expired(TimeUtils.get_current_time_stamp()))
http_server.get_lifecycle().add_startup_hook(lambda: HttpRouterRegistrar(http_server.get_router()).register_routes())
http_server.get_lifecycle().add_startup_hook(
    lambda: WebSocketRouteRegistrar(
        http_server.get_websocket_server()
    ).register()
)
http_server.start()
