from db.connection import engine
from db.models import Base


def init_database():
    Base.metadata.create_all(bind=engine)
    print("Database table created successfully")


if __name__ == "__main__":
    init_database()