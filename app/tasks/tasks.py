from celery import Celery
import asyncio
from app.agents.manager import AgentManager

celery = Celery(
    broker="redis://localhost:6379/0",
    backend="redis://localhost:6379/0"
)

celery.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="UTC",
    enable_utc=True,
)

manager = AgentManager()

@celery.task
def run_agent():
    return asyncio.run(manager.orchestrator.run())


@celery.task
def run_workflow(prompt: str):
    return asyncio.run(manager.run(prompt))
