# study_planner_agent.py
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re


load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# 1. Initialize the Gemini model
model = genai.GenerativeModel('gemini-2.0-flash')

# 2. Input Understanding Layer
def input_understanding(user_input):
    system_prompt = """
    You are an intelligent input analyzer for a Study Planner AI Agent.
    Understand what the student is asking — for example:
    - Are they requesting a study schedule?
    - Are they asking how to revise?
    - Are they requesting subject-specific guidance?
    Return a structured analysis in JSON with fields:
    {"intent": "", "subject": "", "timeframe": "", "custom_notes": ""}
    """
    response = model.generate_content(f"{system_prompt}\n\nUser: {user_input}")
    return response.text


# 3. State Tracker Layer
class StateTracker:
    def __init__(self):
        self.state = {}

    def extract_json(self, text):
        # Remove code block markdown if present (``````)
        match = re.search(r'\{.*\}', text, re.DOTALL)
        if match:
            json_str = match.group(0)
            try:
                return json.loads(json_str)
            except json.JSONDecodeError:
                return {}
        else:
            return {}

    def update_state(self, analysis_text):
        analysis_json = self.extract_json(analysis_text)
        self.state.update(analysis_json)
        return self.state

    def get_state(self):
        return self.state


# 4. Task Planning Layer
def plan_study_task(state):
    plan_prompt = f"""
    You are the task planner for a study revision assistant. Based on the student's context below:
    {state}

    Plan the optimal step-by-step study plan for the next 7 days.
    Each day should include subject focus, time allocation, and revision tips.
    """
    response = model.generate_content(plan_prompt)
    return response.text


# 5. Output Generator Layer
def output_generator(plan_text):
    output_prompt = f"""
    Format the following study plan in Markdown style.
    Use friendly, motivating language and include emojis for clarity.
    Here is the raw plan:
    {plan_text}
    """
    response = model.generate_content(output_prompt)
    return response.text


# 6. Master function to run the entire pipeline
def study_planner_agent(user_query):
    understanding = input_understanding(user_query)
    tracker = StateTracker()
    memory = tracker.update_state(understanding)
    plan = plan_study_task(memory)
    output = output_generator(plan)
    return output


# 7. Example Run
if __name__ == "__main__":
    query = input("Enter your study situation or request: ")
    response = study_planner_agent(query)
    print("\nFinal Study Plan:\n", response)
