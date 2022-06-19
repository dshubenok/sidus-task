from functools import wraps

from fastapi import HTTPException
from fastapi import status as http_status
from sqlalchemy.exc import IntegrityError


def handle_integrity_error(detail="The object already exists!"):
    def decorate(function):
        @wraps(function)
        async def wrapper(*args, **kwargs):

            try:
                result = await function(*args, **kwargs)
            except IntegrityError:
                raise HTTPException(
                    status_code=http_status.HTTP_403_FORBIDDEN,
                    detail=detail
                )

            return result
        return wrapper
    return decorate
