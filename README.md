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

Alternatively you can run the server directly with uvicorn ( in activated environment):
```bash
uvicorn server:app --host 0.0.0.0 --port 8000
uvicorn server:app --host 0.0.0.0 --port 8000 --reload
```
or fastapi
```
fastapi run server.py
fastapi dev server.py
```



API documentation is available at:
http://localhost:8000/docs and http://localhost:8000/redoc
