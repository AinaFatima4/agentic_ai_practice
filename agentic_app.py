import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled

# 1. Turn off tracing.
#    Tracing tries to send run data to OpenAI's servers, which needs an
#    OpenAI API key. We are running locally on Ollama, so we switch it off.
set_tracing_disabled(True)

# 2. Create a client that points at Ollama instead of OpenAI.
#    Ollama exposes an OpenAI-compatible address at http://localhost:11434/v1
#    The api_key is required by the client, but Ollama does not check it,
#    so any text works.
ollama_client = AsyncOpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama",
)

# 3. Wrap that client in a "model" object the agent understands.
#    This is where we name the exact Ollama model we pulled.
local_model = OpenAIChatCompletionsModel(
    model="qwen3:4b",
    openai_client=ollama_client,
)

# 4. Create the agent: a name, its job description, and the model to use.
#    The "/no_think" at the end is the Qwen switch we discussed — it keeps
#    this first answer clean (no brainstorming block).
research_assistant_agent = Agent(
    name="Research Assistant",
    instructions="You are a helpful research assistant. Answer the user's question clearly and concisely. /no_think",
    model=local_model,
)


# 5. Define an async function that runs the agent and prints the answer.
async def main():
    user_question = "In one sentence, what is an AI agent?"

    result = await Runner.run(research_assistant_agent, user_question)

    print("Question:", user_question)
    print("Answer:", result.final_output)


# 6. Start the async machinery and actually run main().
asyncio.run(main())