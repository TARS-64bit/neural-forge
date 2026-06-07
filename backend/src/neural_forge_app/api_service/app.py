from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers.ingest import router as ingest_router
from .routers.plan import router as plan_router
from .routers.status import router as status_router
from .routers.check_repo_exists import router as check_repo_exists_router


def create_app() -> FastAPI:
    app = FastAPI(title="Neural Forge API")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ingest_router)
    app.include_router(status_router)
    app.include_router(plan_router)
    app.include_router(check_repo_exists_router)

    return app


app = create_app()
