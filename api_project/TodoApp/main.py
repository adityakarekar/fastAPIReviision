
from fastapi import  FastAPI
import models
from database import engine
app=FastAPI()
models.Base.metadata.create_all(bind=engine)
from routers import auth,todos,admin,users
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
from models import Todos
