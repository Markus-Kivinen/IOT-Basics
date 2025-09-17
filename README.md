### Requirements
- Python 3.13+

### Install
Create the virtual environment ( choose one ):
```bash
python -m venv .venv
# Using uv
uv venv  
``` 

Activate the virtual environment:
```bash
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.\.venv\Scripts\activate
```

Install dependencies ( choose one ):
```bash
pip install -r requirements.txt
# Using uv
uv pip install -r pyproject.toml  
```

### Running the Server
After activating the environment:  

Start the server:
```bash
fastapi dev server.py  # with auto-reload
fastapi run server.py  # Production mode
```

Other options:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 
uvicorn server:app --host 0.0.0.0 --port 8000 --reload  
# without activating environment
.\.venv\Scripts\python.exe -m fastapi run server.py
# without activating environment using uv
uv run -m fastapi run server.py
```

API documentation is available at:  
http://localhost:8000/docs and http://localhost:8000/redoc
