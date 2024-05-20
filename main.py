#!/usr/bin/env python3
import frontend
import backend
from fastapi import FastAPI

app = FastAPI(openapi_url="/api/openapi.json")


app.include_router(backend.router, prefix="/api")

frontend.init(app)

if __name__ == "__main__":
    print(
        'Please start the app with the "uvicorn" command as shown in the start.sh script'
    )
