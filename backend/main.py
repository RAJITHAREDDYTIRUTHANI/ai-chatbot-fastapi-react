from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ✅ Use correct frontend URL without trailing slash
origins = [
    "http://localhost:3000",
    "https://ai-chatbot-fastapi-react.vercel.app",
    "https://ai-chatbot-fastapi-git-e6d24a-trajithareddy9121-5842s-projects.vercel.app"  # this is the exact one throwing error
]


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    

)

# ✅ Environment variable for Together API key
TOGETHER_API_KEY = os.getenv("TOGETHER_API_KEY")
if not TOGETHER_API_KEY:
    raise ValueError("TOGETHER_API_KEY not found in environment.")

MODEL = "mistralai/Mistral-7B-Instruct-v0.1"

@app.post("/chat")
async def chat(request: Request):
    try:
        data = await request.json()
        user_input = data.get("message", "")

        response = requests.post(
            "https://api.together.xyz/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {TOGETHER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": user_input}
                ]
            }
        )

        if response.status_code == 200:
            reply = response.json()["choices"][0]["message"]["content"]
            return {"response": reply.strip()}
        else:
            print("API Error:", response.text)
            return {"response": "Sorry, something went wrong."}
    except Exception as e:
        print("Exception occurred:", str(e))
        return {"response": "Server error occurred."}
