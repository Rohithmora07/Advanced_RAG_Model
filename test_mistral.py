from mistralai.client import Mistral
import os
from dotenv import load_dotenv

load_dotenv()

client = Mistral(
    api_key=os.getenv("MISTRAL_API_KEY")
)

response = client.chat.complete(
    model="mistral-small-latest",
    messages=[
        {
            "role": "user",
            "content": "What is RAG?"
        }
    ]
)

print(response.choices[0].message.content)