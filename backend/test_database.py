from sqlalchemy import text

from app.database import engine


print("Starting MediLens database connection test...")


try:
    with engine.connect() as connection:
        result = connection.execute(
            text("SELECT 1")
        )

        value = result.scalar()

        print("\nDatabase connection successful.")
        print("Test result:", value)

except Exception as e:
    print("\nDatabase connection failed.")
    print(type(e).__name__)
    print(e)