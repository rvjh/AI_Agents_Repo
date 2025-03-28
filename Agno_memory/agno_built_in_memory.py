import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini

# Load environment variables from the .env file
load_dotenv()

# Retrieve the GEMINI_API_KEY from environment variables
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# Ensure that the API key is loaded properly
if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY is not set. Please check your .env file.")

# Initialize the agent with the Gemini model and the provided API key
agent = Agent(
    model=Gemini(id="gemini-2.0-flash-exp", api_key=GEMINI_API_KEY),
    add_history_to_messages=True,
    num_history_responses=2,
    markdown=True,  # Optional, for markdown formatting
    show_tool_calls=True  # Optional, shows tool calls in the response
)

# Simulate a conversation and print the responses
agent.print_response("My name is Rohan", stream=True)
agent.print_response("I live in Delhi", stream=True)
agent.print_response("I also like cricket?", stream=True)
agent.print_response("Where do I live?", stream=True)
