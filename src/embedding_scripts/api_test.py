
import os 
import google.generativeai as genai
from dotenv import load_dotenv


load_dotenv()
GOOGLE_API_KEY = os.environ.get('GOOGLE_API_KEY')


try:
    genai.configure(api_key=GOOGLE_API_KEY)
    result = genai.embed_content(model='models/text-embedding-004',
                                 content=["test"],
                                 task_type="retrieval_document")
    print("Test API réussi:", result['embedding'])
except Exception as e:
    print("Erreur lors du test API simple:", e)
