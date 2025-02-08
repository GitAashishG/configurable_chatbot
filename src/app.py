import chainlit as cl
import requests
from dotenv import load_dotenv
import os
from typing import List
from pydantic import BaseModel

load_dotenv()


class CopilotRequest(BaseModel):
    role: str = "user"
    content: str


@cl.on_chat_start
async def main():
    initial_endpoint = os.getenv(
        "LLM_ENDPOINT", "http://localhost:8000/api/v1/chat"
    )  # Default from .env
    cl.user_session.set("endpoint", initial_endpoint)  # Store in session
    cl.user_session.set("conversation_history", [])  # Initialize history

    await cl.Message(
        content=f"Welcome! Using LLM endpoint: {initial_endpoint}. To change the endpoint, type `/set_endpoint <URL>`"
    ).send()


@cl.on_message
async def main(message: cl.Message):
    # Check for the /set_endpoint command *first*
    if message.content.startswith("/set_endpoint"):
        try:
            new_endpoint = message.content.split(" ", 1)[1]  # Extract URL after command
            cl.user_session.set("endpoint", new_endpoint)  # Update endpoint in session
            await cl.Message(content=f"LLM endpoint updated to: {new_endpoint}").send()
        except IndexError:
            await cl.Message(
                content="Usage: /set_endpoint <URL>", author="System"
            ).send()  # Help message
        return  # Important: Stop processing this message as a regular chat message

    # If it's not the /set_endpoint command, process it as a regular message
    endpoint = cl.user_session.get("endpoint")
    conversation_history = cl.user_session.get("conversation_history")

    if not endpoint:  # Handle case where endpoint is not set (shouldn't happen)
        await cl.Message(
            content="LLM Endpoint not configured.  Use /set_endpoint <URL>",
            author="System",
        ).send()
        return

    try:
        user_message = CopilotRequest(role="user", content=message.content)
        conversation_history.append(user_message)
        messages_to_send = conversation_history[-4:]

        response = requests.post(
            endpoint,
            json=[msg.dict() for msg in messages_to_send],
            timeout=30,
        )

        if response.status_code == 200:
            response_data = response.json()
            bot_message = response_data.get("content", "")

            assistant_message = CopilotRequest(role="assistant", content=bot_message)
            conversation_history.append(assistant_message)
            cl.user_session.set("conversation_history", conversation_history)

            await cl.Message(content=bot_message).send()
        else:
            error_msg = (
                f"Error: Received status code {response.status_code} from the endpoint"
            )
            if response.text:
                error_msg += f"\nDetails: {response.text}"
            await cl.Message(content=error_msg, author="System").send()

    except requests.exceptions.RequestException as e:
        await cl.Message(
            content=f"Error connecting to the endpoint: {str(e)}", author="System"
        ).send()
