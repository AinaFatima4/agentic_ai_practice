import gradio as gr
from agents import Runner
from agent import agent


async def chat(message):
    result = await Runner.run(agent, message)
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