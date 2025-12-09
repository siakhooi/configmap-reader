from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import os
import json
import uvicorn
from . import config_dir, config_api

app = FastAPI()

CONFIG_DIR = os.getenv("CONFIG_DIR", "/config")
READ_MODE = os.getenv("READ_MODE", "volume").lower()  # 'volume' or 'api'
CONFIGMAP_NAME = os.getenv("CONFIGMAP_NAME")
K8S_NAMESPACE = os.getenv("NAMESPACE") or os.getenv("K8S_NAMESPACE")


@app.get("/config")
def get_config():
    if READ_MODE == "api":
        data = config_api.read(CONFIGMAP_NAME, K8S_NAMESPACE)
    else:
        try:
            data = config_dir.read(CONFIG_DIR)
        except FileNotFoundError as e:
            raise HTTPException(status_code=500, detail=str(e))

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Invalid config data")

    status_code_raw = data.get("statusCode")
    body = data.get("body")

    if status_code_raw is None or body is None:
        raise HTTPException(
            status_code=500, detail="Missing required keys: statusCode or body"
        )

    try:
        status_code = int(status_code_raw)
    except Exception:
        raise HTTPException(status_code=500, detail="Invalid statusCode value")

    try:
        parsed = json.loads(body)
        return JSONResponse(content=parsed, status_code=status_code)
    except Exception:
        return PlainTextResponse(content=body, status_code=status_code)


@app.get("/health")
def health():
    return {"status": "ok"}


def run():

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=False,
    )
