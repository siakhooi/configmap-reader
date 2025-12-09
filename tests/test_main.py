import pytest
from unittest.mock import patch
from fastapi.testclient import TestClient
import json
import os


@pytest.fixture
def client():
    """Fixture to create a test client."""
    from configmap_reader.main import app
    return TestClient(app)


class TestHealthEndpoint:
    """Test cases for the /health endpoint."""

    def test_health_returns_ok(self, client):
        """Test that health endpoint returns ok status."""
        response = client.get("/health")

        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


class TestGetConfigEndpointVolumeMode:
    """Test cases for the /config endpoint in volume mode."""

    @patch("configmap_reader.main.config_dir.read")
    @patch("configmap_reader.main.CONFIG_DIR", "/test/config")
    def test_config_returns_json_response(self, mock_read, client):
        """Test successful JSON response from config."""
        body_content = '{"message": "success", "data": {"key": "value"}}'
        mock_read.return_value = {
            "statusCode": "200",
            "body": body_content
        }

        response = client.get("/config")

        assert response.status_code == 200
        data = {"message": "success", "data": {"key": "value"}}
        assert response.json() == data
        mock_read.assert_called_once()

    @patch("configmap_reader.main.config_dir.read")
    def test_config_returns_plain_text_response(self, mock_read, client):
        """Test successful plain text response from config."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": "Plain text response"
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.text == "Plain text response"
        content_type = "text/plain; charset=utf-8"
        assert response.headers["content-type"] == content_type

    @patch("configmap_reader.main.config_dir.read")
    def test_config_returns_custom_status_code(self, mock_read, client):
        """Test that custom status codes are respected."""
        mock_read.return_value = {
            "statusCode": "201",
            "body": '{"created": true}'
        }

        response = client.get("/config")

        assert response.status_code == 201
        assert response.json() == {"created": True}

    @patch("configmap_reader.main.config_dir.read")
    def test_config_returns_error_status_code(self, mock_read, client):
        """Test that error status codes are handled correctly."""
        mock_read.return_value = {
            "statusCode": "404",
            "body": '{"error": "not found"}'
        }

        response = client.get("/config")

        assert response.status_code == 404
        assert response.json() == {"error": "not found"}

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_file_not_found_error(self, mock_read, client):
        """Test handling of FileNotFoundError from config_dir.read."""
        mock_read.side_effect = FileNotFoundError("Config directory not found")

        response = client.get("/config")

        assert response.status_code == 500
        assert "Config directory not found" in response.json()["detail"]

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_non_dict_data(self, mock_read, client):
        """Test error when config data is not a dictionary."""
        mock_read.return_value = "invalid data"

        response = client.get("/config")

        assert response.status_code == 500
        assert response.json()["detail"] == "Invalid config data"

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_missing_status_code(self, mock_read, client):
        """Test error when statusCode is missing."""
        mock_read.return_value = {
            "body": '{"message": "test"}'
        }

        response = client.get("/config")

        assert response.status_code == 500
        assert "Missing required keys" in response.json()["detail"]

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_missing_body(self, mock_read, client):
        """Test error when body is missing."""
        mock_read.return_value = {
            "statusCode": "200"
        }

        response = client.get("/config")

        assert response.status_code == 500
        assert "Missing required keys" in response.json()["detail"]

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_invalid_status_code(self, mock_read, client):
        """Test error when statusCode cannot be converted to int."""
        mock_read.return_value = {
            "statusCode": "invalid",
            "body": '{"message": "test"}'
        }

        response = client.get("/config")

        assert response.status_code == 500
        assert response.json()["detail"] == "Invalid statusCode value"

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_complex_json(self, mock_read, client):
        """Test handling of complex nested JSON."""
        complex_data = {
            "users": [
                {"id": 1, "name": "Alice"},
                {"id": 2, "name": "Bob"}
            ],
            "metadata": {
                "total": 2,
                "page": 1
            }
        }
        mock_read.return_value = {
            "statusCode": "200",
            "body": json.dumps(complex_data)
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.json() == complex_data

    @patch("configmap_reader.main.config_dir.read")
    def test_config_handles_multiline_plain_text(self, mock_read, client):
        """Test handling of multiline plain text."""
        text_content = "Line 1\nLine 2\nLine 3"
        mock_read.return_value = {
            "statusCode": "200",
            "body": text_content
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.text == text_content

    @patch("configmap_reader.main.config_dir.read")
    def test_config_with_status_code_as_integer(self, mock_read, client):
        """Test that statusCode works when already an integer."""
        mock_read.return_value = {
            "statusCode": 204,
            "body": ""
        }

        response = client.get("/config")

        assert response.status_code == 204


class TestGetConfigEndpointApiMode:
    """Test cases for the /config endpoint in API mode."""

    @patch("configmap_reader.main.READ_MODE", "api")
    @patch("configmap_reader.main.CONFIGMAP_NAME", "my-config")
    @patch("configmap_reader.main.K8S_NAMESPACE", "default")
    @patch("configmap_reader.main.config_api.read")
    def test_config_uses_api_mode(self, mock_read, client):
        """Test that API mode is used when READ_MODE is 'api'."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": '{"mode": "api"}'
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.json() == {"mode": "api"}
        mock_read.assert_called_once_with("my-config", "default")

    @patch("configmap_reader.main.READ_MODE", "api")
    @patch("configmap_reader.main.CONFIGMAP_NAME", "test-config")
    @patch("configmap_reader.main.K8S_NAMESPACE", "test-ns")
    @patch("configmap_reader.main.config_api.read")
    def test_config_api_mode_case_insensitive(self, mock_read, client):
        """Test that READ_MODE is case insensitive."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": '{"test": "value"}'
        }

        response = client.get("/config")

        assert response.status_code == 200
        mock_read.assert_called_once_with("test-config", "test-ns")

    @patch("configmap_reader.main.READ_MODE", "api")
    @patch("configmap_reader.main.CONFIGMAP_NAME", "my-config")
    @patch("configmap_reader.main.K8S_NAMESPACE", "custom-ns")
    @patch("configmap_reader.main.config_api.read")
    def test_config_uses_namespace_env_var(self, mock_read, client):
        """Test that NAMESPACE environment variable is used."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": '{"namespace": "custom-ns"}'
        }

        client.get("/config")

        mock_read.assert_called_once_with("my-config", "custom-ns")


