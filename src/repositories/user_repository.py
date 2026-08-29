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


def get_user_by_id(user_id: int):
    engine = get_engine()

    query = text("""
        SELECT id, name, email, created_at, updated_at
        FROM users
        WHERE id = :user_id;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"user_id": user_id},
        )

        return result.mappings().first()


def get_user_by_email(email: str):
    engine = get_engine()

    query = text("""
        SELECT id, name, email, created_at, updated_at
        FROM users
        WHERE email = :email;
    """)

    with engine.connect() as connection:
        result = connection.execute(
            query,
            {"email": email},
        )

        return result.mappings().first()


def update_user(user_id: int, name: str, email: str):
    engine = get_engine()

    query = text("""
        UPDATE users
        SET
            name = :name,
            email = :email,
            updated_at = CURRENT_TIMESTAMP
        WHERE id = :user_id
        RETURNING id, name, email, created_at, updated_at;
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {
                "user_id": user_id,
                "name": name,
                "email": email,
            },
        )

        return result.mappings().first()


def delete_user(user_id: int):
    engine = get_engine()

    query = text("""
        DELETE FROM users
        WHERE id = :user_id
        RETURNING id;
    """)

    with engine.begin() as connection:
        result = connection.execute(
            query,
            {"user_id": user_id},
        )

        return result.scalar()