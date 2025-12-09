import argparse
from importlib.metadata import version
from . import main


def run() -> None:
    __version__: str = version("configmap-reader")

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        description="Read and return content of a configmap"
    )

    parser.add_argument(
        "-v", "--version", action="version", version=f"%(prog)s {__version__}"
    )

    parser.parse_args()

    main.run()
