"""Module containing FastAPI instance related functions and classes."""
# mypy: ignore-errors
import logging.config
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .api import api_router
from .configs import get_settings
from .db import Base, engine
from .events import startup_handler, shutdown_handler
from .middlewares import log_time
from .version import __version__


def create_db_tables():
    """Create all tables in database."""
    Base.metadata.create_all(engine)


def create_application() -> FastAPI:
    """Create a FastAPI instance.

    Returns:
        object of FastAPI: the fastapi application instance.
    """
    settings = get_settings()
    application = FastAPI(title=settings.PROJECT_NAME,
                          debug=settings.DEBUG,
                          version=__version__,
                          openapi_url=f"{settings.API_STR}/openapi.json")

    # Set all CORS enabled origins
    if settings.CORS_ORIGINS:
        application.add_middleware(
            CORSMiddleware,
            allow_origins=[str(origin) for origin in
                           settings.CORS_ORIGINS],
            allow_origin_regex=settings.CORS_ORIGIN_REGEX,
            allow_credentials=settings.CORS_CREDENTIALS,
            allow_methods=settings.CORS_METHODS,
            allow_headers=settings.CORS_HEADERS,
        )

    # add defined routers
    application.include_router(api_router, prefix=settings.API_STR)

    # event handler
    application.add_event_handler("startup", startup_handler)
    application.add_event_handler("shutdown", shutdown_handler)

    # load logging config
    logging.config.dictConfig(settings.LOGGING_CONFIG)

    # add defined middleware functions
    application.add_middleware(BaseHTTPMiddleware, dispatch=log_time)

    # create tables in db
    create_db_tables()

    return application
