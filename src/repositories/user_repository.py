from sqlalchemy import text

from src.database import get_engine


def create_user(name: str, email: str):
    engine = get_engine()

    query = text("""
        INSERT INTO users (name, email)
        VALUES (:name, :email)
        RETURNING id, name, email, created_at, updated_at;
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "name": name,
                "email": email,
            },
        )

        return result.mappings().one()