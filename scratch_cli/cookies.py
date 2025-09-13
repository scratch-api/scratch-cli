# store 'cookies' in appdata
import json

from typing import Any

from scratch_cli import appdata


class _Cookies:
    def __init__(self):
        (appdata.COOKIES / '..').resolve().mkdir(parents=True, exist_ok=True)
        if not appdata.COOKIES.exists():
            appdata.COOKIES.write_text("{}")

    @property
    def data(self) -> dict[str, str | int | None | bool | float | list | dict[str, Any]]:
        return json.load(appdata.COOKIES.open())

    @data.setter
    def data(self, data: dict[str, str | int | None | bool | float | list | dict[str, Any]]):
        json.dump(data, appdata.COOKIES.open("w"))

    def __setitem__(self, key: str, value: str | int | None | bool | float | list | dict[str, Any]):
        self.data |= {key: value}

    def __getitem__(self, key):
        return self.data[key]

    def __delitem__(self, key: str):
        self.data = {k: v for k, v in self.data.items() if k != key}

    def __contains__(self, item):
        return item in self.data

    def get(self, __key: str, __default=None):
        return self.data.get(__key, __default)


cookies = _Cookies()
