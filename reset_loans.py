from sqlalchemy import text
from src.database import get_engine

engine = get_engine()

with engine.begin() as connection:
    connection.execute(text("DELETE FROM interest_rate_history"))
    connection.execute(text("DELETE FROM loans"))

print("LOANS_RESET_OK")