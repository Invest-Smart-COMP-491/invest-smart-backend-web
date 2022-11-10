import requests

API_TOKEN = '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'  # organization token

API_URL = "https://api-inference.huggingface.co/models/facebook/bart-large-cnn"
headers = {"Authorization": f"Bearer {API_TOKEN}"}


def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()


class Summarizer:
    def __init__(self):
        pass

    def summarizeNews(self, text):
        output = query({
            "inputs": text
        })

        return output[0]['summary_text']
