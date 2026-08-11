# Agentic Knowledge Base Assistant

An agentic AI assistant built with the **OpenAI Agents SDK** that can answer user queries using its own reasoning, local knowledge-base files, and additional tools.

The application provides a simple **Gradio interface** where users can enter questions and receive responses from the agent.

## Features

* AI agent built using the OpenAI Agents SDK
* Local JSON/CSV knowledge-base search
* Calculator tool
* Current time tool
* Employee information lookup tool
* Agent-controlled tool selection
* Logging of:

  * User queries
  * Agent used
  * Tool selected
  * Tool input
  * Tool output
  * Final response
* Simple Gradio web interface
* Asynchronous agent execution

## Project Structure

```text
project/
│
├── app.py
├── agent.py
├── tools.py
├── logger.py
├── knowledge_base.json
├── agent.log
└── README.md
```

### `app.py`

Handles the user interface using Gradio.

It:

* Accepts the user's query
* Runs the agent
* Displays the final response
* Logs the user query and final response

### `agent.py`

Contains the main AI agent.

It defines:

* Agent name
* Agent instructions
* Available tools

The agent decides when to use a tool and when it can answer using its own reasoning.

### `tools.py`

Contains the tools available to the agent.

Current tools include:

* `calculator` — evaluates mathematical expressions
* `get_current_time` — returns the current date and time
* `get_employee_info` — retrieves information about an employee
* `search_knowledge_base` — searches the local JSON/CSV knowledge base for relevant information

### `logger.py`

Contains the Python logging configuration.

Logs are stored in:

```text
agent.log
```

### `knowledge_base.json`

The local knowledge base containing structured information that can be searched by the agent.

## How It Works

The application follows this general flow:

```text
User
 │
 │ Query
 ↓
Gradio Interface
 │
 ↓
Agent
 │
 ├───────────────┐
 │               │
 ↓               ↓
Own Reasoning   Tools
                 │
       ┌─────────┼──────────┐
       ↓         ↓          ↓
  Calculator   Employee   Knowledge
                Info       Base
       │         │          │
       └─────────┴──────────┘
                 │
                 ↓
              Agent
                 │
                 ↓
          Final Response
                 │
                 ↓
              Gradio
```

The agent determines whether it needs to use one of the available tools based on the user's request.

## Knowledge Base Search

The `search_knowledge_base` tool searches the local JSON/CSV knowledge base and returns relevant documents based on the user's query.

The knowledge base is searched locally rather than sending the entire document to the language model.

This allows the application to work with larger knowledge bases without putting the entire dataset into the model's context for every request.

## Logging

The application logs important information about each agent interaction.

Example:

```text
USER QUERY: What department does Ayesha work in?
AGENT: Knowledge Assistant
TOOL SELECTED: get_employee_info
TOOL INPUT: Ayesha
TOOL OUTPUT: Ayesha works in the Engineering department.
FINAL RESPONSE: Ayesha works in the Engineering department.
```

This makes it possible to inspect how the agent handled each request and which tools it used.

## Installation

Install the required packages:

```bash
pip install openai-agents gradio pydantic
```

If a `requirements.txt` file is provided, install the dependencies with:

```bash
pip install -r requirements.txt
```

## Environment Variables

The OpenAI API key should be stored as an environment variable.

### Windows

```bash
set OPENAI_API_KEY=your_api_key
```

### macOS/Linux

```bash
export OPENAI_API_KEY=your_api_key
```

Alternatively, a `.env` file can be used if the project is configured to load environment variables from it.

## Running the Application

Run:

```bash
python app.py
```

Gradio will start a local web server and provide a URL that can be opened in a browser.

## Example Queries

### Knowledge Base

```text
What is the company's refund policy?
```

```text
How long do customers have to request a refund?
```

### Employee Information

```text
What department does Ayesha Khan work in?
```

### Calculator

```text
Calculate 457 * 82
```

### Current Time

```text
What time is it?
```

## Technologies Used

* **Python**
* **OpenAI Agents SDK**
* **Gradio**
* **Pydantic**
* **JSON/CSV**
* **Python Logging**

## Design

The project separates the main responsibilities into different files:

```text
app.py
  → User interface

agent.py
  → Agent configuration and instructions

tools.py
  → Tool implementations

logger.py
  → Logging configuration

knowledge_base.json / CSV
  → Local knowledge source
```

This separation makes the application easier to maintain and allows individual tools or the knowledge-base search implementation to be modified without changing the rest of the application.
