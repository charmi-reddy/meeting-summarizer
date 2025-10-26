import os
import requests
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv("CEREBRAS_API_KEY")
if not API_KEY:
    raise ValueError("Missing CEREBRAS_API_KEY in .env. Add CEREBRAS_API_KEY=your_key_here")

# Use official Cerebras Cloud endpoint
API_URL = "https://api.cerebras.ai/v1/chat/completions"

def build_summary_prompt(transcript):
    return (
        "Summarize the following meeting transcript in approximately 500 tokens "
        "(you may go slightly over if needed to complete your summary coherently).\n\n"
        "Your summary should include:\n"
        "1. Main topics discussed – briefly list each topic covered.\n"
        "2. Key decisions made – specify who made each decision.\n"
        "3. Action items – include who is responsible, what needs to be done, and any deadlines.\n"
        "4. Important dates or deadlines – mention all time-bound events discussed.\n"
        "5. Open questions or unresolved issues – highlight anything still pending or undecided.\n\n"
        "Format clearly using section headings and bullet points.\n"
        "Ensure the response is complete, coherent, and does not end abruptly.\n"
        "Do not exceed approximately 600 tokens.\n"
        "If you reach the token limit, end your summary gracefully with a final sentence instead of cutting off mid-sentence.\n\n"
        f"Transcript:\n{transcript}"
    )


def call_cerebras(transcript, model="llama3.1-8b", max_tokens=500):
    prompt = build_summary_prompt(transcript)
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": max_tokens
    }
    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 401:
        raise PermissionError(
            "401 Unauthorized. Check that your Cerebras key is valid and active. "
            "Keys starting with 'csk-' should work on the official Cerebras endpoint."
        )
    response.raise_for_status()
    result = response.json()
    return result["choices"][0]["message"]["content"]