from dotenv import load_dotenv
from openai import OpenAI
import json
import os
import requests
from pypdf import PdfReader
import gradio as gr
import sys
from pathlib import Path


load_dotenv(override=True)

# Validate required environment variables
required_env_vars = ["OPENAI_API_KEY", "PUSHOVER_TOKEN", "PUSHOVER_USER"]
missing_vars = [var for var in required_env_vars if not os.getenv(var)]
if missing_vars:
    print(f"Error: Missing required environment variables: {', '.join(missing_vars)}")
    print("Please create a .env file based on .env.example and add your API keys.")
    sys.exit(1)

def push(text):
    try:
        response = requests.post(
            "https://api.pushover.net/1/messages.json",
            data={
                "token": os.getenv("PUSHOVER_TOKEN"),
                "user": os.getenv("PUSHOVER_USER"),
                "message": text,
            },
            timeout=10
        )
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"Failed to send notification: {e}")


def record_user_details(email, name="Name not provided", notes="not provided"):
    push(f"Recording {name} with email {email} and notes {notes}")
    return {"recorded": "ok"}

def record_unknown_question(question):
    push(f"Recording {question}")
    return {"recorded": "ok"}

record_user_details_json = {
    "name": "record_user_details",
    "description": "Use this tool to record that a user is interested in being in touch and provided an email address",
    "parameters": {
        "type": "object",
        "properties": {
            "email": {
                "type": "string",
                "description": "The email address of this user"
            },
            "name": {
                "type": "string",
                "description": "The user's name, if they provided it"
            }
            ,
            "notes": {
                "type": "string",
                "description": "Any additional information about the conversation that's worth recording to give context"
            }
        },
        "required": ["email"],
        "additionalProperties": False
    }
}

record_unknown_question_json = {
    "name": "record_unknown_question",
    "description": "Always use this tool to record any question that couldn't be answered as you didn't know the answer",
    "parameters": {
        "type": "object",
        "properties": {
            "question": {
                "type": "string",
                "description": "The question that couldn't be answered"
            },
        },
        "required": ["question"],
        "additionalProperties": False
    }
}

tools = [{"type": "function", "function": record_user_details_json},
        {"type": "function", "function": record_unknown_question_json}]


class Me:

    def __init__(self):
        self.openai = OpenAI()
        self.name = "Ravi Kalla"
        
        # Load LinkedIn PDF with error handling
        pdf_path = Path("me/linkedin.pdf")
        if not pdf_path.exists():
            print(f"Warning: LinkedIn PDF not found at {pdf_path}")
            self.linkedin = "LinkedIn profile not available"
        else:
            try:
                reader = PdfReader(pdf_path)
                self.linkedin = ""
                for page in reader.pages:
                    text = page.extract_text()
                    if text:
                        self.linkedin += text
            except Exception as e:
                print(f"Error reading LinkedIn PDF: {e}")
                self.linkedin = "Error loading LinkedIn profile"
        
        # Load summary with error handling
        summary_path = Path("me/summary.txt")
        if not summary_path.exists():
            print(f"Warning: Summary file not found at {summary_path}")
            self.summary = "Personal summary not available"
        else:
            try:
                with open(summary_path, "r", encoding="utf-8") as f:
                    self.summary = f.read()
            except Exception as e:
                print(f"Error reading summary file: {e}")
                self.summary = "Error loading personal summary"


    def handle_tool_call(self, tool_calls):
        results = []
        for tool_call in tool_calls:
            tool_name = tool_call.function.name
            arguments = json.loads(tool_call.function.arguments)
            print(f"Tool called: {tool_name}", flush=True)
            tool = globals().get(tool_name)
            result = tool(**arguments) if tool else {}
            results.append({"role": "tool","content": json.dumps(result),"tool_call_id": tool_call.id})
        return results
    
    def system_prompt(self):
        system_prompt = f"You are acting as {self.name}. You are answering questions on {self.name}'s website, \
particularly questions related to {self.name}'s career, background, skills and experience. \
Your responsibility is to represent {self.name} for interactions on the website as faithfully as possible. \
You are given a summary of {self.name}'s background and LinkedIn profile which you can use to answer questions. \
Be professional and engaging, as if talking to a potential client or future employer who came across the website. \
If you don't know the answer to any question, use your record_unknown_question tool to record the question that you couldn't answer, even if it's about something trivial or unrelated to career. \
If the user is engaging in discussion, try to steer them towards getting in touch via email; ask for their email and record it using your record_user_details tool. "

        system_prompt += f"\n\n## Summary:\n{self.summary}\n\n## LinkedIn Profile:\n{self.linkedin}\n\n"
        system_prompt += f"With this context, please chat with the user, always staying in character as {self.name}."
        return system_prompt
    
    def chat(self, message, history):
        messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
        done = False
        while not done:
            response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
            if response.choices[0].finish_reason=="tool_calls":
                message = response.choices[0].message
                tool_calls = message.tool_calls
                results = self.handle_tool_call(tool_calls)
                messages.append(message)
                messages.extend(results)
            else:
                done = True
        return response.choices[0].message.content
    

def create_interface():
    me = Me()
    
    # Recommended questions based on Ravi's profile
    recommended_questions = [
        "What is your background in software engineering and data science?",
        "Tell me about your management experience",
        "What technologies and programming languages do you work with?",
        "What kind of projects have you worked on?",
        "Are you available for consulting or full-time opportunities?",
        "What is your experience with team leadership?",
        "Tell me about your data science expertise"
    ]
    
    # Create the interface with custom components
    with gr.Blocks(title="Chat with Ravi Kalla", theme=gr.themes.Soft()) as interface:
        gr.Markdown("# 💬 Chat with Ravi Kalla")
        gr.Markdown("Ask me anything about my professional background, experience, and skills!")
        
        # Recommended questions section
        gr.Markdown("### 🔹 Suggested Questions")
        suggestion_buttons = []
        with gr.Row():
            with gr.Column():
                for question in recommended_questions[:4]:
                    btn = gr.Button(question, variant="secondary", size="sm")
                    suggestion_buttons.append(btn)
            with gr.Column():
                for question in recommended_questions[4:]:
                    btn = gr.Button(question, variant="secondary", size="sm")
                    suggestion_buttons.append(btn)
        
        # Chat interface
        chatbot = gr.Chatbot(type="messages", height=400)
        msg = gr.Textbox(placeholder="Type your question here...", 
                        label="Your Message", lines=2)
        
        def handle_message(message, history):
            if message.strip():
                response = me.chat(message, history)
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": response})
            return "", history
        
        def use_suggestion(question):
            return question
        
        # Set up event handlers
        msg.submit(handle_message, [msg, chatbot], [msg, chatbot])
        
        # Connect suggestion buttons to input textbox
        for btn, question in zip(suggestion_buttons, recommended_questions):
            btn.click(lambda q=question: q, outputs=msg)
    
    return interface

if __name__ == "__main__":
    interface = create_interface()
    interface.launch()
    