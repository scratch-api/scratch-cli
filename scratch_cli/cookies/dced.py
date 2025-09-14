# cookies but 'dced', i.e. dataclassed
from dataclasses import dataclass, field, KW_ONLY

from scratch_cli.cookies.handler import cookies as handler
from abc import ABC, abstractmethod
from typing import Self, Optional

cookies = None


class CookieAble(ABC):
    @classmethod
    @abstractmethod
    def to_json(cls):
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data) -> Self:
        pass

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

        if cookies and cookies.are_ready_to_be_saved:
            cookies.save()


@dataclass
class Cache(CookieAble):
    _current_group: Optional[str]

    @classmethod
    def from_json(cls, data) -> Self:
        return cls(_current_group=data.get('current_group'))

    def to_json(self):
        return {
            'current_group': self._current_group,
        }

    @property
    def current_group(self):
        return self._current_group

    @current_group.setter
    def current_group(self, value):
        print(value)
        self._current_group = value


@dataclass
class Session(CookieAble):
    username: str
    id: str

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            username=data.get('username'),
            id=data.get('id'),
        )

    def to_json(self):
        return {
            "username": self.username,
            "id": self.id,
        }


@dataclass
class Group(CookieAble):
    name: str
    sessions: list[Session]

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            name=data.get('name'),
            sessions=[Session.from_json(sess) for sess in data.get('sessions')],
        )

    def to_json(self):
        return {
            "name": self.name,
            "sessions": [sess.to_json() for sess in self.sessions],
        }


@dataclass
class CookieJarConfig:
    being_inited: bool = True


@dataclass
class CookieJar(CookieAble):
    cache: Cache
    groups: dict[str, Group]

    _: KW_ONLY

    _cfg: CookieJarConfig = field(default_factory=CookieJarConfig)

    def __post_init__(self):
        self._cfg.being_inited = False

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            Cache.from_json(data.get('cache', {})),
            {k: Group.from_json(v) for k, v in data.get('groups', {}).items()},
        )

    def to_json(self):
        return {
            'cache': self.cache.to_json(),
            'groups': {k: v.to_json() for k, v in self.groups.items()},
        }

    @property
    def are_ready_to_be_saved(self) -> bool:
        return hasattr(self, "_cfg") and not self._cfg.being_inited

    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)

        if not (self.are_ready_to_be_saved or key == "_cfg"):
            return

        self.save()

    @classmethod
    def load(cls):
        return cls.from_json(handler.data)

    def save(self):
        handler.data = self.to_json()


if not cookies:
    # cookies should be None
    cookies = CookieJar.load()

if __name__ == '__main__':
    import random

    cookies.cache.current_group = random.choice(list(cookies.groups.keys()))
