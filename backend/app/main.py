from fastapi import FastAPI

from fastapi.routing import APIRoute
from fastapi.staticfiles import StaticFiles

from starlette.middleware.cors import CORSMiddleware

from app.api.main import api_router
from app.core.config import settings

import logging
import sys

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s.%(msecs)04d [%(levelname)s] %(message)s',
                    datefmt='%d-%m-%Y %H:%M:%S')
logger = logging.getLogger(__name__)

stream_handler = logging.StreamHandler(sys.stdout)
log_formatter = logging.Formatter("%(asctime)s [%(processName)s: %(process)d] [%(threadName)s: %(thread)d] [%(levelname)s] %(name)s: %(message)s")
stream_handler.setFormatter(log_formatter)
logger.addHandler(stream_handler)


def custom_generate_unique_id(route: APIRoute) -> str:
    return f"{route.tags[0]}-{route.name}"

def register_log_filter() -> None:
    """
    Removes logs from healthiness/readiness endpoints so they don't spam
    and pollute application log flow
    """

    class EndpointFilter(logging.Filter):
        def filter(self, record: logging.LogRecord) -> bool:
            # logger.info(f":: {record.args}")
            return (
                record.args  # type: ignore
                and len(record.args) >= 3
                and not record.args[2].endswith("/health")
                and not record.args[2].endswith("/ready")
                
            )

    temp_logger = logging.getLogger("uvicorn.access")
    temp_logger.addFilter(EndpointFilter())
    temp_logger.propagate = False

    logger.info("Add EndPoint filter")


app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url=f"{settings.API_V1_STR}/docs",
    redoc_url=f"{settings.API_V1_STR}/redoc",
    generate_unique_id_function=custom_generate_unique_id,
)

register_log_filter()

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[
            str(origin).strip("/") for origin in settings.BACKEND_CORS_ORIGINS
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router, prefix=settings.API_V1_STR)

logger.info(f"DATA_PATH: {settings.output_path}")
logger.info(f"API_V1_STR: {settings.API_V1_STR}")


# Set location of the Static folder (url to retrieve the documents)
app.mount(
    f"{settings.API_V1_STR}/reports",
    StaticFiles(directory=settings.output_path),
    name="reports",
)