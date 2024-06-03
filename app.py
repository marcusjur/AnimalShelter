from hive import *
from fastapi import FastAPI, HTTPException
from typing import Union
import uvicorn

app = FastAPI()


@app.get("/login")
async def userlogin(password: str, username: str):
    try:
        session = login(username, password)
    except InvalidCredentialsError:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    return session.session_id

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=1703)
