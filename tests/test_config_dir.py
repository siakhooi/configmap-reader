import pytest
from configmap_reader.config_dir import read


class TestReadConfigDir:
    """Test cases for the read() function in config_dir module."""

    def test_read_returns_empty_dict_for_empty_directory(self, tmp_path):
        """Test that an empty directory returns an empty dictionary."""
        result = read(str(tmp_path))
        assert result == {}

    def test_read_single_file(self, tmp_path):
        """Test reading a single file from the config directory."""
        config_file = tmp_path / "config.txt"
        config_file.write_text("test content", encoding="utf-8")

        result = read(str(tmp_path))

        assert len(result) == 1
        assert "config.txt" in result
        assert result["config.txt"] == "test content"

    def test_read_multiple_files(self, tmp_path):
        """Test reading multiple files from the config directory."""
        file1 = tmp_path / "config1.txt"
        file1.write_text("content 1", encoding="utf-8")

        file2 = tmp_path / "config2.yaml"
        file2.write_text("content 2", encoding="utf-8")

        file3 = tmp_path / "config3.json"
        file3.write_text('{"key": "value"}', encoding="utf-8")

        result = read(str(tmp_path))

        assert len(result) == 3
        assert result["config1.txt"] == "content 1"
        assert result["config2.yaml"] == "content 2"
        assert result["config3.json"] == '{"key": "value"}'

    def test_read_ignores_subdirectories(self, tmp_path):
        """Test that subdirectories are ignored."""
        file1 = tmp_path / "config.txt"
        file1.write_text("config content", encoding="utf-8")

        subdir = tmp_path / "subdir"
        subdir.mkdir()
        file2 = subdir / "nested.txt"
        file2.write_text("nested content", encoding="utf-8")

        result = read(str(tmp_path))

        assert len(result) == 1
        assert "config.txt" in result
        assert "nested.txt" not in result
        assert "subdir" not in result

    def test_read_handles_multiline_content(self, tmp_path):
        """Test reading files with multiline content."""
        config_file = tmp_path / "multiline.txt"
        content = "line 1\nline 2\nline 3\n"
        config_file.write_text(content, encoding="utf-8")

        result = read(str(tmp_path))

        assert result["multiline.txt"] == content

    def test_read_handles_empty_files(self, tmp_path):
        """Test reading empty files."""
        empty_file = tmp_path / "empty.txt"
        empty_file.write_text("", encoding="utf-8")

        result = read(str(tmp_path))

        assert "empty.txt" in result
        assert result["empty.txt"] == ""

    def test_read_handles_special_characters(self, tmp_path):
        """Test reading files with special characters."""
        config_file = tmp_path / "special.txt"
        content = "Special: àéîöü ñ 你好 🚀\n"
        config_file.write_text(content, encoding="utf-8")

        result = read(str(tmp_path))

        assert result["special.txt"] == content

    def test_read_skips_binary_files(self, tmp_path):
        """Test that binary files that can't be decoded are skipped."""
        text_file = tmp_path / "text.txt"
        text_file.write_text("text content", encoding="utf-8")

        binary_file = tmp_path / "binary.bin"
        binary_file.write_bytes(b'\x80\x81\x82\x83')

        result = read(str(tmp_path))

        assert len(result) == 1
        assert "text.txt" in result
        assert "binary.bin" not in result

    def test_read_raises_error_for_nonexistent_directory(self):
        """Test that FileNotFoundError is raised for nonexistent directory."""
        with pytest.raises(FileNotFoundError) as exc_info:
            read("/nonexistent/path/to/config")

        assert "Config directory not found" in str(exc_info.value)
        assert "/nonexistent/path/to/config" in str(exc_info.value)

    def test_read_raises_error_when_path_is_file(self, tmp_path):
        """Test FileNotFoundError when path is a file, not directory."""
        file_path = tmp_path / "notadir.txt"
        file_path.write_text("content", encoding="utf-8")

        with pytest.raises(FileNotFoundError) as exc_info:
            read(str(file_path))

        assert "Config directory not found" in str(exc_info.value)

    def test_read_uses_default_config_dir(self, monkeypatch, tmp_path):
        """Test that read() uses CONFIG_DIR environment variable."""
        test_dir = tmp_path / "default_config"
        test_dir.mkdir()

        config_file = test_dir / "default.txt"
        config_file.write_text("default content", encoding="utf-8")

        monkeypatch.setenv("CONFIG_DIR", str(test_dir))

        # Reload the module to pick up the new environment variable
        import importlib
        import configmap_reader.config_dir
        importlib.reload(configmap_reader.config_dir)

        result = configmap_reader.config_dir.read()

        assert "default.txt" in result
        assert result["default.txt"] == "default content"

    def test_read_with_explicit_path_overrides_default(self, tmp_path):
        """Test that explicit path overrides default CONFIG_DIR."""
        custom_dir = tmp_path / "custom"
        custom_dir.mkdir()

        config_file = custom_dir / "custom.txt"
        config_file.write_text("custom content", encoding="utf-8")

        result = read(str(custom_dir))

        assert "custom.txt" in result
        assert result["custom.txt"] == "custom content"

    def test_read_preserves_whitespace(self, tmp_path):
        """Test that whitespace in files is preserved."""
        config_file = tmp_path / "whitespace.txt"
        content = "  leading spaces\ntrailing spaces  \n\t\ttabs\n"
        config_file.write_text(content, encoding="utf-8")

        result = read(str(tmp_path))

        assert result["whitespace.txt"] == content

    def test_read_handles_different_file_extensions(self, tmp_path):
        """Test reading files with various extensions."""
        extensions = [
            ".txt", ".yaml", ".yml", ".json", ".conf", ".properties", ""
        ]

        for ext in extensions:
            filename = f"config{ext}" if ext else "confignoext"
            file_path = tmp_path / filename
            file_path.write_text(
                f"content for {filename}", encoding="utf-8"
            )

        result = read(str(tmp_path))

        assert len(result) == len(extensions)
        for ext in extensions:
            filename = f"config{ext}" if ext else "confignoext"
            assert filename in result


class TestConfigDirConstant:
    """Test cases for the CONFIG_DIR constant."""

    def test_config_dir_default_value(self, monkeypatch):
        """Test that CONFIG_DIR defaults to '/config' when not set."""
        monkeypatch.delenv("CONFIG_DIR", raising=False)

        import importlib
        import configmap_reader.config_dir
        importlib.reload(configmap_reader.config_dir)

        assert configmap_reader.config_dir.CONFIG_DIR == "/config"

    def test_config_dir_from_environment(self, monkeypatch):
        """Test that CONFIG_DIR reads from environment variable."""
        monkeypatch.setenv("CONFIG_DIR", "/custom/config/path")

        import importlib
        import configmap_reader.config_dir
        importlib.reload(configmap_reader.config_dir)

        assert configmap_reader.config_dir.CONFIG_DIR == "/custom/config/path"
