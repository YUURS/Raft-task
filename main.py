import argparse
import os
from dotenv import load_dotenv

from agents.skill_agent import SkillAgent
from agents.salary_agent import SalaryAgent
from agents.learning_agent import LearningAgent
from agents.quality_agent import QualityAgent
from utils.file_handler import FileHandler

load_dotenv()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--role", required=True, help="Название специальности")
    parser.add_argument("--model", default=None, help="Название модели (переопределяет DEFAULT_MODEL)")
    args = parser.parse_args()
    
    model = args.model or os.getenv("DEFAULT_MODEL", "gemma3:4b")
    
    skill_agent = SkillAgent(model)
    salary_agent = SalaryAgent(model)
    learning_agent = LearningAgent(model)
    quality_agent = QualityAgent(model)
    
    skill_map = skill_agent.execute(args.role)
    
    salary_data = salary_agent.execute(args.role, skill_map)
    salary_table = salary_data.get("salary_table", {}) if salary_data else {}
    
    learning_data = learning_agent.execute(args.role, skill_map, salary_table)
    
    full_report = {
        "role": args.role,
        "skill_map": skill_map
    }
    if salary_data:
        full_report.update(salary_data)
    if learning_data:
        full_report.update(learning_data)
    
    quality_data = quality_agent.execute(full_report)
    if quality_data:
        full_report.update(quality_data)
    
    FileHandler.save_report(full_report, args.role)
    FileHandler.save_markdown(full_report, args.role)
    
    print(f"Результат сохранён в outputs/report_{args.role.replace(' ', '_')}.json")
    print(f"Markdown сохранён в outputs/report_{args.role.replace(' ', '_')}.md")

if __name__ == "__main__":
    main()