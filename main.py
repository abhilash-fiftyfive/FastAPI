from fastapi import FastAPI, HTTPException, Request
import uvicorn
from app import user, restaurant

app = FastAPI()

app.include_router(user.router)
app.include_router(restaurant.router)

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8001, reload=True)