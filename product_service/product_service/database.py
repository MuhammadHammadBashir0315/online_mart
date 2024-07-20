from sqlmodel import create_engine, Session

DATABASE_URL = ""

engine = create_engine("postgresql://product_user:product_password@localhost:5432/product_db")

def get_session():
    with Session(engine) as session:
        yield session