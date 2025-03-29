from agno.agent import Agent 
from agno.models.google import Gemini
import os
from dotenv import load_dotenv

load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure that the API key is loaded properly
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")


def multiply_numbers(a: int, b:int)-> int:
     "multiply two numbers abd return the number."
     return str(a*b)


agent = Agent(
     model=Gemini(id="gemini-2.0-flash-exp", api_key=GEMINI_API_KEY),
     tools=[multiply_numbers],
     show_tool_calls=True
)

agent.print_response("what is 7 times 6?")