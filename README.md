---
title: Chat with Ravi Kalla
emoji: 💬
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.1
app_file: agent/app.py
pinned: false
license: mit
---

# Chat with Ravi Kalla - AI Resume Assistant

An AI-powered chatbot that represents Ravi Kalla's professional profile. Ask questions about his software engineering background, data science experience, management skills, and career journey.

## Features

- **Interactive Chat Interface** - Natural conversation about professional experience
- **Suggested Questions** - Quick-start questions to explore different aspects of Ravi's background
- **Real-time Responses** - Powered by OpenAI GPT-4o-mini for intelligent conversations
- **Professional Focus** - Tailored for career discussions and networking

## Usage

Simply start a conversation by:
1. Clicking one of the suggested questions, or
2. Typing your own question about Ravi's professional background

## Tech Stack

- **Frontend**: Gradio 4.44.1
- **AI Model**: OpenAI GPT-4o-mini
- **Backend**: Python with OpenAI API integration
- **Data Sources**: LinkedIn profile and professional summary

## Environment Variables

The following environment variables need to be set in Hugging Face Spaces:

- `OPENAI_API_KEY` - Your OpenAI API key
- `PUSHOVER_TOKEN` - Pushover app token (for notifications)
- `PUSHOVER_USER` - Pushover user key (for notifications)

## Contact

This AI assistant can help connect you with Ravi Kalla for professional opportunities and collaboration.