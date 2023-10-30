from functools import wraps

from fastapi import HTTPException

from app.schemas.generation import generation_schema_example


def live_mode(func):
    @wraps(func)
    def wrapper_live_mode(*args, **kwargs):
        if kwargs["live_mode"]:
            return func(*args, **kwargs)
        else:
            return generation_schema_example

    return wrapper_live_mode


def validate_content(support_content_types):
    def decorator(func):
        @wraps(func)
        def wrapper_validate_content(*args, **kwargs):
            if kwargs["upload_file"].content_type not in support_content_types:
                raise HTTPException(
                    status_code=415,
                    detail=f"Content type must be {support_content_types}.",
                )
            else:
                return func(*args, **kwargs)

        return wrapper_validate_content

    return decorator
