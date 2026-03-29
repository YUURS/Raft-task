import json
from .base_agent import BaseAgent
from utils.llm_client import LLMClient

class SkillAgent(BaseAgent):
    def execute(self, role):
        prompt = f"""Ты — эксперт по IT-рынку.

Задача: Верни JSON с картой навыков для специальности "{role}".

Твой ответ должен быть ТОЛЬКО JSON в таком формате:
{{
  "skill_map": {{
    "languages": ["1", "2", ..],
    "frameworks": ["1", "2", ..],
    "infrastructure": ["1", "2", ..],
    "soft_skills": ["1", "2", ..]
  }}
}}

Никаких пояснений, никакого текста до или после JSON. Только JSON."""
        
        response = LLMClient.ask(prompt, self.model, num_predict=500)
        data = LLMClient.extract_json(response)
        if data and "skill_map" in data:
            return data["skill_map"]
        return {}