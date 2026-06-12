from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from slowapi.errors import RateLimitExceeded
import os
from .routers.ingest import router as ingest_router
from .routers.plan import router as plan_router
from .routers.status import router as status_router
from .routers.check_repo_exists import router as check_repo_exists_router
from .routers.github_router import router as github_router
from .helpers.rate_limiter import limiter
load_dotenv()

def create_app() -> FastAPI:
    app = FastAPI(title="Neural Forge API")

    app.state.limiter = limiter

    @app.exception_handler(RateLimitExceeded)
    async def custom_rate_limit_handler(request: Request, exc: RateLimitExceeded):
        return JSONResponse(
            status_code=429,
            content={"detail": "Rate limit exceeded. Please slow down and try again later."}
        )
    
    origins_str = os.getenv("ALLOWED_ORIGINS", "http://localhost:3000,http://127.0.0.1:3000")
    
    # allowed_origins = [
    #     origin.strip().strip('"').strip("'").rstrip("/") 
    #     for origin in origins_str.split(",") 
    #     if origin.strip()
    # ]

    app.add_middleware(
        CORSMiddleware,
         allow_origins=[
            "https://neural-forge-v2-two.vercel.app", 
            "http://localhost:3000",
            "http://127.0.0.1:3000"
        ],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ingest_router)
    app.include_router(status_router)
    app.include_router(plan_router)
    app.include_router(check_repo_exists_router)
    app.include_router(github_router)

    return app

app = create_app()
