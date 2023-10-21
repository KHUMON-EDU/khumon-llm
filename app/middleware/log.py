from starlette.middleware.base import BaseHTTPMiddleware
from app.utils.logger import logger
from datetime import datetime
class LogMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        logger.info(
            "Incoming request",
            extra={
                "timestamp": {"datetime": str(datetime.now())},
                "req": {"method": request.method, "url": str(request.url)},
                "res": {"status_code": response.status_code}
            }
        ) 
        return response