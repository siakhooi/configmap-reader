"""Unit tests for config_api module."""

from unittest.mock import MagicMock, patch

import pytest
from fastapi import HTTPException

from configmap_reader import config_api


@pytest.fixture(autouse=True)
def reset_k8s_client():
    """Reset the global k8s client before each test."""
    config_api._k8s_client = None
    yield
    config_api._k8s_client = None


class TestGetK8sClient:
    """Tests for _get_k8s_client function."""

    @patch("kubernetes.client.CoreV1Api")
    @patch("kubernetes.config.load_kube_config")
    @patch("kubernetes.config.load_incluster_config")
    def test_get_k8s_client_in_cluster_success(
        self, mock_incluster, mock_kubeconfig, mock_core_v1_api
    ):
        """Test successful client initialization with in-cluster config."""
        mock_api = MagicMock()
        mock_core_v1_api.return_value = mock_api

        result = config_api._get_k8s_client()

        assert result == mock_api
        mock_incluster.assert_called_once()
        mock_kubeconfig.assert_not_called()
        mock_core_v1_api.assert_called_once()

    @patch("kubernetes.client.CoreV1Api")
    @patch("kubernetes.config.load_kube_config")
    @patch("kubernetes.config.load_incluster_config")
    def test_get_k8s_client_fallback_to_kubeconfig(
        self, mock_incluster, mock_kubeconfig, mock_core_v1_api
    ):
        """Test fallback to kubeconfig when in-cluster config fails."""
        mock_incluster.side_effect = Exception("Not in cluster")
        mock_api = MagicMock()
        mock_core_v1_api.return_value = mock_api

        result = config_api._get_k8s_client()

        assert result == mock_api
        mock_incluster.assert_called_once()
        mock_kubeconfig.assert_called_once()
        mock_core_v1_api.assert_called_once()

    @patch("kubernetes.client.CoreV1Api")
    @patch("kubernetes.config.load_kube_config")
    @patch("kubernetes.config.load_incluster_config")
    def test_get_k8s_client_both_configs_fail(
        self, mock_incluster, mock_kubeconfig, mock_core_v1_api
    ):
        """Test when both config loading methods fail."""
        mock_incluster.side_effect = Exception("Not in cluster")
        mock_kubeconfig.side_effect = Exception("No kubeconfig")

        with pytest.raises(HTTPException) as exc_info:
            config_api._get_k8s_client()

        assert exc_info.value.status_code == 500
        assert "Failed to init Kubernetes client" in exc_info.value.detail

    @patch("kubernetes.client.CoreV1Api")
    @patch("kubernetes.config.load_kube_config")
    @patch("kubernetes.config.load_incluster_config")
    def test_get_k8s_client_cached(
        self, mock_incluster, mock_kubeconfig, mock_core_v1_api
    ):
        """Test that client is cached after first call."""
        mock_api = MagicMock()
        mock_core_v1_api.return_value = mock_api

        result1 = config_api._get_k8s_client()
        result2 = config_api._get_k8s_client()

        assert result1 == result2 == mock_api
        mock_incluster.assert_called_once()
        mock_core_v1_api.assert_called_once()

    @patch("kubernetes.client.CoreV1Api")
    @patch("kubernetes.config.load_kube_config")
    @patch("kubernetes.config.load_incluster_config")
    def test_get_k8s_client_import_error(
        self, mock_incluster, mock_kubeconfig, mock_core_v1_api
    ):
        """Test when kubernetes module import fails."""
        # Simulate import failure by raising exception on config access
        mock_incluster.side_effect = ImportError(
            "kubernetes not installed"
        )
        mock_kubeconfig.side_effect = ImportError(
            "kubernetes not installed"
        )

        with pytest.raises(HTTPException) as exc_info:
            config_api._get_k8s_client()

        assert exc_info.value.status_code == 500


