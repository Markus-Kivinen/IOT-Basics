import sys

import uvicorn
from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from src import db
from src.models import SensorData

app = FastAPI()


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root() -> HTMLResponse:
    api_url = app.url_path_for("get_sensor_data")
    response_html = (
        "<h1>Hello World</h1>"
        f'<p>Sensor data is available at <a href="{api_url}">{api_url}</a></p>'
        f'<p>API Documentation is available at <a href="{app.docs_url}">{app.docs_url}</a>'
        f' and <a href="{app.redoc_url}">{app.redoc_url}</a></p>'
    )
    return HTMLResponse(content=response_html)


@app.get("/api/sensor", name="get_sensor_data", responses={200: {"model": list[SensorData]}})
async def get_sensor_data() -> list[SensorData]:
    return db.get_data()


@app.post("/api/sensor", name="post_sensor_data", status_code=201, responses={201: {"model": SensorData}})
async def post_sensor_data(data: SensorData, request: Request) -> SensorData:
    db.insert_data(data)
    return data


@app.post(
    "/api/user/create",
    name="create_user",
    status_code=201,
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {
                    "example": {"message": "User created successfully"}
                }
            },
        }
    },
)
async def create_user(username: str, password: str) -> dict[str, str]:
    db.create_user(username, password)
    return {"message": "User created successfully"}


@app.post(
    "/api/user/verify",
    name="verify_user",
    status_code=200,
    responses={
        200: {
            "description": "User verified successfully",
            "content": {
                "application/json": {
                    "example": {"message": "User verified successfully"}
                }
            },
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid username or password"}
                }
            },
        },
    },
)
async def verify_user(username: str, password: str) -> HTMLResponse:
    if db.verify_user(username, password):
        return HTMLResponse(content={"message": "User verified successfully"}
        )
    raise HTTPException(status_code=401, detail="Invalid username or password")


def start_server() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )


def start_dev_server() -> None:
    uvicorn.run("src.server:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    start_server()
