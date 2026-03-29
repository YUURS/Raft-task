import json
from .base_agent import BaseAgent
from utils.llm_client import LLMClient

class LearningAgent(BaseAgent):
    def execute(self, role, skill_map, salary_table):
        skill_map_json = json.dumps(skill_map, ensure_ascii=False, indent=2)
        salary_table_json = json.dumps(salary_table, ensure_ascii=False, indent=2)
        
        prompt = f"""Ты — эксперт по IT-образованию и карьерному развитию.

На основе следующих данных:
Роль: {role}
Карта навыков: {skill_map_json}
Зарплатная таблица по грейдам: {salary_table_json}

Задача: Верни JSON с планом обучения, анализом пробелов и портфельным проектом.

Формат ответа:
{{
  "learning_path": {{
    "phase_1_foundation": {{
      "days": 30,
      "topics": ["тема1", "тема2", "тема3"],
      "resources": [
        {{"name": "Название ресурса", "type": "курс/книга/документация"}},
        {{"name": "Название ресурса", "type": "курс/книга/документация"}}
      ],
      "milestone": "ожидаемый результат"
    }},
    "phase_2_practice": {{
      "days": 30,
      "topics": ["тема1", "тема2", "тема3"],
      "resources": [
        {{"name": "Название ресурса", "type": "курс/книга/документация"}},
        {{"name": "Название ресурса", "type": "курс/книга/документация"}}
      ],
      "milestone": "ожидаемый результат"
    }},
    "phase_3_portfolio": {{
      "days": 30,
      "topics": ["тема1", "тема2", "тема3"],
      "resources": [
        {{"name": "Название ресурса", "type": "курс/книга/документация"}},
        {{"name": "Название ресурса", "type": "курс/книга/документация"}}
      ],
      "milestone": "ожидаемый результат"
    }}
  }},
  "gap_analysis": {{
    "quick_wins": [
      {{"skill": "навык", "timeframe": "2-4 недели", "action": "конкретное действие"}}
    ],
    "long_term": [
      {{"skill": "навык", "timeframe": "3+ месяцев", "action": "конкретное действие"}}
    ]
  }},
  "portfolio_project": {{
    "name": "Название проекта",
    "description": "Описание проекта, что делает и какую проблему решает",
    "technologies": ["технология1", "технология2", "технология3"]
  }}
}}

Важно:
- Ресурсы должны быть реальными и актуальными.
- Milestone должен быть конкретным и измеримым.
- Quick wins — навыки, которые можно быстро освоить на основе уже имеющихся.
- Long term — фундаментальные навыки, требующие длительного изучения.
- Портфельный проект должен демонстрировать ключевые навыки для Junior уровня.
- Ответ должен содержать только JSON, без пояснений и дополнительного текста."""
        
        response = LLMClient.ask(prompt, self.model, num_predict=2000)
        return LLMClient.extract_json(response) or {}