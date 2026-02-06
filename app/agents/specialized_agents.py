from pydantic_ai.builtin_tools import WebSearchTool
from app.agents.tools.search import safe_duckduckgo_search_tool
from app.agents.base import SubAgent
import pathlib
from app.agents.tools.writing import write_pdf


root_path = pathlib.Path(__file__).parent.parent



class OrchestratorAgent(SubAgent):
    with open(root_path / "prompts/orchestrator.txt", "r") as f:
        system_prompt = f.read()
    
    def __init__(self) -> None:
        super().__init__(
            name="Orchestrator",
            model_name="openrouter/free",
            system_prompt=self.system_prompt
        )

class ResearcherAgent(SubAgent):
    with open(root_path / "prompts/researcher.txt", "r") as f:
        system_prompt = f.read()
    
    def __init__(self) -> None:
        super().__init__(
            name="Researcher",
            model_name="openrouter/free",
            system_prompt=self.system_prompt,
            tools=[safe_duckduckgo_search_tool()]
        )
        
    
class WriterAgent(SubAgent):
    with open(root_path / "prompts/writer.txt", "r") as f:
        system_prompt = f.read()
    
    def __init__(self) -> None:
        super().__init__(
            name="Writer",
            model_name="openrouter/free",
            system_prompt=self.system_prompt,
            tools=[write_pdf]
        )

class CritiqueAgent(SubAgent):
    with open(root_path / "prompts/critique.txt", "r") as f:
        system_prompt = f.read()
    
    def __init__(self) -> None:
        super().__init__(
            name="Critique",
            model_name="openrouter/free",
            system_prompt=self.system_prompt
        )