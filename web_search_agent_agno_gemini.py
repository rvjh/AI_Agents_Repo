from agno.agent import Agent, RunResponse  # noqa
from agno.models.google import Gemini
import os
from dotenv import load_dotenv
load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
agent = Agent(model=Gemini(id="gemini-2.0-flash-exp",api_key=api_key), markdown=True)

agent.print_response("Share a 2 sentence horror story")
