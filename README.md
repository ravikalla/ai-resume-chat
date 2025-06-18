# Resume AI Chatbot

A personal AI chatbot that represents Ravi Kalla's professional profile through an interactive web interface.

## Setup

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Configure environment variables:**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your API keys:
   - `OPENAI_API_KEY` - Your OpenAI API key
   - `PUSHOVER_TOKEN` - Your Pushover app token (for notifications)
   - `PUSHOVER_USER` - Your Pushover user key

3. **Run the application:**
   ```bash
   cd agent && python app.py
   ```

4. **Access the web interface:**
   Open your browser to the URL displayed in the terminal (typically `http://127.0.0.1:7860`)

## Features

- AI-powered chat interface using OpenAI GPT-4o-mini
- Automatic contact information recording
- Real-time notifications via Pushover
- PDF-based LinkedIn profile integration
- Professional representation for career inquiries