# Standard Library
from collections.abc import Callable
from typing import Generic, Self, TypeVar

K = TypeVar("K")
T = TypeVar("T")


class CachingDict(dict[K, T], Generic[K, T]):
    cache_factory: Callable[[K], T]

    def __init__(self: Self, cache_factory: Callable[[K], T]) -> None:
        self.cache_factory = cache_factory
        super().__init__()

    def __missing__(self: Self, __key: K) -> T:
        self.__setitem__(__key, self.cache_factory(__key))
        return self[__key]


def test_caching_dict() -> None:
    test_dict = CachingDict[str, str](lambda key: f"{key}-{key}")
    assert test_dict["test"] == "test-test"
