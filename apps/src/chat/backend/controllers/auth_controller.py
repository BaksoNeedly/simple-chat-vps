from urllib.parse import quote
import bcrypt

from simple_framework.http.request import HTTPRequest
from simple_framework.http.response import HTTPResponse

from ..controllers.asset_controller import AssetController
from ..packets.http.reset_password_packet import ResetPasswordPacket
from ..repositories.user_repository import UserRepository
from simple_framework.session.client_session_manager import ClientSessionManager
from simple_framework.utils.json_parser import JSONParser
from ..packets.register_packet import RegisterPacket
from ..packets.login_packet import LoginPacket
from simple_framework.session.session_manager import SessionManager
from simple_framework.utils.time_utils import TimeUtils
from config import app_config
from ..repositories.password_reset_token_repository import PasswordResetTokenRepository

class AuthController:
    
    @staticmethod
    def logout(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        
        print("lewat")
        
        if not session:
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/login"
                }
            )
        
        client_session = ClientSessionManager.get(session.get_session_id())
        if not client_session:
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/login"
                }
            )
        
        ClientSessionManager.close(client_session)
        session.reset()
        return HTTPResponse(
            status="302",
            headers={
                "Location": "/page/login"
            }
        )
    
    @staticmethod
    def redirect_to_reset_password(request: HTTPRequest) -> HTTPResponse:
        query = request.get_url().get_query()
        if not query:
            return HTTPResponse()

        token = query.get("token")
        if not token:
            return HTTPResponse()

        db_token = PasswordResetTokenRepository.get_by_token_hash(token)
        if not db_token:
            return HTTPResponse()
        
        # if db_token.is_valid(TimeUtils.get_current_time_stamp()):
        #     return HTTPResponse()
        
        return HTTPResponse(
            status="302",
            headers={
                "Location": f"/page/reset-password?token={quote(token)}"
            }
        )

    @staticmethod
    def reset_password(request: HTTPRequest) -> HTTPResponse:
        packet = ResetPasswordPacket.from_data(
            JSONParser.parse(
                request.get_body()
            )
        )
        
        password = str(packet.get_password())
        confirm_password = str(packet.get_confirm_password())
        token = str(packet.get_token())
        
        if password != confirm_password:
            return HTTPResponse(
                status="422",
                reason_phrase="Unprocessable Content"
            )
            
        token_model = PasswordResetTokenRepository.get_by_token_hash(token)
        if not token_model or token_model.is_used() or token_model.is_expired(TimeUtils.get_current_time_stamp()):
            return HTTPResponse(
                status="422",
                reason_phrase="Unprocessable Content"
            )
            
        token_user_id = token_model.get_user_id()
        user = UserRepository.get_by_id(token_user_id)
        
        if not user:
            return HTTPResponse(
                status="422",
                reason_phrase="Unprocessable Content"
            )
            
        hash_password = bcrypt.hashpw(
            password.encode(app_config.ENCODING),
            bcrypt.gensalt()
        ).decode(app_config.ENCODING)
            
        UserRepository.update_password(
            user.get_id(), 
            hash_password
        )
        PasswordResetTokenRepository.mark_as_used(token_model.get_id())
        
        return HTTPResponse()
        

    @staticmethod
    def register(request: HTTPRequest) -> HTTPResponse:
        register_packet = RegisterPacket.from_data(request.get_body())
        if not register_packet:
            return HTTPResponse(
                status="400",
                reason_phrase="Bad Request",
            )

        username = register_packet.get_username().strip()
        email = register_packet.get_email().strip()
        password = register_packet.get_password()
        confirm_password = register_packet.get_confirm_password()

        if not username or not email or not password:
            return HTTPResponse(
                status="422",
                reason_phrase="Unprocessable Content",
            )

        if password != confirm_password:
            return HTTPResponse(
                status="422",
                reason_phrase="Unprocessable Content",
            )

        if UserRepository.get_by_username(username):
            return HTTPResponse(
                status="409",
                reason_phrase="Conflict",
            )

        hash_password = bcrypt.hashpw(
            password.encode(app_config.ENCODING),
            bcrypt.gensalt(),
        ).decode(app_config.ENCODING)

        UserRepository.create(username, email, hash_password)

        return AssetController.serve_response("registration-success.html")

    @staticmethod
    def login(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        if not session:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized",
            )
        
        if session.is_authenticated():
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/chat"
                }
            )
        login_packet = LoginPacket.from_data(request.get_body())
        if not login_packet:
            return HTTPResponse(
                status="400",
                reason_phrase="Bad Request",
            )

        username = login_packet.get_username().strip()
        password = login_packet.get_password()
        user = UserRepository.get_by_username(username)

        if not user or not user.get_hash_password():
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized",
            )

        is_password_valid = bcrypt.checkpw(
            password.encode(app_config.ENCODING),
            user.get_hash_password().encode(app_config.ENCODING),
        )
        if not is_password_valid:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized",
            )        

        session.set_username(user.get_username())
        session.set_email(user.get_email())
        session.authenticate()

        return HTTPResponse(
            status="302",
            reason_phrase="Found",
            headers={
                "Location": "/page/chat"
            }
        )
