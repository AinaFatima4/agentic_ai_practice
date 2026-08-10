import os
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled

from tools import calculator

#reading the env file to get api key and base url
load_dotenv()
set_tracing_disabled(True)

#making a basic local model using the env variables
local_model = OpenAIChatCompletionsModel(
    model=os.getenv("LLM_MODEL"),
    openai_client= AsyncOpenAI(
        base_url=os.getenv("LLM_BASE_URL"),
        api_key=os.getenv("LLM_API_KEY")     #ollama doesnt need an api key so any value works
    ),
)


#agent that uses the local model and acts like a reseacrh assistane
agent = Agent(
    name='Research Assistant',
    instructions="Act as an experienced research assistant,analyze the user's prompt and provide a dedicated researched answer with relevent sources u got " \
    "the information from , DONT TRY TO DO EVERYTHING YOURSELF, USE A TOOL IF IT FITS THE SCENARIO",
    model=local_model,
    tools=[calculator]
)

#using the Runner in the async function to run the agent with a prompt and print the final output
async def main():
    prompt = "what is the answer to 5+990*122"
    result = await Runner.run(agent, prompt)
    print(result.final_output)

asyncio.run(main())