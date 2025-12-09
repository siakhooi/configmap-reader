from fastapi import HTTPException

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
        raise HTTPException(
            status_code=500, detail=f"Failed to init Kubernetes client: {e}"
        )


def read(configmap_name: str, namespace: str) -> dict:
    """
    Read ConfigMap via Kubernetes API.

    Args:
        configmap_name: Name of the ConfigMap to read
        namespace: Kubernetes namespace

    Returns:
        dict: ConfigMap data as filename -> string content
    """
    if not configmap_name:
        raise HTTPException(
            status_code=500,
            detail="CONFIGMAP_NAME is not set for API read mode",  # noqa: E501
        )
    if not namespace:
        raise HTTPException(
            status_code=500, detail="NAMESPACE is not set for API read mode"
        )
    api = _get_k8s_client()
    try:
        cm = api.read_namespaced_config_map(
            name=configmap_name, namespace=namespace
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to read ConfigMap {namespace}/{configmap_name}: {e}",  # noqa: E501
        )
    data = cm.data or {}
    return dict(data)
