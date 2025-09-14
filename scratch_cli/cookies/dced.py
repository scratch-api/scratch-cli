# cookies but 'dced', i.e. dataclassed
from dataclasses import dataclass, field, KW_ONLY

from scratch_cli.cookies.handler import cookies as handler
from abc import ABC, abstractmethod
from typing import Self, Optional, Generic, TypeVar

cookies = None


def try_save_cookies():
    if cookies:
        if cookies.are_ready_to_be_saved:
            cookies.save()


def try_save_cookies_on_ret(func):
    def wrapper(*args, **kwargs):
        ret = func(*args, **kwargs)
        try_save_cookies()
        return ret

    return wrapper


T = TypeVar('T')
U = TypeVar('U')

KEY_T = TypeVar('KEY_T')
VAL_T = TypeVar('VAL_T')
ITEM_T = TypeVar('ITEM_T')


class AutoSave:
    @try_save_cookies_on_ret
    def __setattr__(self, key, value):
        object.__setattr__(self, key, value)


class CookieAble(ABC, AutoSave):
    @classmethod
    @abstractmethod
    def to_json(cls):
        pass

    @classmethod
    @abstractmethod
    def from_json(cls, data) -> Self:
        pass

@dataclass
class CookieList(CookieAble, Generic[ITEM_T]):
    """
    Handler for Cookied lists. Will save cookies if mutated.
    """

    _data: list[ITEM_T] = field(default_factory=list)

    @classmethod
    def from_json(cls, data: list[ITEM_T]) -> Self:
        return cls(data)

    def to_json(self):
        return self._data

    # immutable

    def __iter__(self):
        return iter(self._data)

    def __add__(self, other):
        if isinstance(other, CookieList):
            other = other._data

        return CookieList(self._data + other)

    # mutable

    @try_save_cookies_on_ret
    def __setitem__(self, key, value):
        self._data[key] = value

    @try_save_cookies_on_ret
    def __delitem__(self, key):
        del self._data[key]

@dataclass
class CookieDict(CookieAble, Generic[KEY_T, VAL_T]):
    """
    Handler for Cookied dicts. Will save cookies if mutated.
    """

    _data: dict[KEY_T, VAL_T] = field(default_factory=dict)

    @classmethod
    def from_json(cls, data: dict[KEY_T, VAL_T]) -> Self:
        return cls(data)

    def to_json(self):
        return self._data

    # dict

    ## immutables

    def get(self, __key: KEY_T, __default: T = None) -> VAL_T | T:
        return self._data.get(__key, __default)

    def items(self):
        return self._data.items()

    def __getitem__(self, item):
        return self._data[item]

    def __iter__(self):
        return iter(self._data)

    def __len__(self):
        return len(self._data)

    def __contains__(self, item):
        return item in self._data

    def __bool__(self):
        return bool(self._data)

    def keys(self):
        return self._data.keys()

    def values(self):
        return self._data.values()

    def __or__(self, other):
        if isinstance(other, CookieDict):
            other = other._data

        return CookieDict(self._data | other)

    ## mutables
    @try_save_cookies_on_ret
    def __setitem__(self, key, value):
        self._data[key] = value

    @try_save_cookies_on_ret
    def __delitem__(self, key):
        del self._data[key]

    @try_save_cookies_on_ret
    def pop(self, __key: KEY_T = None, __value: T = None) -> VAL_T | T:
        return self._data.pop(__key, __value)

@dataclass
class Cache(CookieAble):
    current_group: Optional[str]

    @classmethod
    def from_json(cls, data) -> Self:
        return cls(current_group=data.get('current_group'))

    def to_json(self):
        return {
            'current_group': self.current_group,
        }


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
    sessions: CookieList[Session]

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            name=data.get('name'),
            sessions=CookieList([Session.from_json(sess) for sess in data.get('sessions')]),
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
    groups: CookieDict[str, Group]

    _: KW_ONLY

    _cfg: CookieJarConfig = field(default_factory=CookieJarConfig)

    def __post_init__(self):
        self._cfg.being_inited = False

    @classmethod
    def from_json(cls, data: dict) -> Self:
        return cls(
            Cache.from_json(data.get('cache', {})),
            CookieDict.from_json({k: Group.from_json(v) for k, v in data.get('groups', {}).items()}),
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

        if not self.are_ready_to_be_saved or key == "_cfg":
            return

        self.save()

    @classmethod
    def load(cls):
        return cls.from_json(handler.data)

    def save(self):
        assert self.are_ready_to_be_saved, "Cookies not ready to be saved."

        handler.data = self.to_json()

    # properties for accessing special items
    @property
    def current_group_id(self):
        return self.cache.current_group

    @current_group_id.setter
    def current_group_id(self, value):
        self.cache.current_group = value

    @property
    def current_group(self):
        if self.current_group_id == '':
            return Group('', CookieList())

        return self.groups[self.current_group_id]

    @current_group.setter
    def current_group(self, value):
        self.groups[self.current_group_id] = value


if not cookies:
    # cookies should be None
    cookies = CookieJar.load()

if __name__ == '__main__':
    import random

    cookies.cache.current_group = random.choice(list(cookies.groups.keys()))
