from app.agents.specialized_agents import OrchestratorAgent, ResearcherAgent, WriterAgent, CritiqueAgent


class AgentManager:
    def __init__(self):
        self.orchestrator = OrchestratorAgent()
        self.researcher = ResearcherAgent()
        self.writer = WriterAgent()
        self.critique = CritiqueAgent()
        self._setup_orchestration()

    def _setup_orchestration(self):
        self.researcher.register_as_tool(self.orchestrator.agent)
        self.writer.register_as_tool(self.orchestrator.agent)
        self.critique.register_as_tool(self.orchestrator.agent)

    async def run(self, message: str):
        return await self.orchestrator.run(message)