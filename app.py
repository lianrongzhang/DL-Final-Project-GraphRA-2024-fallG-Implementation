import chainlit as cl
import subprocess
import shlex
import asyncio

# Default list of suggested questions
SUGGESTED_QUERIES = [
    "What is the weather today?",
    "Can you summarize the latest news?",
    "How to install Python on Windows?",
    "Explain the concept of machine learning.",
    "What are the benefits of regular exercise?"
]

# Default query method
DEFAULT_METHOD = "local"

@cl.on_chat_start
async def start():
    """
    Generate the initial message, display suggested questions, and set the default query method.
    """
    cl.user_session.set("history", [])
    cl.user_session.set("query_method", DEFAULT_METHOD)

    # Add a button for toggling query methods
    actions = [
        cl.Action(
            name="toggle_search_method",
            value="toggle",
            description="Toggle between Local and Global search",
            label="Switch Search Method"
        )
    ]

@cl.set_starters
async def set_starters():
    return [
        cl.Starter(
            label="GraphRAG use case ideation",
            message="Can you help me brainstorm use cases for GraphRAG in different industries? Start by asking me about my interests or specific fields where this could be impactful.",
            icon="/public/lightbulb.svg",
        ),
        cl.Starter(
            label="Explain GraphRAG concepts",
            message="Explain GraphRAG and how it combines graph databases with retrieval-augmented generation in simple terms.",
            icon="/public/explain.svg",
        ),
        cl.Starter(
            label="Automate GraphRAG setup",
            message="Write a script to automate the setup of a GraphRAG system, including connecting a graph database and configuring a generative AI model. Walk me through the key steps.",
            icon="/public/summerize.svg",
        ),
        cl.Starter(
            label="Inviting collaborators",
            message="Write a message inviting a colleague to collaborate on a GraphRAG project. Keep it concise and mention the potential benefits of using GraphRAG for our data analysis workflow.",
            icon="/public/write.svg",
        )
    ]

@cl.action_callback("toggle_search_method")
async def toggle_search_method(action: cl.Action):
    """
    Toggle the query method between Local and Global.
    """
    current_method = cl.user_session.get("query_method", DEFAULT_METHOD)
    new_method = "global" if current_method == "local" else "local"
    cl.user_session.set("query_method", new_method)
    await cl.Message(content=f"Switched to {new_method} search.").send()

@cl.on_message
async def main(message: cl.Message):
    """
    Handle user messages, execute a command-line query, and return the results step by step.
    """
    history = cl.user_session.get("history", [])
    query_method = cl.user_session.get("query_method", DEFAULT_METHOD)
    query = message.content

    # Construct the command-line query
    cmd = [
        "python", "-m", "graphrag.query",
        "--root", "./ragtest",
        "--method", query_method,
        shlex.quote(query)
    ]

    # Create a "processing" message
    thinking_message = await cl.Message(content="").send()
    await thinking_message.stream_token(" ")
    try:
        # Execute the command and capture the output
        process = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode != 0:
            raise RuntimeError(f"Error executing command: {stderr.decode('utf-8').strip()}")

        output = stdout.decode("utf-8")
        response = output.split("SUCCESS: Local Search Response:", 1)[-1].strip()

        # Update the "processing" message and display the response gradually
        display_response = ""
        for char in response:
            display_response += char
            await thinking_message.stream_token(char)
            await asyncio.sleep(0.001)  # Adjust delay for gradual character-by-character display

        # Update the chat history
        history.append({"role": "user", "content": query})
        history.append({"role": "assistant", "content": display_response.strip()})
        cl.user_session.set("history", history)

        thinking_message.content = display_response.strip()
        await thinking_message.update()

        # Add the toggle button after each response
        actions = [
            cl.Action(
                name="toggle_search_method",
                value="toggle",
                description="Toggle between Local and Global search",
                label="Switch Search Method"
            )
        ]
        await cl.Message(content="You can switch search methods using the button below:", actions=actions).send()

    except Exception as e:
        error_message = f"An error occurred: {str(e)}"
        await cl.Message(content=error_message).send()

if __name__ == "__main__":
    cl.run()
