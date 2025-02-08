# FlexiChat

A flexible chat interface built with Chainlit for testing and interacting with LLM endpoints.

## Features

- Interactive chat interface powered by Chainlit
- Configurable LLM endpoint
- Conversation history management
- Dynamic endpoint switching using commands
- Environment variable support

## Prerequisites

- Python 3.x
- Required Python packages:
  - chainlit
  - requests
  - python-dotenv
  - pydantic

## Setup

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install chainlit requests python-dotenv pydantic
   ```
3. Create a `.env` file with your default LLM endpoint:
   ```
   LLM_ENDPOINT=http://localhost:8000/api/v1/chat
   ```

## Usage

1. Start the application:

   ```bash
   chainlit run src/app.py
   ```

2. Access the chat interface through your web browser.

3. To change the LLM endpoint during runtime, use the command:
   ```
   /set_endpoint <URL>
   ```

## API Format

The application expects the LLM endpoint to:

- Accept POST requests with a JSON array of messages
- Each message should have `role` and `content` fields
- Return JSON response with a `content` field containing the LLM's reply

## Environment Variables

- `LLM_ENDPOINT`: Default LLM endpoint URL (can be overridden using /set_endpoint command)

## Features

- Maintains conversation history (last 4 messages)
- Error handling for endpoint connection issues
- System messages for configuration changes and errors
- Timeout handling for LLM requests (30 seconds)

## Project Structure

- `src/app.py`: Main application file containing the Chainlit chat interface
- `src/chainlit.md`: Chainlit configuration for welcome screen
- `src/chainlit.toml`: Chainlit configuration file
