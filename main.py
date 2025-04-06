from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
from bs4 import BeautifulSoup
import requests
import os
import traceback

# Load environment variables
load_dotenv()
api_key = os.getenv("TOGETHER_API_KEY")
print("🔑 TOGETHER_API_KEY loaded:", api_key)

if not api_key:
    raise Exception("❌ TOGETHER_API_KEY not found in .env!")

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model
class ChatRequest(BaseModel):
    question: str
    url: str

@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        print(f"🌐 Scraping website: {req.url}")
        website_response = requests.get(req.url, timeout=10)
        soup = BeautifulSoup(website_response.text, "html.parser")

        for tag in soup(["script", "style", "noscript", "img", "footer", "header", "nav"]):
            tag.decompose()

        website_content = soup.get_text(separator="\n", strip=True)
        website_content = "\n".join([line for line in website_content.splitlines() if len(line.strip()) > 30])

        prompt = f"Website Content:\n{website_content[:10000]}\n\nQuestion:\n{req.question}"

        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "mistralai/Mixtral-8x7B-Instruct-v0.1",
            "messages": [
                {"role": "system", "content": "You are a helpful assistant that answers user questions based only on the content of the given website."},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.7,
            "top_p": 0.7,
            "max_tokens": 512
        }

        response = requests.post("https://api.together.xyz/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()

        data = response.json()
        answer = data['choices'][0]['message']['content']
        return {"answer": answer.strip()}

    except Exception as e:
        print("❌ Exception occurred:", str(e))
        traceback.print_exc()
        return JSONResponse(
            status_code=500,
            content={"answer": f"⚠️ Backend Error: {str(e)}"}
        )

# 👇 This makes sure the server runs when deploying with Railway
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000)
