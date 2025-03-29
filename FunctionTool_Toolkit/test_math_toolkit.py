from agno.agent import Agent
from agno.models.google import Gemini
import os
from dotenv import load_dotenv
from math_toolkit import MathToolkit  # Corrected import

# Load environment variables from the .env file
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure that the API key is loaded properly
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

# Initialize the agent with the Gemini model and the provided API key
agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", api_key=GEMINI_API_KEY),
    tools=[MathToolkit()],  # Use MathToolkit here
    show_tool_calls=True
)

# Ask the agent to perform a math operation
agent.print_response("What is 15 divided by 3?")

agent.print_response("What is 15 - 3?")
