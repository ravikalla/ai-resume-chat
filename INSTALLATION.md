# Installation Guide - AI Resume Chat

This guide will help you set up and run the AI Resume Chat application locally or deploy it to Hugging Face Spaces.

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- OpenAI API key
- (Optional) Pushover account for notifications

## 🚀 Local Installation

### 1. Clone the Repository

```bash
git clone https://github.com/ravikalla/ai-resume-chat.git
cd ai-resume-chat
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `openai>=1.0.0`
- `gradio>=4.0.0`
- `pypdf>=3.0.0`
- `python-dotenv>=1.0.0`
- `requests>=2.31.0`

### 3. Set Up Environment Variables

Create a `.env` file in the root directory:

```bash
# Required
OPENAI_API_KEY=your_openai_api_key_here

# Optional (for notifications)
PUSHOVER_TOKEN=your_pushover_token
PUSHOVER_USER=your_pushover_user_key
```

### 4. Add Your Personal Data

1. **LinkedIn PDF**: Place your LinkedIn profile PDF in `me/linkedin.pdf`
2. **Summary**: Update `me/summary.txt` with your professional summary

### 5. Run the Application

```bash
python3 app.py
```

The application will start and display:
```
Running on local URL: http://0.0.0.0:7860
```

Open your browser and navigate to `http://localhost:7860`

## 🌐 Hugging Face Spaces Deployment

### 1. Create a Hugging Face Space

1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose:
   - **SDK**: Gradio
   - **Hardware**: CPU basic (free tier)
   - **Visibility**: Public or Private

### 2. Clone and Push Code

```bash
# Add Hugging Face remote
git remote add huggingface https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME

# Push code
git push huggingface main
```

### 3. Configure Environment Variables

In your Hugging Face Space:

1. Go to **Settings** → **Repository secrets**
2. Add the following variables:
   ```
   OPENAI_API_KEY = your_openai_api_key_here
   PUSHOVER_TOKEN = your_pushover_token (optional)
   PUSHOVER_USER = your_pushover_user_key (optional)
   ```

### 4. Upload Personal Data

1. Go to **Files and versions** in your Space
2. Upload your LinkedIn PDF to `me/linkedin.pdf`
3. Update `me/summary.txt` with your information

### 5. Access Your Space

Your application will be available at:
```
https://huggingface.co/spaces/YOUR_USERNAME/YOUR_SPACE_NAME
```

## 🔧 Configuration

### Personal Data Setup

1. **LinkedIn PDF**: 
   - Export your LinkedIn profile as PDF
   - Place in `me/linkedin.pdf`
   - Ensure the file is readable by the application

2. **Professional Summary**:
   - Edit `me/summary.txt`
   - Include key career highlights, skills, and experience
   - This text will be used by the AI for context

### Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `OPENAI_API_KEY` | ✅ Yes | Your OpenAI API key for GPT-4o-mini |
| `PUSHOVER_TOKEN` | ❌ Optional | Pushover app token for notifications |
| `PUSHOVER_USER` | ❌ Optional | Pushover user key for notifications |

### Customization

You can customize the application by modifying:

- **Suggested questions**: Edit the `suggested_questions` list in `app.py`
- **AI persona**: Modify the system prompt in the `system_prompt()` method
- **UI appearance**: Update the CSS styles or Gradio theme
- **Version number**: Change the version in the description field

## 🛠️ Troubleshooting

### Common Issues

**Port already in use:**
```bash
# Find and kill processes on port 7860
lsof -ti:7860 | xargs kill -9
```

**Missing dependencies:**
```bash
# Reinstall requirements
pip install -r requirements.txt --upgrade
```

**OpenAI API errors:**
- Verify your API key is correct
- Check your OpenAI account has sufficient credits
- Ensure the API key has the necessary permissions

**PDF not loading:**
- Verify the PDF file is named exactly `linkedin.pdf`
- Check the file is in the `me/` directory
- Ensure the PDF is not password protected

### Logs and Debugging

- Application logs are written to console output
- For Hugging Face Spaces, check the **Logs** tab in your Space
- Enable debug mode by setting environment variable: `GRADIO_DEBUG=1`

## 📁 Project Structure

```
ai-resume-chat/
├── app.py                 # Main application file
├── requirements.txt       # Python dependencies
├── README.md             # Hugging Face Space configuration
├── INSTALLATION.md       # This installation guide
├── CLAUDE.md            # Development instructions
├── me/                  # Personal data directory
│   ├── linkedin.pdf     # Your LinkedIn profile PDF
│   └── summary.txt      # Professional summary
└── .env                 # Environment variables (local only)
```

## 🔒 Security Notes

- Never commit your `.env` file to Git
- Keep your OpenAI API key secure
- For production deployment, use environment variables instead of `.env` files
- Regularly rotate your API keys

## 📞 Support

If you encounter issues:

1. Check the troubleshooting section above
2. Review the application logs
3. Verify all environment variables are set correctly
4. Ensure your OpenAI API key is valid and has credits

## 🎯 Next Steps

After successful installation:

1. Test the chat interface with suggested questions
2. Verify the auto-submit functionality works
3. Customize the suggested questions for your profile
4. Share your Space URL with potential employers or clients

---

*Happy chatting! 🚀*