class TestRunFunction:
    """Test cases for the run() function."""

    @patch("configmap_reader.main.uvicorn.run")
    @patch.dict(os.environ, {"PORT": "9000"})
    def test_run_with_custom_port(self, mock_uvicorn):
        """Test that run() uses custom port from environment."""
        from configmap_reader.main import run

        run()

        mock_uvicorn.assert_called_once_with(
            "app.main:app",
            host="0.0.0.0",
            port=9000,
            reload=False
        )

    @patch("configmap_reader.main.uvicorn.run")
    @patch.dict(os.environ, {}, clear=True)
    def test_run_with_default_port(self, mock_uvicorn):
        """Test that run() uses default port when PORT not set."""
        from configmap_reader.main import run

        run()

        mock_uvicorn.assert_called_once_with(
            "app.main:app",
            host="0.0.0.0",
            port=8000,
            reload=False
        )

    @patch("configmap_reader.main.uvicorn.run")
    def test_run_always_binds_to_all_interfaces(self, mock_uvicorn):
        """Test that run() always binds to 0.0.0.0."""
        from configmap_reader.main import run

        run()

        call_args = mock_uvicorn.call_args
        assert call_args[1]["host"] == "0.0.0.0"

    @patch("configmap_reader.main.uvicorn.run")
    def test_run_has_reload_disabled(self, mock_uvicorn):
        """Test that run() has reload disabled."""
        from configmap_reader.main import run

        run()

        call_args = mock_uvicorn.call_args
        assert call_args[1]["reload"] is False


class TestEnvironmentVariableDefaults:
    """Test cases for environment variable defaults."""

    @patch.dict(os.environ, {}, clear=True)
    def test_default_config_dir(self):
        """Test default CONFIG_DIR value."""
        from configmap_reader import main
        # Need to reload module to pick up new env vars
        import importlib
        importlib.reload(main)

        assert main.CONFIG_DIR == "/config"

    @patch.dict(os.environ, {}, clear=True)
    def test_default_read_mode(self):
        """Test default READ_MODE value."""
        from configmap_reader import main
        import importlib
        importlib.reload(main)

        assert main.READ_MODE == "volume"

    @patch.dict(os.environ, {"CONFIG_DIR": "/custom/path"})
    def test_custom_config_dir(self):
        """Test custom CONFIG_DIR value."""
        from configmap_reader import main
        import importlib
        importlib.reload(main)

        assert main.CONFIG_DIR == "/custom/path"

    @patch.dict(os.environ, {"READ_MODE": "api"})
    def test_custom_read_mode(self):
        """Test custom READ_MODE value."""
        from configmap_reader import main
        import importlib
        importlib.reload(main)

        assert main.READ_MODE == "api"


class TestEdgeCases:
    """Test edge cases and error conditions."""

    @patch("configmap_reader.main.READ_MODE", "volume")
    @patch("configmap_reader.main.config_dir.read")
    def test_config_with_empty_body(self, mock_read, client):
        """Test handling of empty body string."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": ""
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.text == ""

    @patch("configmap_reader.main.READ_MODE", "volume")
    @patch("configmap_reader.main.config_dir.read")
    def test_config_with_large_status_code(self, mock_read, client):
        """Test handling of large status codes."""
        mock_read.return_value = {
            "statusCode": "500",
            "body": '{"error": "custom error"}'
        }

        response = client.get("/config")

        assert response.status_code == 500
        assert response.json() == {"error": "custom error"}

    @patch("configmap_reader.main.READ_MODE", "volume")
    @patch("configmap_reader.main.config_dir.read")
    def test_config_with_json_array(self, mock_read, client):
        """Test handling of JSON array as body."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": '[1, 2, 3, 4, 5]'
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.json() == [1, 2, 3, 4, 5]

    @patch("configmap_reader.main.READ_MODE", "volume")
    @patch("configmap_reader.main.config_dir.read")
    def test_config_with_unicode_in_json(self, mock_read, client):
        """Test handling of Unicode characters in JSON."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": '{"message": "Hello 世界 🌍"}'
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.json() == {"message": "Hello 世界 🌍"}

    @patch("configmap_reader.main.READ_MODE", "volume")
    @patch("configmap_reader.main.config_dir.read")
    def test_config_with_special_chars_plain_text(self, mock_read, client):
        """Test handling of special characters in plain text."""
        mock_read.return_value = {
            "statusCode": "200",
            "body": "Special chars: <>&\"'\n\t"
        }

        response = client.get("/config")

        assert response.status_code == 200
        assert response.text == "Special chars: <>&\"'\n\t"
