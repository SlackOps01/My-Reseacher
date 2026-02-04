from fastapi import FastAPI, Request
from fastapi.responses import RedirectResponse
from app.core.limiter import limiter
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded
from slowapi.middleware import SlowAPIMiddleware
from app.core.logging import logger
from contextlib import asynccontextmanager
from redis.asyncio import Redis
from app.core.config import settings
from app.tasks.tasks import run_research

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


app = FastAPI(lifespan=lifespan)

app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


@app.get("/")
@limiter.limit("10 per minute")
async def root(request: Request) -> RedirectResponse:
    return RedirectResponse(url="/docs")


@app.post("/research")
async def research(prompt: str):
    task = run_research.delay(prompt)
    return {
        "message": "Research started",
        "task_id": task.id
    }

@app.get("/research/{task_id}")
def get_research(task_id: str):
    result = run_research.AsyncResult(task_id)
    return {
        "state": result.state,
        "result": result.result
    }



