import os
from dotenv import load_dotenv
from agno.agent import Agent, AgentMemory
from agno.models.google import Gemini
from agno.memory.db.sqlite import SqliteMemoryDb
from agno.storage.agent.sqlite import SqliteAgentStorage  # Corrected typo

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
    memory=AgentMemory(
        db=SqliteMemoryDb(
            table_name='agent_memory',
            db_file='./storage/agent.db'  # Ensure correct path
        ),
        create_user_memories=True,
        update_session_summary_after_run=True,
        create_session_summary=True,
        update_user_memories_after_run=True
    ),
    storage=SqliteAgentStorage(
        table_name='agent_session',
        db_file='./storage/agent_storage.db'  # Ensure correct path
    ),
    add_history_to_messages=True,
    markdown=True,  # Optional, for markdown formatting
    show_tool_calls=True
)

try:
    agent.print_response("My name is Rohan. I live in Delhi", stream=True)
    agent.print_response("I also like cricket and football and my favourite player is Ronaldo.", stream=True)
    agent.print_response("what do you know about the?", stream=True)
except Exception as e:
    print(f"An error occurred during agent response: {e}")