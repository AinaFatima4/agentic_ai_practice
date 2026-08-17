import os
import json

from dotenv import load_dotenv
import asyncio
from openai import AsyncOpenAI

from agents import (
    Agent,
    GuardrailFunctionOutput,
    InputGuardrailTripwireTriggered,
    RunContextWrapper,
    Runner,
    TResponseInputItem,
    input_guardrail,
    OpenAIChatCompletionsModel, 
    set_tracing_disabled
)


from tools import calculator
from tools import get_current_time
from tools import get_employee_info
from tools import search_knowledge_base

from pydantic import BaseModel



#pydantic model to store guardrail agent's output
class guardrail_output(BaseModel):
    is_correct_input : bool
    reasoning : str



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

#agent to make decisions about input prompts
guardrail_agent = Agent(
    name='Input Guardrail',
    instructions="detect whether the prompt asks for one of the following : math equations, current date and time ,only professional/workplace information about employees, never personal or family details. /no_think",
    model=local_model,
    output_type=guardrail_output
)

@input_guardrail
async def input_guardrail(
    ctx: RunContextWrapper[None],
    agent: Agent,
    input: str | list[TResponseInputItem],

) -> GuardrailFunctionOutput:
    result = await Runner.run(guardrail_agent, input, context=ctx.context)
    return GuardrailFunctionOutput(
        output_info=result.final_output,
        tripwire_triggered= not result.final_output.is_correct_input,
    )

#agent that uses the local model and acts like a reseacrh assistane
agent = Agent(
    name='Research Assistant',
    instructions="Act as an experienced research assistant,analyze the user's prompt and provide a dedicated researched answer with relevent sources u got " \
    "the information from , DONT TRY TO DO EVERYTHING YOURSELF, USE A TOOL IF IT FITS THE SCENARIO /no_think",
    model=local_model,
    tools=[calculator, get_current_time, get_employee_info , search_knowledge_base],
    input_guardrails=[input_guardrail]
    )

