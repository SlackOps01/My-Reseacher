from pydantic_ai import RunContext
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIResponsesModel
from pydantic_ai.providers.ollama import OllamaProvider

class BaseAgent:

    def __init__(self, name: str, model_name: str, system_prompt: str, tools=None):
        self.name = name
        self.model_name = model_name
        self.system_prompt = system_prompt
        self.agent = self._setup_agent(tools)
        

    def _setup_agent(self, tools):
        model = OpenAIResponsesModel(
            model_name=self.model_name,
            provider=OllamaProvider(
                base_url="http://localhost:11434/v1"
            )
        )

        return Agent(name=self.name, model=model, system_prompt=self.system_prompt, builtin_tools=tools or [])

    async def run(self, message: str):
        response = await self.agent.run(message)
        return response.output

    
class SubAgent(BaseAgent):
    def register_as_tool(self, parent: Agent):
        tool_name = f"ask_{self.name.lower().replace(' ', '_')}"
        async def call_sub_agent(ctx: RunContext, prompt: str):
            response = await self.agent.run(prompt)
            return response.output
        
        call_sub_agent.__name__ = tool_name
        call_sub_agent.__doc__ = f"Ask {self.name}, his role is {self.system_prompt}"
        parent.tool(call_sub_agent)
        return call_sub_agent
