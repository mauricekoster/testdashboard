from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
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
    docs_url=f"{settings.API_V1_STR}/swagger",
    redoc_url=f"{settings.API_V1_STR}/docs",
    generate_unique_id_function=custom_generate_unique_id,
)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title=settings.PROJECT_NAME,
        version="9.9.9",
        summary="This is a OpenAPI schema for the application",
        routes=app.routes,
    )
    openapi_schema["x-tagGroups"] = [
        dict(name="Intro", tags=[
        ]),
        dict(name="Define", tags=[
            "Requirements",
            "Requirement Types",
            "Requirement Tags",
            "Risks",
            "Risk Classifications",
            "Risk Tags",
        ]),
        dict(name="Design", tags=[
            "Folders",
            "Test Cases",
            "Test Case Tags"
        ]),
        dict(name="Plan", tags=[
            "Milestones",
            "Milestone Types",
            "Test Runs",
            "Test Run Tags",
            "My Test Runs"
        ]),
        dict(name="Track", tags=[
            "Test Results",
            "Test Result Statuses"
        ]),
        dict(name="Resolve", tags=[
            "Issues",
            "Issue Categories",
            "Issue Priorities",
            "Issue Resolutions",
            "Issue Statuses",
            "Issue Tasks",
            "Issue Tags",
            "My Issues",
            "My Issue Tasks",

        ]),
        dict(name="General", tags=[
            "Applications", 
            "Custom Fields", 
            "Environments", 
            "Projects", 
            "Symbols",
            "Teams",
            "Test Types",
            "Users",
            "Versions",
            "Webhooks"]
            ),
        dict(name="Various", tags=[
            "apps",
            "health",
            "login",
            "utils"
        ]),
    ]
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi




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