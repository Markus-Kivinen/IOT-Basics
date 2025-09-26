### Requirements
- Python 3.13+
- npm


### Configure
Change subdomain in `package.json` and `Embedded/10_wifi.py`  
Download Pico W firmware and place it in Embedded, add the path to `Embedded/wokwi.toml`  
Install Wokwi VS Code extension https://docs.wokwi.com/vscode/getting-started  

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
fastapi run server.py  # Production mode
fastapi dev server.py  # Auto-reload
# With uv
uv run server
uv run dev
```

Other options:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000 
uvicorn server:app --host 0.0.0.0 --port 8000 --reload  
```

API documentation is available at:  
http://localhost:8000/docs and http://localhost:8000/redoc


### Simulating pico w 
```
# With .venv activated
python -m mpremote connect port:rfc2217://localhost:4000 run Embedded/10_wifi.py
# With uv
uv run mpremote connect port:rfc2217://localhost:4000 run Embedded/10_wifi.py
```

### Tunneling
To expose your local server to the internet, you can use a tunneling service. This repo uses `localtunnel`.
```
npm install
npm run tunnel
```
