# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

You are acting as Ravi. You are answering questions on Ravi's website, particularly questions related to Ravi's career, background, skills and experience. Your responsibility is to represent Ravi for interactions on the website as faithfully as possible. You are given a summary of Ravi's background and LinkedIn profile which you can use to answer questions. Be professional and engaging, as if talking to a potential client or future employer who came across the website. If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. 

## Development Commands

**Run the application:**
```bash
cd agent && python app.py
```

**Install dependencies (create requirements.txt first):**
```bash
pip install openai gradio pypdf python-dotenv requests
```

## Project Architecture

This is a personal AI chatbot application that represents Ravi Kalla's professional profile. The application consists of:

- **Single-file Gradio web app** (`agent/app.py`) - Contains all application logic
- **Personal data files** (`agent/me/`) - LinkedIn PDF and summary text file
- **AI-powered chat interface** - Uses OpenAI GPT-4o-mini with custom tool calling

## Key Components

**Me Class (`app.py:76-133`)**:
- Loads LinkedIn PDF and summary text on initialization
- Handles OpenAI chat completions with tool calling capabilities
- Maintains conversation context and system prompts

**Tool Functions**:
- `record_user_details()` - Captures user contact information via Pushover notifications
- `record_unknown_question()` - Logs unanswered questions via Pushover notifications

**Environment Requirements**:
- `PUSHOVER_TOKEN` - Pushover app token for notifications
- `PUSHOVER_USER` - Pushover user key
- OpenAI API key (standard environment variable)

## Data Flow

1. Related questions(based on Ravi's profile) and the Gradio chat interface are shown on the UI.
2. User may click any related question shown to them or directly type in Gradio chat interface.
3. Messages processed through OpenAI GPT-4o-mini with system context from LinkedIn PDF and summary
4. AI can call tools to record user details or unknown questions
5. Tool calls trigger Pushover notifications
6. Conversation continues with tool results included in context