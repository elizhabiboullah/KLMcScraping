from .database import engine, Base
from .models import Outlet

def init_db():
    Base.metadata.create_all(bind=engine)

if __name__ == "__main__":
    init_db()
    print("DB init mate? lol")
