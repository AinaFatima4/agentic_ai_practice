import gradio as gr
from agents import Runner, InputGuardrailTripwireTriggered
from agent import agent
from logger import logger


#saving chat history to keep track of the conversation between user and agent
chat_history = []


async def chat(message, history):      

    logger.info(f"USER QUERY: {message}")
    logger.info(f"AGENT: {agent.name}")

    chat_history.append({"role": "user", "content" : message})

    try:
        result = await Runner.run(agent, chat_history)

        chat_history.append({"role":"assistant", "content" : result.final_output})

        logger.info(f"FINAL RESPONSE: {result.final_output}")
        return result.final_output
    
    except InputGuardrailTripwireTriggered:
        chat_history.pop()
        message_to_user = "Sorry, I can only help with research, calculations, date/time, or employee questions."
        logger.info(f"BLOCKED BY GUARDRAIL: {message}")
        return message_to_user


demo = gr.ChatInterface(
    fn=chat,
    title="AI Research Assistant",
    description="Ask a question and let the agent find the answer.",
)

demo.launch()