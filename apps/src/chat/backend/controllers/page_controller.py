from simple_framework.cookie.cookie import Cookie
from simple_framework.http.request import HTTPRequest
from simple_framework.http.response import HTTPResponse
from simple_framework.session.session import Session
from simple_framework.session.session_manager import SessionManager
from config import app_config
from .asset_controller import AssetController

class PageController:

    @staticmethod
    def serve_login_page(request: HTTPRequest) -> HTTPResponse:
        cookie = request.get_headers().get("cookie")
        session_id = None
        if cookie:
            session_id = Cookie.parse(
                str(cookie).encode(app_config.ENCODING)
            ).get("session_id")

        set_cookie = None
        session = SessionManager.get(session_id) if session_id else None

        if not session:
            if session_id:
                print("Has cookie but session was not found.")
            else:
                print("Do not have session yet.")

            # SessionManager stores sessions in memory, so a server restart
            # makes an existing browser cookie invalid.
            session_id = SessionManager.generate_id()
            set_cookie = Cookie.build({"session_id": session_id})

            session = Session(session_id)
            SessionManager.set(session_id, session)

        if session.is_authenticated():
            return HTTPResponse(
                status="302",
                headers={"Location": "/page/chat"}
            )

        response = AssetController.serve_response("login.html")
        if set_cookie:
            response.add_headers("Set-Cookie", set_cookie)
        return response

    @staticmethod
    def serve_register_page(request: HTTPRequest) -> HTTPResponse:
        return AssetController.serve_response("register.html")
