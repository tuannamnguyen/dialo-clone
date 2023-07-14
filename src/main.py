from fastapi import FastAPI
from src.routers.extension.views import extension_router

app = FastAPI()
app.include_router(extension_router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
