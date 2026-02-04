# BillieJean

BillieJean is an advanced AI agent orchestration system built with FastAPI, Celery, and Pydantic-AI. It manages a team of specialized agents (Orchestrator, Researcher, Writer, Critique) to perform complex research and content generation tasks.

## 🚀 Features

- **Multi-Agent Orchestration**: A hierarchical agent system with an Orchestrator managing specialized sub-agents.
- **Asynchronous Task Processing**: Powered by Celery and Redis for robust background job handling.
- **AI-Powered**: Utilizes Ollama and local LLMs (e.g., `qwen3:4b`, `lfm2.5`) via `pydantic-ai` for intelligent reasoning.
- **Tool Use**: Agents are equipped with tools (like DuckDuckGo Search) to gather real-time information.
- **Rate Limiting**: Integrated `slowapi` for API rate limiting.
- **Structured Logging**: Rich console logging for better observability.

## 🛠️ Tech Stack

- **Framework**: FastAPI (Python 3.12+)
- **Task Queue**: Celery
- **Broker/Backend**: Redis
- **AI/LLM**: Pydantic-AI + Ollama
- **Local Dev**: Uvicorn, WatchFiles

## 📦 Installation

1. **Clone the repository**:

    ```bash
    git clone https://github.com/SlackOps01/My-Reseacher.git
    cd My-Reseacher
    ```

2. **Set up Virtual Environment**:

    ```bash
    python -m venv .venv
    source .venv/bin/activate
    pip install -r requirements.txt
    ```

3. **Start Services**:
    - **Redis**: Ensure Redis is running on `localhost:6379`.
    - **Ollama**: Ensure Ollama is running (`ollama serve`) and you have the required models pulled (e.g., `ollama pull qwen3:4b`).

## 🏃‍♂️ Usage

You need to run the FastAPI server and the Celery worker in separate terminals.

### 1. Start Celery Worker

This processes the background AI tasks.

```bash
celery -A app.tasks.tasks worker --loglevel=info
```

### 2. Start FastAPI Server

This provides the HTTP API.

```bash
uvicorn app.main:app --reload
```

## 🔌 API Endpoints

### `POST /research`

Starts a new research task.

**Request:**

```json
{
  "prompt": "Who is the current President of Nigeria?"
}
```

**Response:**

```json
{
  "message": "Research started",
  "task_id": "39072c97-ed79-4456-a4a0-082983fcdb5e"
}
```

### `GET /research/{task_id}`

Checks the status and result of a task.

**Response (Pending):**

```json
{
  "state": "PENDING",
  "result": null
}
```

**Response (Success):**

```json
{
  "state": "SUCCESS",
  "result": "The current President of Nigeria is Bola Ahmed Tinubu..."
}
```

## 📂 Project Structure

```
My-Reseacher/
├── app/
│   ├── agents/          # Agent definitions (Manager, Specialized Agents)
│   ├── core/            # Config, Logging, Limiter
│   ├── prompts/         # System prompts for agents
│   ├── tasks/           # Celery task definitions
│   ├── main.py          # FastAPI application entry point
│   └── ...
├── .env                 # Environment variables
├── README.md            # Project documentation
└── ...
```
