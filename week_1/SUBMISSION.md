# Week 1 Submission

## Overview

I built a terminal-based chatbot using the OpenRouter API and the OpenAI Python SDK. The chatbot maintains conversation history across turns by storing messages in a list and resending the full conversation history on every API call.

## Key Decisions

### API Key Management

I stored the API key in a `.env` file and loaded it using `python-dotenv`. The `.env` file was added to `.gitignore` to prevent accidental commits.

### ChatAgent Class

I implemented the chatbot as a `ChatAgent` class which keept the conversation state, model configuration, and API logic organized in a single object.

### Conversation State

The chatbot stores messages using the standard chat template format:

* system
* user
* assistant

The full message history is sent on every request because the API itself is stateless.

### Model Selection

The user can choose from multiple OpenRouter models before starting the conversation. This makes the chatbot model-agnostic.

### Rolling Buffer

I implemented a rolling buffer with a configurable maximum number of turns. When the limit is reached, the oldest user-assistant message pair is removed. This prevents the conversation history from growing indefinitely.

### Additional Commands

* `exit` / `quit` ends the chat session.
* `/reset` clears conversation history.
* `/tokens` displays token usage information from the most recent API call.

## What I Learnt

The main lesson was understanding that LLM APIs are stateless. The chatbot remembers information only because the conversation history is maintained and resent with every request.
