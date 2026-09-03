from simple_framework.http.response import HTTPResponse
from simple_framework.http.request import HTTPRequest
from simple_framework.services.email_service import EmailService
from simple_framework.utils.json_parser import JSONParser
from simple_framework.session.session_manager import SessionManager
from simple_framework.cookie.cookie import Cookie

from simple_framework.session.client_session import ClientSession
from simple_framework.session.client_session_manager import ClientSessionManager

from ..packets.http.new_chat_packet import NewChatPacket
from ..packets.http.new_contact_packet import NewContactPacket
from ..packets.http.user_packet import UserPacket

from ..repositories.user_repository import UserRepository
from ..repositories.contact_repository import ContactRepository
from ..repositories.room_repository import RoomRepository

from ..models.room import Room

from config import app_config


from simple_framework.database.database_manager import DatabaseManager

from simple_framework.http.multipart import Multipart


import random

from ..packets.verification_code_packet import VerificationCodePacket


class UserController:
    
    @staticmethod
    def load_users(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        
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
            
        users = []
        for k, v in ClientSessionManager.get_all().items():
            users.append({
                "username": v.get_username()
            })
            
        print(users)
        return HTTPResponse(body=JSONParser.stringify(users))
    
    @staticmethod
    def delete_account(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        
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
        
        UserRepository.delete(client_session.get_serial_id())
        ClientSessionManager.close(client_session)
        SessionManager.remove(session.get_session_id())

        return HTTPResponse(
            status="302",
            headers={
                "Location": "/page/account-deleted"
            }
        )

    @staticmethod
    def redirect_to_chat(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)

        if not session or not session.is_authenticated():
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/login"
                }
            )

        return HTTPResponse(
            status="302",
            headers={
                "Location": "/page/chat"
            }
        )
        

    @staticmethod
    def verify_code(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)

        packet = VerificationCodePacket.from_data(JSONParser.parse(request.get_body()))
        
        if not session:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized"
            )

        session_id = session.get_session_id()
        client_session = ClientSessionManager.get(session_id)

        if not client_session:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized"
            )

        user = UserRepository.get_by_id(client_session.get_serial_id())

        if not user:
            return HTTPResponse(
                status="403",
                reason_phrase="Forbidden"
            )

        insert_code = str(packet.get_code())
        user_code = str(user.get_verify_code())
        

        if insert_code != user_code:
            return HTTPResponse(
                status="400",
                reason_phrase="Bad Request"
            )
            
        UserRepository.mark_as_verified(user.get_id())
        return HTTPResponse(
            status="302",
            headers={
                "Location": "/page/verified"
            }
        )

    @staticmethod
    def start_verification(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)

        if not session:
            return HTTPResponse(
                status="302",
                reason_phrase="Unauthorized",
                headers={
                    "Location": "/page/login"
                }
            )

        session_id = session.get_session_id()
        client_session = ClientSessionManager.get(session_id)

        if not client_session:
            return HTTPResponse(
                status="302",
                reason_phrase="Unauthorized",
                headers={
                    "Location": "/page/login"
                }
            )

        user = UserRepository.get_by_id(client_session.get_serial_id())

        if not user:
            return HTTPResponse(
                status="403",
                reason_phrase="Forbidden"
            )

        verify_code = user.get_verify_code()

        if user.is_verified():
            print("ini")
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/verified"
                }
            )
        
        if not verify_code:
            verify_code = str(random.randint(100000, 999999))
            UserRepository.update_verify_code(user.get_id(), verify_code)

        message = f"""Hello {user.get_username()},

We received a request to verify your email address for Simple Chat.

Your verification code is:

{verify_code}

Enter this 6-digit code on the verification page to verify your email.

If you did not request this verification, you can safely ignore this email.

Regards,
Simple Chat Team
"""

        EmailService.send(
            user.get_email(),
            "Verify Email",
            message
        )

        return HTTPResponse(
            status="302",
            headers={
                "Location": "/page/verification"
            }
        )

    @staticmethod
    def new_contact(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        
        if not session:
            return HTTPResponse(
                status="302",
                reason_phrase="Unauthorized",
                headers={
                    "Location": "/page/login"
                }
            )
        
        session_id = session.get_session_id()
        client_session = ClientSessionManager.get(session_id)
        
        if not client_session:
            return HTTPResponse(
                status="302",
                reason_phrase="Unauthorized",
                headers={
                    "Location": "/page/login"
                }
            )

        packet = NewContactPacket.from_data(JSONParser.parse(request.get_body()))

        target_user = UserRepository.get_by_username(packet.get_username())
        if target_user:
            if not ContactRepository.exists(client_session.get_serial_id(), target_user.get_id()):
                UserRepository.add_contact_to(
                    client_session.get_serial_id(),
                    target_user
                )
                calculated_id = RoomRepository.calculate(client_session.get_username(), target_user.get_username())
                room = RoomRepository.get_by_id(calculated_id)
                if not room:
                    RoomRepository.create(
                        Room(calculated_id),
                        [client_session.get_username(), target_user.get_username()]
                    )
            
            return HTTPResponse()
        else:
            return HTTPResponse(
                status="404",
                reason_phrase="Not Found"
            )

    @staticmethod
    def check_online_user(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)
        if not session or not session.is_authenticated():
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized"
            )

        session_id = session.get_session_id()
        client_session = ClientSessionManager.get(session_id)
        if not client_session:
            return HTTPResponse(
                status="404",
                reason_phrase="Not Found"
            )

        packet = NewChatPacket.from_data(JSONParser.parse(request.get_body()))

        target_user = ClientSessionManager.get_by_name(packet.get_username())

        if(target_user):
            status = "200"
            reason_phrase = "OK"
        else:
            status = "404"
            reason_phrase = "Not Found"

        return HTTPResponse(status=status, reason_phrase=reason_phrase)

    @staticmethod
    def load_contacts(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)

        if not session:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized"
            )

        client_session = ClientSessionManager.get(session.get_session_id())

        if not client_session:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized"
            )

        client_session_id = client_session.get_serial_id()

        contacts = ContactRepository.get_by_user_id(client_session_id)

        usernames = []
        for contact in contacts:

            contact_user = UserRepository.get_by_id(contact.get_contact_id())

            if contact_user:
                usernames.append(contact_user.get_username())

        return HTTPResponse(
            body=JSONParser.stringify(usernames)
        )

    @staticmethod
    def load_user_profile(request: HTTPRequest) -> HTTPResponse:
        session = SessionManager.extract_session(request)

        if not session or not session.is_authenticated():
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/login"
                },
            )

        client_session = ClientSessionManager.get(session.get_session_id())
        if not client_session:
            return HTTPResponse(
                status="401",
                reason_phrase="Unauthorized"
            )

        client_session_id = client_session.get_serial_id()
        user = UserRepository.get_by_id(client_session_id)
        if not user:
            return HTTPResponse(
                status="302",
                headers={
                    "Location": "/page/login"
                },
            )
        user_data = JSONParser.stringify(user.to_data())
        return HTTPResponse(
            headers={
                "Content-Length": len(user_data.encode(app_config.ENCODING)),
                "Content-Type": "application/json"
            },
            body=user_data
        )
