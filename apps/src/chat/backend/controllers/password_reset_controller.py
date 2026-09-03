from urllib.parse import quote
import secrets

from simple_framework.http.request import HTTPRequest
from simple_framework.http.response import HTTPResponse
from ..packets.http.request_reset_password_packet import RequestResetPasswordPacket
from ..repositories.password_reset_token_repository import PasswordResetTokenRepository
from ..repositories.user_repository import UserRepository
from simple_framework.services.email_service import EmailService
from simple_framework.utils.json_parser import JSONParser
from simple_framework.utils.time_utils import TimeUtils


class PasswordResetController:
    
    @staticmethod
    def request_reset(request: HTTPRequest) -> HTTPResponse:
        packet = RequestResetPasswordPacket.from_data(
            JSONParser.parse(
                request.get_body()
            )
        )
                
        user = UserRepository.get_by_username(
            packet.get_username()
        )
        
        if not user:
            return HTTPResponse()
        
        if user.get_email() != packet.get_email():
            return HTTPResponse()
        
        db_tokens = PasswordResetTokenRepository.get_by_user_id(user.get_id())
        for db_token in db_tokens:
            if db_token.is_valid(TimeUtils.get_current_time_stamp()):
                return HTTPResponse()
        
        token = secrets.token_urlsafe(32)
        
        PasswordResetTokenRepository.create(
            user.get_id(),
            token,
            TimeUtils.get_timestamp_after_minutes(10),
            TimeUtils.get_current_time_stamp()
        )
        
        reset_url = (
            "http://192.168.100.100:8080/reset/password/check"
            f"?token={quote(token)}"
        )

        message = f"""Hello {user.get_username()},

        We received a request to reset your password.

        Click the link below to create a new password:

        {reset_url}

        This link will expire in 10 minutes.

        If you did not request a password reset, you can safely ignore this email.

        Regards,
        Simple Chat Team
        """

        send_mail = EmailService().send(
            user.get_email(),
            "Reset Password",
            message
        )

        if not send_mail:
            return HTTPResponse(
                status="500",
                reason_phrase="Internal Server Error"
            )
        
        return HTTPResponse()
