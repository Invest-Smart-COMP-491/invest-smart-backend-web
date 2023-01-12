import requests
from scrape.api_keys import HUGGING_FACE_KEY
#from investsmart.scrape.api_keys import HUGGING_FACE_KEY

API_TOKEN = HUGGING_FACE_KEY # organization token
API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_TOKEN}"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class Summarizer:
    def __init__(self):
        pass

    def summarize_news(self, text):
        output = query({
            "inputs": text
        })

        return output[0]['summary_text']
