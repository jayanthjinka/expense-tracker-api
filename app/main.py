from fastapi import FastAPI
from app.db.database import engine, Base
from app.models import user, expense  # noqa: F401
from app.routers import auth, expenses

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(auth.router)
app.include_router(expenses.router)


@app.get("/")
def root():
    return {"message": "Expense Tracker Backend Running"}
