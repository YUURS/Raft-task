import json
import os
from datetime import datetime

class FileHandler:
    OUTPUT_DIR = "outputs"
    
    @classmethod
    def ensure_output_dir(cls):
        if not os.path.exists(cls.OUTPUT_DIR):
            os.makedirs(cls.OUTPUT_DIR)
    
    @classmethod
    def save_report(cls, data, role):
        cls.ensure_output_dir()
        filename = f"report_{role.replace(' ', '_')}.json"
        filepath = os.path.join(cls.OUTPUT_DIR, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
    @classmethod
    def save_markdown(cls, data, role):
        cls.ensure_output_dir()
        filename = f"report_{role.replace(' ', '_')}.md"
        filepath = os.path.join(cls.OUTPUT_DIR, filename)
        
        md_content = cls._generate_markdown(data, role)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(md_content)
    
    @classmethod
    def _generate_markdown(cls, data, role):
        md = f"# Анализ роли: {role}\n\n"
        md += f"*Дата генерации: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n"
        
        if "quality_score" in data:
            score = data["quality_score"].get("score", "N/A")
            md += f"## Качество отчета\n\n"
            md += f"- **Оценка качества**: {score}/100\n"
            md += f"- **Обоснование**: {data['quality_score'].get('justification', 'N/A')}\n"
            md += f"- **Согласованность**: {'Да' if data.get('is_consistent') else '❌ Нет'}\n"
            if data.get("warnings"):
                md += f"- **Предупреждения**:\n"
                for warning in data["warnings"]:
                    md += f"  - {warning}\n"
            md += "\n"
        
        if "skill_map" in data:
            md += f"## Карта навыков\n\n"
            for category, skills in data["skill_map"].items():
                if skills:
                    md += f"**{category.replace('_', ' ').title()}**: {', '.join(skills)}\n\n"
        
        if "salary_table" in data:
            md += f"## Зарплатная таблица (тыс. руб./USD)\n\n"
            md += "| Грейд | Москва | Регионы РФ | Remote USD |\n"
            md += "|-------|--------|------------|-----------|\n"
            for grade, regions in data["salary_table"].items():
                moscow = regions.get("Москва", {})
                regions_rf = regions.get("Регионы РФ", {})
                remote = regions.get("Remote USD", {})
                moscow_str = f"{moscow.get('min', '-')}/{moscow.get('median', '-')}/{moscow.get('max', '-')}"
                regions_str = f"{regions_rf.get('min', '-')}/{regions_rf.get('median', '-')}/{regions_rf.get('max', '-')}"
                remote_str = f"{remote.get('min', '-')}/{remote.get('median', '-')}/{remote.get('max', '-')}"
                md += f"| {grade} | {moscow_str} | {regions_str} | {remote_str} |\n"
            md += "\n"
        
        if "market_trend" in data:
            md += f"## Рыночный тренд\n\n"
            md += f"**Тренд**: {data['market_trend'].get('trend', 'N/A').upper()}\n\n"
            md += f"**Обоснование**: {data['market_trend'].get('justification', 'N/A')}\n\n"
        
        if "top_employers" in data:
            md += f"## Топ-работодатели\n\n"
            for employer in data["top_employers"]:
                md += f"- {employer}\n"
            md += "\n"
        
        if "learning_path" in data:
            md += f"## План обучения\n\n"
            for phase_key, phase in data["learning_path"].items():
                phase_name = phase_key.replace("phase_", "").replace("_", " ").title()
                md += f"### {phase_name} ({phase.get('days', 'N/A')} дней)\n\n"
                md += f"**Темы**: {', '.join(phase.get('topics', []))}\n\n"
                md += f"**Ресурсы**:\n"
                for resource in phase.get("resources", []):
                    md += f"- {resource.get('name', 'N/A')} ({resource.get('type', 'N/A')})\n"
                md += f"\n**Milestone**: {phase.get('milestone', 'N/A')}\n\n"
        
        if "gap_analysis" in data:
            md += f"## Карьерный совет\n\n"
            md += f"### Быстрые решения (2-4 недели)\n\n"
            for item in data["gap_analysis"].get("quick_wins", []):
                md += f"- **{item.get('skill', 'N/A')}**: {item.get('action', 'N/A')} ({item.get('timeframe', 'N/A')})\n"
            md += f"\n### Долгосрочное развитие (3+ месяцев)\n\n"
            for item in data["gap_analysis"].get("long_term", []):
                md += f"- **{item.get('skill', 'N/A')}**: {item.get('action', 'N/A')} ({item.get('timeframe', 'N/A')})\n"
            md += "\n"
        
        if "portfolio_project" in data:
            md += f"## Портфельный проект\n\n"
            md += f"**Название**: {data['portfolio_project'].get('name', 'N/A')}\n\n"
            md += f"**Описание**: {data['portfolio_project'].get('description', 'N/A')}\n\n"
            md += f"**Технологии**: {', '.join(data['portfolio_project'].get('technologies', []))}\n\n"
        
        return md