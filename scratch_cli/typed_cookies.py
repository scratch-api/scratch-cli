from typing import Any, Literal, TypedDict, final

from scratch_cli.cookies import cookies as untyped_cookies


class SESSION(TypedDict):
    username: str
    id: str


class GROUP(TypedDict):
    name: str
    sessions: list[SESSION]


class CACHE(TypedDict):
    current_group: str


class COOKIES(TypedDict):
    cache: CACHE
    groups: dict[str, GROUP]


PARTIAL_TYPED: COOKIES = untyped_cookies
"""
Note: cookies isn't actually a dict, so some methods may not work.
"""


class _TypedCookies:
    @property
    def raw(self):
        return untyped_cookies.data

    @property
    def groups(self) -> dict[str, GROUP]:
        return PARTIAL_TYPED.get("groups", {})

    @groups.setter
    def groups(self, value):
        PARTIAL_TYPED["groups"] = value

    @property
    def cache(self) -> CACHE:
        return PARTIAL_TYPED.get("cache", {})

    @cache.setter
    def cache(self, value: CACHE):
        PARTIAL_TYPED["cache"] = value

    @property
    def current_group(self) -> str:
        return self.cache.get("current_group", '')

    @current_group.setter
    def current_group(self, value: str):
        self.cache = self.cache | {"current_group": value}


cookies = _TypedCookies()
