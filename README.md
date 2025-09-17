Create virtual environment and install dependencies:  
```bash
./install.sh
```
Or with uv:  
```bash
./install_uv.sh
```


Run the server in production mode:
```bash
./server.sh
```

Run the server in development mode:
```bash
./server.sh dev
```

Alternatively you can run the server directly with uvicorn:
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
```

API documentation is available at:
http://localhost:8000/docs and http://localhost:8000/redoc