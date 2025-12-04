from typing import Any, Generic, List, Tuple, TypeVar

from Flight_Project.repositories.RepositoryManager import RepositoryManager


T = TypeVar("T")


class BaseRepository(Generic[T]):
    def __init__(self, db: RepositoryManager, table_name: str):
        self.db = db
        self.table_name = table_name

    def _to_entity(self, row: Tuple) -> T:
        pass

    def _to_tuple(self, entity: T) -> Tuple[Any, ...]:
        pass

    def _get_insert_columns(self) -> List[str]:
        pass

    def fetch_all(self) -> List[T]:
        cursor = self.db.query(f"Select * from {self.table_name}")
        rows = cursor.fetchall()
        return [self._to_entity(row) for row in rows]

    def fetch_one(self, id: int) -> T:
        cursor = self.db.query(
            f"Select * from {self.table_name} WHERE id = ?",
            (id,),
        )
        row = cursor.fetchone()
        return self._to_entity(row) if row else None

    def save(self, entity: T) -> T:
        columns = self._get_insert_columns()
        placeholders = ", ".join(["?"] * len(columns))
        columns_str = ", ".join(columns)

        cursor = self.db.execute(
            f"INSERT INTO {self.table_name}({columns_str}) VALUES ({placeholders})",
            self._to_tuple(entity),
        )

        new_id = cursor.lastrowid

        if new_id is not None:
            entity.id = new_id

        return entity

    def update(self, entity: T) -> None:
        columns = self._get_insert_columns()
        set_clause = ", ".join([f"{col} = ?" for col in columns])

        self.db.execute(
            f"UPDATE {self.table_name} SET {set_clause} WHERE id = ?",
            (*self._to_tuple(entity), entity.id),
        )

    def delete(self, id: int) -> None:
        self.db.execute(f"DELETE FROM {self.table_name} WHERE id = ?", (id,))
