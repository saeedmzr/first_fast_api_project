from fastapi import FastAPI
from routes.posts import router as post_router

app = FastAPI()
app.include_router(post_router)
