"""
Implement example about how to handle an agent session and manage an agent memory.

Memorry are isolated between sessions and agents.

Three types of memory (Google ADK):
    - InMemorySessionService: Stored in RAM, not persistance between sessions=> for quick prototyping
    - DatabaseSesionServive : Stiore in DB with persisatnce between sessions=> for Small/medium Apps
    - Agent engine session : Production on GCP for entreprise scale session

# DatabaseSesionServive
All the events are stored in full in the session Database, and this quickly adds up which may harm and slow down performance..

Context Compaction helps solving this problem: EventsCompactionConfig
Context Compaction have several techniques (not covered here) like SlidingWindowCompactor
ADK's Context Compaction feature reduces the context that's stored in the Session.
PS/ The demo does not work because of a bug in the ADK library: "AttributeError: 'dict' object has no attribute 'start_timestamp'


# Session State
In many scenario we many need only some key information to share accross sessions
The problem with Context is that it still contains a lot of information to transfer accross them.
In these scenarios, instead of sharing the entire session history, transferring information from a few key variables can improve the session experience

"""

from typing import Any, Dict, Optional

from google.adk.agents import Agent, LlmAgent
from google.adk.apps.app import App, EventsCompactionConfig
from google.adk.models.google_llm import Gemini
from google.adk.sessions import DatabaseSessionService
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.adk.tools.tool_context import ToolContext
from google.genai import types
from agentic_learning.utils.utils import load_env
import sqlite3
import asyncio
import os   
from  loguru import logger

# Define helper functions that will be reused throughout the notebook
# Define helper functions that will be reused throughout the notebook
from google.adk.events.event import Event
import google.adk.flows.llm_flows.contents as contents_module
import google.adk.apps.compaction as compaction_module
from google.adk.apps.app import App
from google.adk.apps.llm_event_summarizer import LlmEventSummarizer
from google.adk.sessions.base_session_service import BaseSessionService
from google.adk.sessions.session import Session

async def run_session(
    runner_instance: Runner,
    user_queries: list[str] | str = None,
    session_name: str = "default",
    user_id: str = "default",
):
    print(f"\n ### Session: {session_name}")

    # Get app name from the Runner
    app_name = runner_instance.app_name

    # Attempt to create a new session or retrieve an existing one
    try:
        session = await runner.session_service.create_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )
    except:
        session = await runner.session_service.get_session(
            app_name=app_name, user_id=user_id, session_id=session_name
        )

    # Process queries if provided
    if user_queries:
        # Convert single query to list for uniform processing
        if type(user_queries) == str:
            user_queries = [user_queries]

        # Process each query in the list sequentially
        for query in user_queries:
            print(f"\nUser > {query}")

            # Convert the query string to the ADK Content format
            query = types.Content(role="user", parts=[types.Part(text=query)])

            # Stream the agent's response asynchronously
            async for event in runner_instance.run_async(
                user_id=user_id, session_id=session.id, new_message=query
            ):
                # Check if the event contains valid content
                if event.content and event.content.parts:
                    # Filter out empty or "None" responses before printing
                    if (
                        event.content.parts[0].text != "None"
                        and event.content.parts[0].text
                    ):
                        model_name = runner.agent.model
                        print(f"{model_name} > ", event.content.parts[0].text)
    else:
        print("No queries!")

def get_db_url():
    return os.path.join(os.path.dirname(__file__), "my_agent_data.db")

def build_db_memory_agent_run(
    app_name: str, 
    user_id: str, 
    session_id: str, 
    model_name: str = "gemini-2.5-flash-lite",
    events_compaction: Optional[bool] = True):

    # Step 1: Create the same agent (notice we use LlmAgent this time)
    

    # Step 2: Switch to DatabaseSessionService
    # SQLite database will be created automatically
    # Create the database next to this script file
    db_url = get_db_url()
    session_service = DatabaseSessionService(db_url=f"sqlite+aiosqlite:///{db_url}")

    chatbot_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot with persistent memory",
    )

    if events_compaction:
        # Re-define our app with Events Compaction enabled
        research_app_compacting = App(
            name="research_app_compacting",
            root_agent=chatbot_agent,
            # This is the new part!
            events_compaction_config=EventsCompactionConfig(
                compaction_interval=3,  # Trigger compaction every 3 invocations
                overlap_size=1,  # Keep 1 previous turn for context
            ),
        )   

        # Create a new runner for our upgraded app
        runner = Runner(
            app=research_app_compacting, session_service=session_service
        )

    else :
        # Step 3: Create a new runner with persistent storage
        runner = Runner(
            agent=chatbot_agent, 
            app_name=app_name, 
            session_service=session_service
        )
   
    print("✅ Upgraded to persistent sessions!")
    return runner

def check_data_in_db():
    """Print the contecnt of the Sqlite DataBase to show the compaction effect"""
    """The database logs all events and interactions, but without compaction this can generate a huge """
    """ volume of data that can impact the performance. """
    db_url = get_db_url()

    with sqlite3.connect(db_url) as connection:
        cursor = connection.cursor()
        result = cursor.execute(
            "select app_name, session_id, author, content from events"
        )
        print([_[0] for _ in result.description])
        for each in result.fetchall():
            print(each)


