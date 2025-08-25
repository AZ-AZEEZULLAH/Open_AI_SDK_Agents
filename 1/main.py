from agents import Runner, Agent, OpenAIChatCompletionsModel, AsyncOpenAI, RunConfig
import os
from dotenv import load_dotenv

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
result = Runner.run_sync(
    agent,
    input="Hello, how are you?",
    run_config=Config
)

# Print final AI response
print(result.final_output)


