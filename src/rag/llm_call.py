import os
from google import genai
from google.genai import types
from dotenv import load_dotenv
load_dotenv()


google_api_key = os.environ.get("GOOGLE_API_KEY")

client = genai.Client(api_key=google_api_key)

response = client.models.generate_content(
    model="gemini-2.0-flash", contents="Explain how AI works in a few words"
)
print(response.text)


result = client.models.embed_content(
        model="gemini-embedding-exp-03-07",
        contents="What is the meaning of life?",
        config=types.EmbedContentConfig(task_type="SEMANTIC_SIMILARITY")
)
print(result.embeddings)