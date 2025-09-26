import sys

import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from pydantic import BaseModel

app = FastAPI()

class SensorData(BaseModel):
    temperature: float
    humidity: float
    status: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"temperature": 22.5, "humidity": 55, "status": "OK"},
                {"temperature": 50.0, "humidity": 65, "status": "Warning"},
            ],
        },
    }


@app.get("/", response_class=HTMLResponse)
async def root() -> HTMLResponse:
    api_url = app.url_path_for("get_sensor_data")
    response_html = (
        "<h1>Hello World</h1>"
        f'<p>Sensor data is available at <a href="{api_url}">{api_url}</a></p>'
        f'<p>API Documentation is available at <a href="{app.docs_url}">{app.docs_url}</a>'
        f' and <a href="{app.redoc_url}">{app.redoc_url}</a></p>'
    )
    return HTMLResponse(content=response_html)


@app.get("/api/sensor", name="get_sensor_data")
async def get_sensor_data() -> SensorData:
    return SensorData(temperature=22.5, humidity=55, status="OK")


@app.post("/api/sensor", name="post_sensor_data")
async def post_sensor_data(data: SensorData, request: Request) -> SensorData:
    print(f"Temperature {data.temperature}C, Humidity {data.humidity}%, Status {data.status}")
    return data


def start_server() -> None:
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
    sys.exit()

def start_dev_server() -> None:
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
    sys.exit()


if __name__ == "__main__":
    start_server()
