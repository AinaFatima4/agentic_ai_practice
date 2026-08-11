import gradio as gr
from agents import Runner
from agent import agent
import logger


async def chat(message):

    #log the user query and agent name

    logger.info(f"USER QUERY: {message}")
    logger.info(f"AGENT: {agent.name}")

    result = await Runner.run(agent, message)

    logger.info(f"FINAL RESPONSE: {result.final_output}")
    
    return result.final_output


demo = gr.Interface(
    fn=chat,
    inputs=gr.Textbox(
        label="Write your prompt here"
    ),
    outputs=gr.Textbox(
        label="Answer"
    ),
    title="AI Research Assistant",
    description="Ask a question and let the agent find the answer.",
)

demo.launch()