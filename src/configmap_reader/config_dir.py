import pathlib
import os


CONFIG_DIR = os.getenv("CONFIG_DIR", "/config")


def read(config_dir: str = CONFIG_DIR) -> dict:
    """Read all files from the config directory and return as a dictionary.

    Args:
        config_dir: Path to the configuration directory

    Returns:
        Dictionary mapping filenames to their content

    Raises:
        FileNotFoundError: If the config directory doesn't exist or
            isn't a directory
    """
    path = pathlib.Path(config_dir)
    if not path.exists() or not path.is_dir():
        raise FileNotFoundError(f"Config directory not found: {config_dir}")
    result = {}
    for p in path.iterdir():
        if p.is_file():
            try:
                content = p.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            result[p.name] = content
    return result
