import sys
import os

from pathlib import Path
from typing import Final


def _gen_appdata_folder() -> Path:
    un = "scratch_api"
    match sys.platform:
        case "win32":
            return Path(os.getenv('APPDATA')) / un
        case "linux":
            return Path.home() / f".{un}"
        case plat:
            raise NotImplementedError(f"No 'appdata' folder implemented for {plat}")


PATH: Final[Path] = _gen_appdata_folder()
SCRATCHCLI: Final[Path] = PATH / "scratch_cli"
COOKIES: Final[Path] = SCRATCHCLI / "cookies.json"
TEMP: Final[Path] = SCRATCHCLI / "temp"

TEMP.mkdir(parents=True, exist_ok=True)
