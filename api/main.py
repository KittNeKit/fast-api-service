from fastapi import FastAPI

from api.database import init_db
from api.routers import auth, post

app = FastAPI()

app.include_router(auth.router)
app.include_router(post.router)


@app.on_event("startup")
async def start_database():
    init_db()
