from app.database import Base, engine

# Import models so SQLAlchemy knows about the tables
from app.models.analysis import MedicineAnalysis


print("Creating MediLens database tables...")


try:
    Base.metadata.create_all(bind=engine)

    print("\nDatabase tables created successfully.")
    print("Table created: medicine_analyses")

except Exception as e:
    print("\nFailed to create database tables.")
    print(type(e).__name__)
    print(e)