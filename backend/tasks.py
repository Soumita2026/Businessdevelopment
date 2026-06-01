from crewai import Task, Agent

class Productanalysistask:
    def analyze_product_task(self, agent: Agent, product_name: str) -> Task:
        return Task(
            description=(
                f"Analyze the market landscape, competitive positioning, and core features "
                f"associated with: '{product_name}'. Utilize your search tools to gather real-world, "
                f"up-to-date data on existing alternatives, customer pain points, and target demographics."
            ),
            expected_output=(
                "A comprehensive Markdown report summarizing key competitors, a feature breakdown matrix, "
                "identified market gaps, and strategic business development recommendations."
            ),
            agent=agent
        )