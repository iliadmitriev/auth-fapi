from typing import Any

from sqlalchemy.ext.declarative import as_declarative, declared_attr


@as_declarative()
class Base:
    id: Any
    __name__: str

    # Generate table name automatically
    @declared_attr
    def __tablename__(cls) -> str: # noqa
        return cls.__name__.lower()
