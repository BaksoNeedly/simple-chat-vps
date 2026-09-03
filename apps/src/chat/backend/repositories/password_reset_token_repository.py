from config import auth_tables

from simple_framework.database.database_manager import DatabaseManager
from ..models.password_reset_token import PasswordResetToken
from simple_framework.utils.time_utils import TimeUtils


class PasswordResetTokenRepository:
    """Database operations for password-reset tokens."""

    @staticmethod
    def create(
        user_id: int,
        token_hash: str,
        expires_at: int,
        created_at: int | None = None,
    ) -> None:
        if created_at is None:
            created_at = TimeUtils.get_current_time_stamp()

        DatabaseManager.execute(
            f"""
            INSERT INTO {auth_tables.PASSWORD_RESET_TOKENS}
                (user_id, token_hash, expires_at, created_at)
            VALUES (%s, %s, %s, %s)
            """,
            (user_id, token_hash, expires_at, created_at),
        )

    @staticmethod
    def get_by_id(token_id: int) -> PasswordResetToken | None:
        row = DatabaseManager.fetch_one(
            f"""
            SELECT id, user_id, token_hash, expires_at, used_at, created_at
            FROM {auth_tables.PASSWORD_RESET_TOKENS}
            WHERE id = %s
            """,
            (token_id,),
        )
        return PasswordResetTokenRepository._row_to_model(row)

    @staticmethod
    def get_by_token_hash(token_hash: str) -> PasswordResetToken | None:
        row = DatabaseManager.fetch_one(
            f"""
            SELECT id, user_id, token_hash, expires_at, used_at, created_at
            FROM {auth_tables.PASSWORD_RESET_TOKENS}
            WHERE token_hash = %s
            """,
            (token_hash,),
        )
        return PasswordResetTokenRepository._row_to_model(row)

    @staticmethod
    def get_by_user_id(user_id: int) -> list[PasswordResetToken]:
        rows = DatabaseManager.fetch_all(
            f"""
            SELECT id, user_id, token_hash, expires_at, used_at, created_at
            FROM {auth_tables.PASSWORD_RESET_TOKENS}
            WHERE user_id = %s
            ORDER BY created_at DESC
            """,
            (user_id,),
        )
        return [
            PasswordResetTokenRepository._row_to_model(row)
            for row in rows
        ]

    @staticmethod
    def get_valid_by_token_hash(
        token_hash: str,
        current_timestamp: int | None = None,
    ) -> PasswordResetToken | None:
        if current_timestamp is None:
            current_timestamp = TimeUtils.get_current_time_stamp()

        row = DatabaseManager.fetch_one(
            f"""
            SELECT id, user_id, token_hash, expires_at, used_at, created_at
            FROM {auth_tables.PASSWORD_RESET_TOKENS}
            WHERE token_hash = %s
              AND used_at IS NULL
              AND expires_at > %s
            """,
            (token_hash, current_timestamp),
        )
        return PasswordResetTokenRepository._row_to_model(row)

    @staticmethod
    def mark_as_used(token_id: int, used_at: int | None = None) -> None:
        if used_at is None:
            used_at = TimeUtils.get_current_time_stamp()

        DatabaseManager.execute(
            f"""
            UPDATE {auth_tables.PASSWORD_RESET_TOKENS}
            SET used_at = %s
            WHERE id = %s AND used_at IS NULL
            """,
            (used_at, token_id),
        )

    @staticmethod
    def delete_expired(current_timestamp: int | None = None) -> None:
        if current_timestamp is None:
            current_timestamp = TimeUtils.get_current_time_stamp()

        DatabaseManager.execute(
            f"""
            DELETE FROM {auth_tables.PASSWORD_RESET_TOKENS}
            WHERE expires_at <= %s
            """,
            (current_timestamp,),
        )

    @staticmethod
    def _row_to_model(row) -> PasswordResetToken | None:
        if row is None:
            return None

        return PasswordResetToken(
            token_id=row[0],
            user_id=row[1],
            token_hash=row[2],
            expires_at=row[3],
            used_at=row[4],
            created_at=row[5],
        )
