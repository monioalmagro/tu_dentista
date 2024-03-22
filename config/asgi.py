"""
ASGI config for config project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""

# Standard Libraries
import logging
import os

# Third-party Libraries
from django.core.asgi import get_asgi_application
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from strawberry.fastapi import GraphQLRouter

# Own Libraries
from config.enviroment_vars import settings

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

application = get_asgi_application()

# Own Libraries
from apps.core.schema.api import schema

graphql_app = GraphQLRouter(schema, path="/psychology/")

fastapp = FastAPI()
fastapp.include_router(graphql_app, prefix="/api/graph")


origins = [
    "http://localhost",
    settings.DECIRES_URL,
    # settings.GRAPHQL_URL,
]

fastapp.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
