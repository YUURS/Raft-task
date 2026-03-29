import json
from .base_agent import BaseAgent
from utils.llm_client import LLMClient

class SalaryAgent(BaseAgent):
    def execute(self, role, skill_map):
        skill_map_json = json.dumps(skill_map, ensure_ascii=False, indent=2)
        
        prompt = f"""Ты — эксперт по рынку труда в IT.

На основе следующих данных:
Роль: {role}
Карта навыков: {skill_map_json}

Задача: Верни JSON с данными о зарплатах, трендах и топ-работодателях для этой специальности.

Формат ответа:
{{
  "salary_table": {{
    "Junior": {{
      "Москва": {{"min": число, "median": число, "max": число}},
      "Регионы РФ": {{"min": число, "median": число, "max": число}},
      "Remote USD": {{"min": число, "median": число, "max": число}}
    }},
    "Middle": {{ ... }},
    "Senior": {{ ... }},
    "Lead": {{ ... }}
  }},
  "market_trend": {{
    "trend": "growing" или "stable" или "declining",
    "justification": "краткое обоснование (1-2 предложения)"
  }},
  "top_employers": ["Компания1", "Компания2", "Компания3", "Компания4", "Компания5"]
}}

Важно:
- Все значения в тыс. руб. для Москвы и Регионов РФ.
- Для Remote USD значения в USD.
- Укажи реалистичные рыночные цифры на 2025–2026 год.
- Ответ должен содержать только JSON, без пояснений и дополнительного текста."""
        
        response = LLMClient.ask(prompt, self.model, num_predict=1500)
        return LLMClient.extract_json(response) or {}