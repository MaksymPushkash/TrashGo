

from fastapi import FastAPI
from backend.app.api.v1 import orders, users, auth
from backend.app.db.session import Base, engine


def create_app() -> FastAPI:

    app = FastAPI(title="TrashGo API")


    app.include_router(users.router, prefix="/api/v1")
    app.include_router(orders.router, prefix="/api/v1")
    app.include_router(auth.router, prefix="/api/v1")


    Base.metadata.create_all(bind=engine)


    @app.get("/")
    def healthcheck() -> dict[str, str]:
        return {"status": "ok"}

    return app



app = create_app()


