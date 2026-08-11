import os
from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI
from agents import Agent, Runner, OpenAIChatCompletionsModel, set_tracing_disabled

from tools import calculator
from tools import get_current_time
from tools import get_employee_info
fomm tools import search_knowledge_base


from pydantic import BaseModel

import json


#reading the env file to get api key and base url
load_dotenv()
set_tracing_disabled(True)



#use a pydantic class to add structure to the agent's output
class output_structure(BaseModel):
    tool_ouput : str
    model_ouptt : str
    sources : str


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
    instructions="Act as a reseacrh assistant to answer user queries, use the relevant tools when neccessary, if tools are not" \
    "relevent you may use your own knowledge base"
    "provide source of your output - if you used a tool - give the tool name as the source",
    model=local_model,
    tools=[calculator, get_current_time, get_employee_info , search_knowledge_base],
    output_type=output_structure
)

#using the Runner in the async function to run the agent with a prompt and print the final output
async def main():


    prompt = input("Enter your prompt: ")
    result = await Runner.run(agent, prompt)
    print(result.final_output)

asyncio.run(main())