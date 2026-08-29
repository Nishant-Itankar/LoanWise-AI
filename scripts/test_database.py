from sqlalchemy import text
from src.database import get_engine

def main():
     engine = get_engine()
     
     with engine.connect() as connection:
          result = connection.execute(text("SELECT version();"))
          version = result.scalar()
     
     print("Database connection successful.")
     print(version)
     
if __name__ == "__main__":
     main()