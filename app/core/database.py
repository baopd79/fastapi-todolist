from collections.abc import Generator
from sqlmodel import Session, SQLModel, create_engine

from app.core.config import settings

# Naming convention for constraints
# Why: ensures consistent, predictable constraint names across migrations.
# Without this, Alembic generates random names which break on schema changes.
NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}

SQLModel.metadata.naming_convention = NAMING_CONVENTION

# Engine: connection pool, persist suốt lifecycle của app
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
)


def get_db() -> Generator[Session, None, None]:
    """FastAPI dependency để inject DB session vào endpoint."""
    with Session(engine) as session:
        yield session
