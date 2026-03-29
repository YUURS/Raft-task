import json
from .base_agent import BaseAgent
from utils.llm_client import LLMClient

class QualityAgent(BaseAgent):
    def execute(self, full_report):
        full_report_json = json.dumps(full_report, ensure_ascii=False, indent=2)
        
        prompt = f"""Ты — эксперт по качеству аналитических IT-отчетов.

Проверь следующий отчет на согласованность и качество:
{full_report_json}

Задача: Верни JSON с оценкой качества, предупреждениями и вердиктом о согласованности.

Формат ответа:
{{
  "quality_score": {{
    "score": целое_число_от_0_до_100,
    "justification": "обоснование оценки в 1-2 предложения"
  }},
  "warnings": [
    "предупреждение 1",
    "предупреждение 2"
  ],
  "is_consistent": true_или_false
}}

Правила проверки:
1. Проверь соответствие зарплат уровню навыков (Junior зарплаты должны быть ниже Middle и т.д.)
2. Найди противоречия: если market_trend.trend = "declining" для технологии, но эта технология активно используется в learning_path или portfolio_project — добавь warning
3. Проверь, что технологии из portfolio_project присутствуют в skill_map или learning_path
4. Проверь, что ресурсы в learning_path реалистичны и соответствуют темам
5. quality_score выставляй на основе:
   - Согласованность данных (30%)
   - Реалистичность зарплат и трендов (30%)
   - Логичность learning_path (20%)
   - Качество gap_analysis (20%)
6. is_consistent = True только если нет критических противоречий и score >= 70

Ответ должен содержать только JSON, без пояснений и дополнительного текста."""
        
        response = LLMClient.ask(prompt, self.model, num_predict=1500)
        return LLMClient.extract_json(response) or {}