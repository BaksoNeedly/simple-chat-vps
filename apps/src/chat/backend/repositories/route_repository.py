from ..database.database_manager import DatabaseManager
from ..models.dynamic_route import DynamicRoute
from ..utils.time_utils import TimeUtils
from config import framework_tables


class RouteRepository:
    """Database operations for framework_routes."""

    @staticmethod
    def create(
        path: str,
        route_key: str,
        created_at: int | None = None,
    ) -> None:
        if created_at is None:
            created_at = TimeUtils.get_current_time_stamp()

        DatabaseManager.execute(
            f"""
            INSERT INTO {framework_tables.ROUTES}
                (path, route_key, created_at)
            VALUES (%s, %s, %s)
            """,
            (path, route_key, created_at),
        )

    @staticmethod
    def get_by_id(route_id: int) -> DynamicRoute | None:
        row = DatabaseManager.fetch_one(
            f"""
            SELECT id, path, route_key, created_at
            FROM {framework_tables.ROUTES}
            WHERE id = %s
            """,
            (route_id,),
        )
        return RouteRepository._row_to_dynamic_route(row)

    @staticmethod
    def get_by_path(path: str) -> DynamicRoute | None:
        row = DatabaseManager.fetch_one(
            f"""
            SELECT id, path, route_key, created_at
            FROM {framework_tables.ROUTES}
            WHERE path = %s
            ORDER BY id
            LIMIT 1
            """,
            (path,),
        )
        return RouteRepository._row_to_dynamic_route(row)

    @staticmethod
    def get_by_route_key(route_key: str) -> list[DynamicRoute]:
        rows = DatabaseManager.fetch_all(
            f"""
            SELECT id, path, route_key, created_at
            FROM {framework_tables.ROUTES}
            WHERE route_key = %s
            ORDER BY id
            """,
            (route_key,),
        )
        return [
            RouteRepository._row_to_dynamic_route(row)
            for row in rows
        ]

    @staticmethod
    def get_all() -> list[DynamicRoute]:
        rows = DatabaseManager.fetch_all(
            f"""
            SELECT id, path, route_key, created_at
            FROM {framework_tables.ROUTES}
            ORDER BY id
            """
        )
        return [
            RouteRepository._row_to_dynamic_route(row)
            for row in rows
        ]

    @staticmethod
    def delete(route_id: int) -> None:
        DatabaseManager.execute(
            f"""
            DELETE FROM {framework_tables.ROUTES}
            WHERE id = %s
            """,
            (route_id,),
        )

    @staticmethod
    def _row_to_dynamic_route(row) -> DynamicRoute | None:
        if row is None:
            return None

        return DynamicRoute(
            route_id=row[0],
            path=row[1],
            route_key=row[2],
            created_at=row[3],
        )
