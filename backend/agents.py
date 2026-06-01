from crewai import Agent, LLM
from crewai_tools import SerperDevTool

class ProductAnalysisAgents:
    def __init__(self):
        # Initialize CrewAI's native LLM configuration for Groq
        self.groq_llm = LLM(
            model="groq/llama3-8b-8192",  # Native string format: provider/model-name
            temperature=0.7
        )
        # Initialize Google Search tool via crewai-tools
        self.search_tool = SerperDevTool()

    def product_analyst_agent(self) -> Agent:
        return Agent(
            role="Senior Business Development & Product Analyst",
            goal="Conduct deep competitive analysis and uncover strategic market trends.",
            backstory=(
                "You are an expert product strategist with a background in venture capital "
                "and market positioning. You specialize in breaking down product specifications, "
                "identifying market gaps, and evaluating competitor strengths and weaknesses."
            ),
            tools=[self.search_tool],
            llm=self.groq_llm,
            verbose=True,
            allow_delegation=False
        )