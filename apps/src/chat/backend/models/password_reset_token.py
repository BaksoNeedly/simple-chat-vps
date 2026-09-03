class PasswordResetToken:
    """Domain model for a password-reset token record."""

    def __init__(
        self,
        token_id: int,
        user_id: int,
        token_hash: str,
        expires_at: int,
        used_at: int | None,
        created_at: int,
    ):
        self._id = token_id
        self._user_id = user_id
        self._token_hash = token_hash
        self._expires_at = expires_at
        self._used_at = used_at
        self._created_at = created_at

    def get_id(self) -> int:
        return self._id

    def get_user_id(self) -> int:
        return self._user_id

    def get_token_hash(self) -> str:
        return self._token_hash

    def get_expires_at(self) -> int:
        return self._expires_at

    def get_used_at(self) -> int | None:
        return self._used_at

    def get_created_at(self) -> int:
        return self._created_at

    def is_used(self) -> bool:
        return self._used_at is not None

    def is_expired(self, current_timestamp: int) -> bool:
        return current_timestamp >= self._expires_at

    def is_valid(self, current_timestamp: int) -> bool:
        return not self.is_used() and not self.is_expired(current_timestamp)

    def to_data(self) -> dict:
        return {
            "id": self._id,
            "user_id": self._user_id,
            "token_hash": self._token_hash,
            "expires_at": self._expires_at,
            "used_at": self._used_at,
            "created_at": self._created_at,
        }
