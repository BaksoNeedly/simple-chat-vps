from simple_framework.database.database_manager import DatabaseManager

from config import auth_tables, chat_tables, framework_tables


class DatabaseRegistrar:
    @staticmethod
    def register() -> None:
        DatabaseRegistrar._register_users()
        DatabaseRegistrar._register_chat_tables()
        DatabaseRegistrar._register_framework_tables()
        DatabaseRegistrar._register_password_reset_tokens()

    @staticmethod
    def _register_users() -> None:
        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {auth_tables.USERS}(
                id SERIAL PRIMARY KEY,
                username TEXT,
                email TEXT,
                hash_password TEXT,
                is_verified BOOLEAN,
                verify_code VARCHAR(6),
                contacts TEXT
            )
        """)

    @staticmethod
    def _register_chat_tables() -> None:
        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {chat_tables.ROOMS}(
                id SERIAL PRIMARY KEY,
                room_id TEXT
            )
        """)

        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {chat_tables.ROOM_MEMBERS} (
                id SERIAL PRIMARY KEY,
                room_id INTEGER NOT NULL
                    REFERENCES {chat_tables.ROOMS}(id) ON DELETE CASCADE,
                member_id INTEGER NOT NULL
                    REFERENCES {auth_tables.USERS}(id) ON DELETE CASCADE
            )
        """)

        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {chat_tables.MESSAGES} (
                id SERIAL PRIMARY KEY,
                room_id TEXT,
                sender_id TEXT,
                message TEXT,
                created_at TEXT,
                is_read BOOLEAN DEFAULT FALSE
            )
        """)

        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {chat_tables.MESSAGE_READS} (
                message_id INTEGER PRIMARY KEY
                    REFERENCES {chat_tables.MESSAGES}(id) ON DELETE CASCADE,
                read_at BIGINT
            )
        """)

        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {chat_tables.USER_CONTACTS} (
                id SERIAL PRIMARY KEY,
                user_id INTEGER
                    REFERENCES {auth_tables.USERS}(id) ON DELETE CASCADE,
                contact_id INTEGER
                    REFERENCES {auth_tables.USERS}(id) ON DELETE CASCADE,
                created_at BIGINT,
                UNIQUE (user_id, contact_id)
            )
        """)

    @staticmethod
    def _register_framework_tables() -> None:
        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {framework_tables.ROUTES} (
                id SERIAL PRIMARY KEY,
                path TEXT,
                route_key TEXT,
                created_at BIGINT
            )
        """)

    @staticmethod
    def _register_password_reset_tokens() -> None:
        DatabaseManager.execute(f"""
            CREATE TABLE IF NOT EXISTS {auth_tables.PASSWORD_RESET_TOKENS} (
                id SERIAL PRIMARY KEY,
                user_id INTEGER NOT NULL
                    REFERENCES {auth_tables.USERS}(id) ON DELETE CASCADE,
                token_hash TEXT NOT NULL UNIQUE,
                expires_at BIGINT NOT NULL,
                used_at BIGINT,
                created_at BIGINT NOT NULL
            )
        """)
