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
from app.tasks.tasks import run_workflow
from app.schemas import ResearchRequest, ResearchResponse, TaskStatusResponse
from fastapi.middleware.cors import CORSMiddleware


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Lifecycle manager for the FastAPI app.
    Handles startup and shutdown events.
    """
    logger.info("Starting application...")
    yield
    logger.info("Shutting down application...")


app = FastAPI(
    title="BillieJean Agent API",
    description="API for managing AI research agents.",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(SlowAPIMiddleware)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/", summary="Root Endpoint", description="Redirects to the API documentation.")
@limiter.limit("10 per minute")
async def root(request: Request) -> RedirectResponse:
    """
    Root endpoint that redirects users to the Swagger UI documentation.
    """
    return RedirectResponse(url="/docs")


@app.post(
    "/research", 
    response_model=ResearchResponse, 
    summary="Start Research Task", 
    description="Initiates a new background research task based on the provided prompt."
)
async def research(request: ResearchRequest):
    """
    **Starts a research process.**

    - **prompt**: The topic to research.
    
    Returns a `task_id` which can be used to poll for results.
    """
    task = run_workflow.delay(request.prompt)
    return {
        "message": "Research started",
        "task_id": task.id
    }

@app.get(
    "/research/{task_id}", 
    response_model=TaskStatusResponse, 
    summary="Get Task Status",
    description="Retrieves the current status and result of a specific research task."
)
def get_research(task_id: str):
    """
    **Check the status of a task.**

    - **task_id**: The ID returned by the start endpoint.
    
    **States:**
    - `PENDING`: Task is waiting in queue or currently executing.
    - `SUCCESS`: Task completed successfully. Result is available.
    - `FAILURE`: Task failed.
    """
    result = run_workflow.AsyncResult(task_id)
    return {
        "state": result.state,
        "result": result.result
    }