class TestRead:
    """Tests for read function."""

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_success(self, mock_get_client):
        """Test successful ConfigMap read."""
        mock_api = MagicMock()
        mock_get_client.return_value = mock_api

        mock_cm = MagicMock()
        mock_cm.data = {
            "config.yaml": "key: value",
            "app.properties": "port=8080",
        }
        mock_api.read_namespaced_config_map.return_value = mock_cm

        result = config_api.read("my-config", "default")

        assert result == {
            "config.yaml": "key: value",
            "app.properties": "port=8080",
        }
        mock_api.read_namespaced_config_map.assert_called_once_with(
            name="my-config", namespace="default"
        )

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_empty_data(self, mock_get_client):
        """Test reading ConfigMap with None data."""
        mock_api = MagicMock()
        mock_get_client.return_value = mock_api

        mock_cm = MagicMock()
        mock_cm.data = None
        mock_api.read_namespaced_config_map.return_value = mock_cm

        result = config_api.read("my-config", "default")

        assert result == {}

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_empty_configmap_name(self, mock_get_client):
        """Test read with empty configmap_name."""
        with pytest.raises(HTTPException) as exc_info:
            config_api.read("", "default")

        assert exc_info.value.status_code == 500
        assert "CONFIGMAP_NAME is not set" in exc_info.value.detail
        mock_get_client.assert_not_called()

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_none_configmap_name(self, mock_get_client):
        """Test read with None configmap_name."""
        with pytest.raises(HTTPException) as exc_info:
            config_api.read(None, "default")

        assert exc_info.value.status_code == 500
        assert "CONFIGMAP_NAME is not set" in exc_info.value.detail
        mock_get_client.assert_not_called()

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_empty_namespace(self, mock_get_client):
        """Test read with empty namespace."""
        with pytest.raises(HTTPException) as exc_info:
            config_api.read("my-config", "")

        assert exc_info.value.status_code == 500
        assert "NAMESPACE is not set" in exc_info.value.detail
        mock_get_client.assert_not_called()

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_none_namespace(self, mock_get_client):
        """Test read with None namespace."""
        with pytest.raises(HTTPException) as exc_info:
            config_api.read("my-config", None)

        assert exc_info.value.status_code == 500
        assert "NAMESPACE is not set" in exc_info.value.detail
        mock_get_client.assert_not_called()

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_api_exception(self, mock_get_client):
        """Test read when API call fails."""
        mock_api = MagicMock()
        mock_get_client.return_value = mock_api
        mock_api.read_namespaced_config_map.side_effect = Exception(
            "ConfigMap not found"
        )

        with pytest.raises(HTTPException) as exc_info:
            config_api.read("my-config", "default")

        assert exc_info.value.status_code == 500
        detail = exc_info.value.detail
        assert "Failed to read ConfigMap default/my-config" in detail
        assert "ConfigMap not found" in detail

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_with_special_characters_in_data(self, mock_get_client):
        """Test reading ConfigMap with special characters in data."""
        mock_api = MagicMock()
        mock_get_client.return_value = mock_api

        mock_cm = MagicMock()
        mock_cm.data = {
            "file.json": '{"key": "value"}',
            "script.sh": "#!/bin/bash\necho 'test'",
        }
        mock_api.read_namespaced_config_map.return_value = mock_cm

        result = config_api.read("my-config", "prod")

        assert result == {
            "file.json": '{"key": "value"}',
            "script.sh": "#!/bin/bash\necho 'test'",
        }

    @patch("configmap_reader.config_api._get_k8s_client")
    def test_read_client_init_failure(self, mock_get_client):
        """Test read when client initialization fails."""
        mock_get_client.side_effect = HTTPException(
            status_code=500, detail="Failed to init Kubernetes client"
        )

        with pytest.raises(HTTPException) as exc_info:
            config_api.read("my-config", "default")

        assert exc_info.value.status_code == 500
        assert "Failed to init Kubernetes client" in exc_info.value.detail
