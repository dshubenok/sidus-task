from functools import wraps
from json import dumps, loads
from typing import Optional, List

from aioredis import Redis
from aioredis import from_url
from hashlib import md5


class Cache:
    backend: Redis = None
    prefix: str = None

    @classmethod
    def init(
            cls,
            url: str,
            encoding="utf8",
            decode_responses=True,
            prefix: str = ""
    ):
        cls.backend = from_url(
            url=url,
            encoding=encoding,
            decode_responses=decode_responses
        )

        cls.prefix = prefix

    @classmethod
    def build_key(
            cls,
            namespace,
            args: Optional[tuple] = None,
            kwargs: Optional[dict] = None,
            keys: List[str] = None
    ):
        if keys:
            kwargs_keys = {k: str(kwargs[k]) for k in keys}
        else:
            kwargs_keys = dumps(kwargs, default=str)

        cache_key = f"{cls.prefix}:{namespace}:"
        cache_key += md5(f"{args[1:]}:{kwargs_keys}".encode()).hexdigest()

        return cache_key

    @classmethod
    def get(cls, key: str):
        return cls.backend.get(key)

    @classmethod
    def set(
            cls,
            key: str,
            value: str,
            ex=None,
            px=None,
            nx: bool = None,
            xx: bool = None,
            keepttl: bool = False
    ):
        return cls.backend.set(
            key,
            value,
            ex=ex,
            px=px,
            nx=nx,
            xx=xx,
            keepttl=keepttl
        )

    @classmethod
    def delete(cls, key: str):
        return cls.backend.delete(key)


def cache(namespace: Optional[str] = "", model=None, keys: List[str] = None):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            if not kwargs.get("no_cache", False) and Cache.backend is not None:
                cache_key = Cache.build_key(
                    namespace=namespace,
                    args=args,
                    kwargs=kwargs,
                    keys=keys
                )

                cached_value = await Cache.get(cache_key)

                if cached_value:
                    cached_value = loads(cached_value)
                    if model:
                        cached_value = model(**cached_value)
                    return cached_value

                results = await func(*args, **kwargs)

                if hasattr(results, "json"):
                    data = results.json()
                else:
                    data = dumps(results)

                await Cache.set(key=cache_key, value=data)
            else:
                results = await func(*args, **kwargs)

            return results
        return inner
    return wrapper


def cache_update(
        namespace: Optional[str] = "",
        keys: List[str] = None
):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            if Cache.backend is not None:
                cache_key = Cache.build_key(
                    namespace=namespace,
                    args=args,
                    kwargs=kwargs,
                    keys=keys
                )

                results = await func(*args, **kwargs)

                if hasattr(results, "json"):
                    data = results.json()
                else:
                    data = dumps(results)

                await Cache.set(key=cache_key, value=data)
            else:
                results = await func(*args, **kwargs)

            return results
        return inner
    return wrapper


def cache_remove(
        namespace: Optional[str] = "",
        keys: List[str] = None
):
    def wrapper(func):
        @wraps(func)
        async def inner(*args, **kwargs):
            if Cache.backend is not None:
                cache_key = Cache.build_key(
                    namespace=namespace,
                    args=args,
                    kwargs=kwargs,
                    keys=keys
                )

                await Cache.delete(key=cache_key)
            results = await func(*args, **kwargs)

            return results
        return inner
    return wrapper
