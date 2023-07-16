from fastapi import FastAPI

from src.routers.extension.views import extension_router
from src.routers.queue.views import queue_router
from src.routers.user.views import user_router

app = FastAPI()
app.include_router(extension_router)
app.include_router(user_router)
app.include_router(queue_router)

@app.get("/")
async def root():
    return {"message": "Hello World"}
