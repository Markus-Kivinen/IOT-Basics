### Requirements
- Python 3.13+

### Configure
- Download RPI_PICO_W-20250911-v1.26.1.uf2 from https://micropython.org/download/RPI_PICO_W/ to Embedded folder.
- Set API_URL in `Embedded/10_wifi.py` to your machine IP.  
- Copy `src/.env.example` → `src/.env` and set `WEBHOOK_URL` (optional).  
- Use `TEMP_ALERT` / `HUMIDITY_ALERT` in `.env` to tune alerts.  
<img width="355" height="107" alt="image" src="https://github.com/user-attachments/assets/28cbfc28-4f09-439d-aa98-792734397a0d" />

### Install
Using pip
```bash
python -m venv .venv

# Linux / macOS
source .venv/bin/activate
# Windows (PowerShell)
.venv\Scripts\activate

pip install -e .
```

Using uv 
```bash
uv venv --python 3.13
```

### Run the server
```bash
server  # Production mode
dev  # Auto-reload

# With uv
uv run server
uv run dev

# Other options
uvicorn src.server:app --host 0.0.0.0 --port 8000 
uvicorn src.server:app --host 0.0.0.0 --port 8000 --reload  
```
<img width="941" height="585" alt="image" src="https://github.com/user-attachments/assets/2e63ef56-b758-4c24-9526-294588f6d6e9" />  

### Docs

API documentation is available at:  
http://localhost:8000/docs and http://localhost:8000/redoc  
<img width="996" height="1090" alt="image" src="https://github.com/user-attachments/assets/731ec09d-fd21-4f4e-a7c6-4686f2976253" />
<img width="1911" height="881" alt="image" src="https://github.com/user-attachments/assets/d5b41d58-6e9a-4b3d-8d4d-eaec6d4793b0" />




### Simulating pico w 
Start Wokwi simulator with F1 -> `Wokwi: Start Simulation` or by opening diagram.json  
Wokwi simulator has to be visible to connect to it with mpremote
```
# Install ssd1306 driver from micropython-lib
python -m mpremote connect port:rfc2217://localhost:4000 mip install ssd1306
python -m mpremote connect port:rfc2217://localhost:4000 run Embedded/10_wifi.py

# With uv
uv run mpremote connect port:rfc2217://localhost:4000 mip install ssd1306
uv run mpremote connect port:rfc2217://localhost:4000 run Embedded/10_wifi.py
```
<img width="1097" height="1036" alt="image" src="https://github.com/user-attachments/assets/887ecccf-e2d7-4613-bca4-ab883fd35903" />
<img width="794" height="903" alt="image" src="https://github.com/user-attachments/assets/40135435-925e-4a94-91de-a4f0278d9b10" />

