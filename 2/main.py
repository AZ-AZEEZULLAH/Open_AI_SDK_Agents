from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
import os
from dotenv import load_dotenv

import chainlit as cl # pyright: ignore[reportMissingImports]

# Load environment variables
load_dotenv()
gemini_api_key = os.getenv("GEMINI_API_KEY")

# Create Async Gemini/OpenAI API client
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai"
)

# Set up Gemini 2.0 Flash model
model = OpenAIChatCompletionsModel(
    model="gemini-2.0-flash",
    openai_client=external_client
)

# Configure model run settings
Config = RunConfig(
    model=model,
    model_provider=external_client,
    tracing_disabled=True
)

# Create the AI agent
agent = Agent(
    name="Frontend Export Agent",
    instructions="You are an agent that helps to export frontend code based on user requirements."
)

# Run agent synchronously and get response
# result = Runner.run_sync(
#     agent,
#     input="Hello, how are you?",
#     run_config=Config
# )

# # Print final AI response
# print(result.final_output)

@cl.on_chat_start
async def handle_start():
     cl.user_session.set("history",[])
     await cl.Message(content="Hello! I am Azeezullah. How can I help you today?").send()
@cl.on_message
async def handle_message(message:cl.Message):
    #  content = message.content
     history =cl.user_session.get("history")
     history.append({"role":"user","content":message.content})
     result = await Runner.run(
          agent,
        #   input=message.content,
          input=history,
          run_config=Config
     )
     history.append({"role":"assistant","content":result.final_output})
     cl.user_session.set("history",history)
     await cl.Message(content=result.final_output).send()