def build_in_memory_agent_run(app_name: str, user_id: str, session_id: str, model_name: str = "gemini-2.5-flash-lite"):
    # Step 1: Create the LLM Agent
    root_agent = Agent(
        model=Gemini(model=model_name, retry_options=retry_config),
        name="text_chat_bot",
        description="A text chatbot",  # Description of the agent's purpose
    )

    # Step 2: Set up Session Management
    # InMemorySessionService stores conversations in RAM (temporary)
    session_service = InMemorySessionService()

    # Step 3: Create the Runner
    runner = Runner(agent=root_agent, app_name=app_name, session_service=session_service)

    print("✅ Stateful agent initialized!")
    print(f"   - Application: {app_name}")
    print(f"   - User: {user_id}")
    print(f"   - Using: {session_service.__class__.__name__}")

    return runner


######################### USER STATE ############################################

# Define scope levels for state keys (following best practices)
USER_NAME_SCOPE_LEVELS = ("temp", "user", "app")

# This demonstrates how tools can write to session state using tool_context.
# The 'user:' prefix indicates this is user-specific data.
def save_userinfo(
    tool_context: ToolContext, user_name: str, country: str
) -> Dict[str, Any]:
    """
    Tool to record and save user name and country in session state.

    Args:
        user_name: The username to store in session state
        country: The name of the user's country
    """
    # Write to session state using the 'user:' prefix for user data
    tool_context.state["user:name"] = user_name
    tool_context.state["user:country"] = country

    return {"status": "success"}


# This demonstrates how tools can read from session state.
def retrieve_userinfo(tool_context: ToolContext) -> Dict[str, Any]:
    """
    Tool to retrieve user name and country from session state.
    """
    # Read from session state
    user_name = tool_context.state.get("user:name", "Username not found")
    country = tool_context.state.get("user:country", "Country not found")

    return {"status": "success", "user_name": user_name, "country": country}

def build_agent_with_user_state(app_name: str, retry_config: types.HttpRetryOptions):
    # Create an agent with session state tools
    root_agent = LlmAgent(
        model=Gemini(model="gemini-2.5-flash-lite", retry_options=retry_config),
        name="text_chat_bot",
        description="""A text chatbot.
    Tools for managing user context:
    * To record username and country when provided use `save_userinfo` tool. 
    * To fetch username and country when required use `retrieve_userinfo` tool.
    """,
        tools=[save_userinfo, retrieve_userinfo],  # Provide the tools to the agent
    )

    # Set up session service and runner
    session_service = InMemorySessionService()
    runner = Runner(agent=root_agent, session_service=session_service, app_name=app_name)
    return runner

########################################################################

if __name__ == "__main__":

    RUN_MODE = "StateTools" # InMemory or DBMemory or CheckDB
    load_env()

    retry_config = types.HttpRetryOptions(
        attempts=5,  # Maximum retry attempts
        exp_base=7,  # Delay multiplier
        initial_delay=1,
        http_status_codes=[429, 500, 503, 504],  # Retry on these HTTP errors
    )
    
    if RUN_MODE ==  "InMemory" : 
        runner = build_in_memory_agent_run(
            app_name="default", 
            user_id="default", 
            session_id="default"
            )

    elif RUN_MODE == "DBMemory" :
        runner = build_db_memory_agent_run(
            app_name="default", 
            user_id="default", 
            session_id="default"
            )

        asyncio.run(run_session(
                runner,
                [
                    "What is the latest news about AI in healthcare?",
                    "Are there any new developments in drug discovery?",
                    "Tell me more about the second development you found?",
                    "Who are the main companies involved in that?",
                ],
                "compaction_demo",
            ))
        exit(0)
    elif RUN_MODE == "StateTools" :
        runner = build_agent_with_user_state(
            app_name="user_state_demo", 
            retry_config=retry_config
            )

        asyncio.run(run_session(
            runner,
            [
                "Hi there, how are you doing today? What is my name?",  # Agent shouldn't know the name yet
                "My name is Ridha. I'm from Abu Dhabi.",  # Provide name - agent should save it
                "What is my name? Which country am I from?",  # Agent should recall from session state
            ],
            "state-demo-session",
        ))
        
        # Retrieve the session and inspect its state
        session = asyncio.run(runner.session_service.get_session(
            app_name="user_state_demo", user_id="default", session_id="state-demo-session"
        ))
        runner.close()
        
        print("Session State Contents 1:")
        print(session.state)
        print("\n🔍 Notice the 'user:name' and 'user:country' keys storing our data!")
        
        print("\n🔍 Now running a new session without providing name or country")
        print("\n*****************************************")
        runner2 = build_agent_with_user_state(
            app_name="user_state_demo", 
            retry_config=retry_config
            )
        
        asyncio.run(run_session(
            runner2,
            [
                "Hi there, how are you doing today? What is my name?",  # Agent shouldn't know the name yet
             ],
            "state-demo-session-2",
        ))
        
        # Retrieve the session and inspect its state
        session2= asyncio.run(runner2.session_service.get_session(
            app_name="user_state_demo", user_id="default", session_id="state-demo-session-2"
        ))

        print("Session State Contents 2:")
        print(session2.state)
        print("\n🔍 Notice the 'user:name' and 'user:country' are not shared accross the session but persistant accross the state")
       
        exit(0)
    else :
        check_data_in_db()
        exit(0)

    msg = [
        "Hi, I am Ridha! What is the capital of Tunisia?",
        "Hello! What is my name?",  # This time, the agent should remember!
    ]

    asyncio.run(runner.run_debug(msg))