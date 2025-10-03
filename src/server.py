import asyncio
import datetime as dt
import logging
from os import getenv
from typing import Annotated

import dotenv
import httpx
import uvicorn
from fastapi import (
    FastAPI,
    HTTPException,
    Query,
    Request,
    WebSocket,
    WebSocketDisconnect,
)
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from src import Database, SensorData, SensorInput, User, UserData

dotenv.load_dotenv()
logger = logging.getLogger(__name__)
database = Database("sensor_data.db")

app = FastAPI()
templates = Jinja2Templates(directory="templates")


TEMP_ALERT = float(getenv("TEMP_ALERT", "50.0"))
HUMIDITY_ALERT = float(getenv("HUMIDITY_ALERT", "80.0"))
WEBHOOK_URL = getenv("WEBHOOK_URL")


@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def root(request: Request) -> HTMLResponse:
    api_url: str = app.url_path_for("get_sensor_data")
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "api_url": api_url,
            "docs_url": app.docs_url,
            "redoc_url": app.redoc_url,
        },
    )


@app.get(
    "/api/sensor",
    name="get_sensor_data",
    responses={200: {"model": list[SensorData]}},
)
async def get_sensor_data(
    start: Annotated[
        str | None, Query(description="Start date (YYYY-MM-DD)")
    ] = None,
    end: Annotated[
        str | None, Query(description="End date (YYYY-MM-DD)")
    ] = None,
) -> list[SensorData]:
    return database.get_data(start, end)


@app.post(
    "/api/sensor",
    name="post_sensor_data",
    status_code=201,
    responses={201: {"model": SensorData}},
)
async def post_sensor_data(data: SensorInput, request: Request) -> SensorData:
    sensor_data = database.insert_data(data)
    if WEBHOOK_URL and (
        sensor_data.temperature >= TEMP_ALERT or sensor_data.humidity >= HUMIDITY_ALERT
    ):
        timestamp_dt = dt.datetime.strptime(
            sensor_data.timestamp, "%Y-%m-%d %H:%M:%S"
        ).replace(tzinfo=dt.UTC)  # pyright: ignore[reportArgumentType]
        local_tz = dt.datetime.now().astimezone().tzinfo
        timestamp_local = timestamp_dt.astimezone(local_tz)
        timestamp: str = timestamp_local.strftime("%Y-%m-%d %H:%M:%S")
        msg = [f"**{timestamp}**."]
        if sensor_data.temperature >= TEMP_ALERT:
            msg.append(f"High temperature detected: {sensor_data.temperature}°C.")
        if sensor_data.humidity >= HUMIDITY_ALERT:
            msg.append(f"High humidity detected: {sensor_data.humidity}%.")
        async with httpx.AsyncClient() as client:
            await client.post(
                WEBHOOK_URL,
                json={"content": "\n".join(msg)},
            )
    return sensor_data


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket) -> None:
    await websocket.accept()
    try:
        while True:
            data: list[dict[str, str]] = [
                d.model_dump() for d in database.get_data()
            ]
            await websocket.send_json(data)
            await asyncio.sleep(5)

    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
    except asyncio.CancelledError:
        logger.warning("WebSocket task was cancelled")
        raise
    except Exception:
        logger.exception("Unexpected error in WebSocket connection")
    finally:
        try:
            await websocket.close()
        except RuntimeError:
            logger.warning("WebSocket already closed")


@app.post(
    "/api/user/create",
    name="create_user",
    status_code=201,
    responses={
        201: {
            "description": "User created successfully",
            "content": {
                "application/json": {"example": {"id": 1, "username": "admin"}}
            },
        }
    },
)
async def create_user(user_data: UserData) -> User:
    return database.create_user(user_data.username, user_data.password)


@app.get(
    "/api/users",
    name="get_users",
    responses={200: {"model": list[User]}},
)
async def get_users() -> list[User]:
    return database.get_users()


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
    if database.verify_user(username, password):
        return HTMLResponse(content={"message": "User verified successfully"})
    raise HTTPException(status_code=401, detail="Invalid username or password")


def start_server() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )


def start_dev_server() -> None:
    uvicorn.run(
        "src.server:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
        access_log=True,
    )


if __name__ == "__main__":
    start_server()
