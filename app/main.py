import subprocess

from fastapi import FastAPI

from routers import patient, user, authentication


def create_app():
    app = FastAPI()

    app.include_router(authentication.router)
    app.include_router(patient.router)
    app.include_router(user.router)

    subprocess.run(["alembic", "upgrade", "head"])

    return app
