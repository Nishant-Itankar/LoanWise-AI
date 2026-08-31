import re

from src.repositories.user_repository import get_all_users


from src.repositories.user_repository import (
    create_user,
    get_user_by_email,
    get_user_by_id,
    update_user,
)


EMAIL_PATTERN = re.compile(
    r"^[^@\s]+@[^@\s]+\.[^@\s]+$"
)

def list_users() -> list[dict]:
    return get_all_users() 

def validate_user(name: str, email: str):
    name = name.strip()
    email = email.strip().lower()

    if not name:
        raise ValueError("Name cannot be empty.")

    if len(name) > 100:
        raise ValueError("Name cannot exceed 100 characters.")

    if not EMAIL_PATTERN.match(email):
        raise ValueError("Invalid email address.")

    return name, email


def register_user(name: str, email: str):
    name, email = validate_user(name, email)

    existing_user = get_user_by_email(email)

    if existing_user:
        raise ValueError("A user with this email already exists.")

    return create_user(
        name=name,
        email=email,
    )


def get_user(user_id: int):
    if user_id <= 0:
        raise ValueError("User ID must be positive.")

    return get_user_by_id(user_id)


def update_user_profile(
    user_id: int,
    name: str,
    email: str,
):
    if user_id <= 0:
        raise ValueError("User ID must be positive.")

    name, email = validate_user(name, email)

    existing_user = get_user_by_email(email)

    if existing_user and existing_user["id"] != user_id:
        raise ValueError(
            "Another user already uses this email."
        )

    return update_user(
        user_id=user_id,
        name=name,
        email=email,
    )