import os
from dotenv import load_dotenv
from agno.agent import Agent
from agno.models.google import Gemini
from agno.storage.sqlite import SqliteStorage

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
    storage=SqliteStorage(
        table_name='agent_session',
        db_file = 'storage/agent_storage.db'
    ),
    add_history_to_messages=True,
    markdown=True,  # Optional, for markdown formatting
    show_tool_calls=True,  # Optional, shows tool calls in the response,
    session_id="f99397f5-5c16-4d34-8f24-be6973556aeb"
)

# agent.print_response("My name is Rohan. I live in Delhi", stream=True)
# agent.print_response("I also like cricket and football and my favourite player is Ronaldo.", stream=True)
agent.print_response("Who am I? where do I live and who is my favourite player?", stream=True)

## to return the conversation session we need to return the id

# print(agent.session_id)