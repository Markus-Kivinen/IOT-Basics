from pydantic import BaseModel


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
