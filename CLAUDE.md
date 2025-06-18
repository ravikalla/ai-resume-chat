# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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

1. User interacts with Gradio chat interface
2. Messages processed through OpenAI GPT-4o-mini with system context from LinkedIn PDF and summary
3. AI can call tools to record user details or unknown questions
4. Tool calls trigger Pushover notifications
5. Conversation continues with tool results included in context