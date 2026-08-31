from sqlalchemy import text

from src.database import get_engine
from src.repositories.user_repository import create_user


def main():
    email = "nishant-dev@loanwise.local"

    engine = get_engine()

    with engine.connect() as connection:
        existing_user = connection.execute(
            text(
                """
                SELECT id, name, email
                FROM users
                WHERE email = :email;
                """
            ),
            {"email": email},
        ).mappings().first()

    if existing_user:
        print("Development user already exists.")
        print(f"User ID: {existing_user['id']}")
        print(f"Name: {existing_user['name']}")
        print(f"Email: {existing_user['email']}")
        return

    user = create_user(
        name="Nishant",
        email=email,
    )

    print("Development user created successfully.")
    print(f"User ID: {user['id']}")
    print(f"Name: {user['name']}")
    print(f"Email: {user['email']}")


if __name__ == "__main__":
    main()