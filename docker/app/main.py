from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse, PlainTextResponse
import os
import pathlib
import json

app = FastAPI()

CONFIG_DIR = os.getenv("CONFIG_DIR", "/config")
READ_MODE = os.getenv("READ_MODE", "volume").lower()  # 'volume' or 'api'
CONFIGMAP_NAME = os.getenv("CONFIGMAP_NAME")
K8S_NAMESPACE = os.getenv("NAMESPACE") or os.getenv("K8S_NAMESPACE")

_k8s_client = None

def _get_k8s_client():
    global _k8s_client
    if _k8s_client is not None:
        return _k8s_client
    try:
        from kubernetes import client, config
        # In-cluster config first; fallback to local kubeconfig for dev
        try:
            config.load_incluster_config()
        except Exception:
            config.load_kube_config()
        _k8s_client = client.CoreV1Api()
        return _k8s_client
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to init Kubernetes client: {e}")


def read_config_dir() -> dict:
    path = pathlib.Path(CONFIG_DIR)
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Config directory not found: {CONFIG_DIR}")
    result = {}
    for p in path.iterdir():
        if p.is_file():
            try:
                content = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            result[p.name] = content
    return result


def read_config_via_api() -> dict:
    if not CONFIGMAP_NAME:
        raise HTTPException(status_code=500, detail="CONFIGMAP_NAME is not set for API read mode")
    if not K8S_NAMESPACE:
        raise HTTPException(status_code=500, detail="NAMESPACE is not set for API read mode")
    api = _get_k8s_client()
    try:
        cm = api.read_namespaced_config_map(name=CONFIGMAP_NAME, namespace=K8S_NAMESPACE)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to read ConfigMap {K8S_NAMESPACE}/{CONFIGMAP_NAME}: {e}")
    data = cm.data or {}
    # Return as filename -> string content just like volume mode
    return dict(data)


@app.get("/config")
def get_config():
    if READ_MODE == "api":
        data = read_config_via_api()
    else:
        try:
            data = read_config_dir()
        except FileNotFoundError as e:
            raise HTTPException(status_code=500, detail=str(e))

    if not isinstance(data, dict):
        raise HTTPException(status_code=500, detail="Invalid config data")

    status_code_raw = data.get("statusCode")
    body = data.get("body")

    if status_code_raw is None or body is None:
        raise HTTPException(status_code=500, detail="Missing required keys: statusCode or body")

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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app.main:app", host="0.0.0.0", port=int(os.getenv("PORT", "8000")), reload=False)
