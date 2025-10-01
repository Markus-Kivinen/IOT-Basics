### Requirements
- Python 3.13+
- npm


### Configure
In `Embedded/10_wifi.py`: replace API_URL with your machine’s IP and port  
Download Pico W firmware and place it in Embedded, add the path to `Embedded/wokwi.toml`  
Install Wokwi VS Code extension https://docs.wokwi.com/vscode/getting-started  

### Webhook ( optional )
<img width="355" height="107" alt="image" src="https://github.com/user-attachments/assets/28cbfc28-4f09-439d-aa98-792734397a0d" />

Create a `src/.env` file based on `src/.env.example` and set your WEBHOOK_URL  
use TEMP_ALERT and HUMIDITY_ALERT to set alert thresholds

### Install
Create the virtual environment ( choose one ):
```bash
python -m venv .venv
# Using uv
uv venv --python 3.13
``` 

Activate the virtual environment:
```bash
# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\activate
```

Install dependencies ( choose one ):
```bash
pip install -r pylock.toml
# Using uv
uv pip install -r pylock.toml
```

### Running the Server
After activating the environment:  

Start the server:
```bash
fastapi run src/server.py  # Production mode
fastapi dev src/server.py  # Auto-reload
# With uv
uv run server
uv run dev
```

Other options:
```bash
uvicorn src.server:app --host 0.0.0.0 --port 8000 
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload  
```
<img width="941" height="585" alt="image" src="https://github.com/user-attachments/assets/2e63ef56-b758-4c24-9526-294588f6d6e9" />


API documentation is available at:  
http://localhost:8000/docs and http://localhost:8000/redoc
<img width="996" height="1090" alt="image" src="https://github.com/user-attachments/assets/731ec09d-fd21-4f4e-a7c6-4686f2976253" />
<img width="1911" height="881" alt="image" src="https://github.com/user-attachments/assets/d5b41d58-6e9a-4b3d-8d4d-eaec6d4793b0" />




### Simulating pico w 
Start Wokwi simulator with F1 -> `Wokwi: Start Simulation` or by opening diagram.json  
Wokwi simulator has to be visible to connect to it with mpremote
```
# With .venv activated
python -m mpremote connect port:rfc2217://localhost:4000 run Embedded/10_wifi.py
# With uv
uv run mpremote connect port:rfc2217://localhost:4000 run Embedded/10_wifi.py
```
