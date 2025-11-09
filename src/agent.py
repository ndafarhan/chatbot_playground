from langchain.agents import create_agent
from src.llm import get_llm


class AgentExecutor:
    def __init__(self, model_name: str, base_url: str, api_key: str):
        self.llm = get_llm(model_name, base_url, api_key)

    def create(self, system_prompt: str):
        agent = create_agent(
            model=self.llm,
            tools=[],
            system_prompt=system_prompt
        )
        return agent