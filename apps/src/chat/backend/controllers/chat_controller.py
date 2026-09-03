from ..controllers.asset_controller import AssetController

from simple_framework.http.request import HTTPRequest
from simple_framework.http.response import HTTPResponse
from simple_framework.session.session_manager import SessionManager
from simple_framework.session.client_session_manager import ClientSessionManager as UserManager
from ..packets.http.search_user_packet import SearchUserPacket
from simple_framework.utils.json_parser import JSONParser

class ChatController:
    
    @staticmethod
    def serve_chat_page(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        if not session or not session.is_authenticated():
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/login"
                }
            )
        return AssetController.serve_response("chat.html")

    @staticmethod
    def search_online_user(request: HTTPRequest) -> HTTPResponse:
        packet = SearchUserPacket.from_data(JSONParser.parse(request.get_body()))
        target_username = packet.get_username()
        target_user = UserManager.get_by_name(target_username)
        if target_user:
            status = "200"
            reason_phrase = "OK"
        else:
            status = "404"
            reason_phrase = "Not Found"
        return HTTPResponse(status=status, reason_phrase=reason_phrase)
