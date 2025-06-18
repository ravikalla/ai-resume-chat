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
required_env_vars = ["OPENAI_API_KEY"]
optional_env_vars = ["PUSHOVER_TOKEN", "PUSHOVER_USER"]

missing_required = [var for var in required_env_vars if not os.getenv(var)]
missing_optional = [var for var in optional_env_vars if not os.getenv(var)]

if missing_required:
    print(f"Error: Missing required environment variables: {', '.join(missing_required)}")
    print("Please set your OPENAI_API_KEY in the Hugging Face Spaces settings.")
    sys.exit(1)

if missing_optional:
    print(f"Warning: Optional environment variables not set: {', '.join(missing_optional)}")
    print("Pushover notifications will be disabled.")

def push(text):
    # Check if Pushover credentials are available
    if not os.getenv("PUSHOVER_TOKEN") or not os.getenv("PUSHOVER_USER"):
        print(f"Notification (would send via Pushover): {text}")
        return
    
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
        print(f"Pushover notification sent: {text}")
    except requests.exceptions.RequestException as e:
        print(f"Failed to send Pushover notification: {e}")


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
        try:
            messages = [{"role": "system", "content": self.system_prompt()}] + history + [{"role": "user", "content": message}]
            print(f"Chat request - Message: {message[:50]}...", flush=True)
            print(f"History length: {len(history)}", flush=True)
            
            done = False
            while not done:
                response = self.openai.chat.completions.create(model="gpt-4o-mini", messages=messages, tools=tools)
                if response.choices[0].finish_reason=="tool_calls":
                    message_obj = response.choices[0].message
                    tool_calls = message_obj.tool_calls
                    results = self.handle_tool_call(tool_calls)
                    messages.append(message_obj)
                    messages.extend(results)
                else:
                    done = True
            
            print("Chat response generated successfully", flush=True)
            return response.choices[0].message.content
            
        except Exception as e:
            print(f"Error in chat method: {e}", flush=True)
            return "I apologize, but I'm having trouble processing your request right now. Please try again."
    

if __name__ == "__main__":
    me = Me()
    
    # Suggested questions
    suggested_questions = [
        "What is your background in software engineering and data science?",
        "Tell me about your management experience",
        "What technologies and programming languages do you work with?",
        "What kind of projects have you worked on?",
        "Are you available for consulting or full-time opportunities?",
        "What is your experience with team leadership?",
        "Tell me about your data science expertise"
    ]
    
    def chat_fn(message, history):
        # Convert Gradio history format to OpenAI messages format
        messages = []
        if history:
            for entry in history:
                if isinstance(entry, dict) and "role" in entry and "content" in entry:
                    # Proper OpenAI format with role/content
                    messages.append(entry)
                elif isinstance(entry, list) and len(entry) >= 2:
                    # Gradio format [user_msg, assistant_msg]
                    if entry[0] and entry[0].strip():  # User message
                        messages.append({"role": "user", "content": str(entry[0])})
                    if entry[1] and entry[1].strip():  # Assistant message
                        messages.append({"role": "assistant", "content": str(entry[1])})
        
        try:
            print(f"Converting history with {len(history) if history else 0} entries to {len(messages)} messages", flush=True)
            response = me.chat(message, messages)
            return response
        except Exception as e:
            print(f"Error in chat_fn: {e}", flush=True)
            return f"I apologize, but I encountered an error. Please try again or ask a different question."
    
    # Create interface with custom CSS to change "Examples" to "You can ask..."
    css = """
    /* Target Examples heading and hide it */
    .examples h3,
    .examples-container h3,
    [data-testid*="examples"] h3,
    .chatbot .examples h3 {
        display: none !important;
    }
    
    /* Add custom "You can ask..." heading */
    .examples::before,
    .examples-container::before,
    [data-testid*="examples"]::before {
        content: "You can ask...";
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 0.75rem;
        display: block;
        color: #374151;
    }
    """
    
    interface = gr.ChatInterface(
        fn=chat_fn,
        title="💬 Chat with Ravi Kalla",
        description="Ask me anything about my professional background, experience, and skills!",
        examples=suggested_questions,
        theme=gr.themes.Soft(),
        retry_btn=None,
        undo_btn=None,
        clear_btn="Clear",
        css=css,
        textbox=gr.Textbox(placeholder="Ask about Ravi Kalla...", container=False, scale=7),
        js="""
        function() {
            setTimeout(function() {
                // Change Examples heading to "You can ask..."
                const headings = document.querySelectorAll('h3');
                headings.forEach(h => {
                    if (h.textContent && h.textContent.trim() === 'Examples') {
                        h.textContent = 'You can ask...';
                    }
                });
                
                // Auto-submit when example is clicked
                const exampleButtons = document.querySelectorAll('.examples button, [data-testid*="examples"] button');
                exampleButtons.forEach(button => {
                    button.addEventListener('click', function() {
                        setTimeout(function() {
                            const submitButton = document.querySelector('button[data-testid="submit-button"], .submit-btn, button[type="submit"]');
                            if (submitButton && !submitButton.disabled) {
                                submitButton.click();
                            }
                        }, 100);
                    });
                });
            }, 500);
        }
        """
    )
    
    # Launch with appropriate settings for Hugging Face Spaces
    # In production (Hugging Face), use specific port. In development, let Gradio choose.
    port = int(os.getenv("GRADIO_SERVER_PORT", 7860))
    
    interface.launch(
        server_name="0.0.0.0",
        server_port=port if os.getenv("SPACE_ID") else None,  # Only use fixed port in HF Spaces
        share=False,
        show_error=True
    )
    