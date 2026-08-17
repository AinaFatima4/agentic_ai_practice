import gradio as gr
from agents import Runner, SQLiteSession, InputGuardrailTripwireTriggered
from agent import agent
from logger import logger

session = SQLiteSession("aina_conversation")


async def chat(message, history):      

    logger.info(f"USER QUERY: {message}")
    logger.info(f"AGENT: {agent.name}")

    try:
        result = await Runner.run(agent, message, session=session)
        logger.info(f"FINAL RESPONSE: {result.final_output}")
        return result.final_output
    
    except InputGuardrailTripwireTriggered:
        message_to_user = "Sorry, I can only help with research, calculations, date/time, or employee questions."
        logger.info(f"BLOCKED BY GUARDRAIL: {message}")
        return message_to_user


demo = gr.ChatInterface(
    fn=chat,
    title="AI Research Assistant",
    description="Ask a question and let the agent find the answer.",
)

demo.launch()