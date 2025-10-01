from pydantic import BaseModel


class SensorInput(BaseModel):
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

class SensorData(SensorInput):
    timestamp: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"temperature": 22.5, "humidity": 55, "status": "OK", "timestamp": "2025-01-01T12:00:00"},
                {"temperature": 50.0, "humidity": 65, "status": "Warning", "timestamp": "2025-01-01T12:00:00"},
            ],
        },
    }


class UserData(BaseModel):
    username: str
    password: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"username": "admin", "password": "strongpassword"},
                {"username": "user1", "password": "anotherpassword"},
            ],
        },
    }

class User(BaseModel):
    id: int
    username: str

    model_config = {
        "json_schema_extra": {
            "examples": [
                {"id": 1, "username": "admin"},
                {"id": 2, "username": "user1"},
            ],
        },
    }
