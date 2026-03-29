import requests
import json
import os

class LLMClient:
    @staticmethod
    def ask(prompt, model, num_predict=500):
        url = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
        temperature = float(os.getenv("TEMPERATURE", "0.7"))
        timeout = int(os.getenv("TIMEOUT", "60"))
        
        payload = {
            "model": model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": temperature,
                "num_predict": num_predict
            }
        }
        
        try:
            response = requests.post(url, json=payload, timeout=timeout)
            if response.status_code != 200:
                return None
            result = response.json()
            return result.get("response", "")
        except Exception:
            return None
    
    @staticmethod
    def extract_json(text):
        if not text:
            return None
        
        start = text.find('{')
        end = text.rfind('}') + 1
        if start == -1 or end == 0:
            return None
        
        json_str = text[start:end]
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            return None