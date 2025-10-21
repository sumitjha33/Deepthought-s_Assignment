
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json
import re

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

# 1. Input Understanding Layer
def input_understanding(user_input):
    system_prompt = """
    You are an input analyzer for a Mindfulness Prompt AI Agent.
    Understand if the user wants a general prompt, a prompt for a specific mood, or a type of mindfulness (e.g., gratitude, focus, calm).
    Return a JSON with fields: {"intent": "", "mood": "", "type": "", "custom_notes": ""}
    """
    response = model.generate_content(f"{system_prompt}\n\nUser: {user_input}")
    return response.text

# 2. State Tracker Layer
class StateTracker:
    def __init__(self):
        self.state = {}

    def extract_json(self, text):
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

# 3. Task Planning Layer
def plan_prompt(state):
    plan_prompt = f"""
    You are the task planner for a mindfulness prompt generator.
    Based on the user's context below:
    {state}

    Generate a single, actionable, and positive mindfulness prompt for today.
    If a mood or type is specified, tailor the prompt accordingly.
    """
    response = model.generate_content(plan_prompt)
    return response.text

# 4. Output Generator Layer
def output_generator(prompt_text):
    output_prompt = f"""
    Format the following mindfulness prompt in a friendly, encouraging tone.
    Add a short motivational message at the end.
    Here is the raw prompt:
    {prompt_text}
    """
    response = model.generate_content(output_prompt)
    return response.text

# 5. Master function to run the pipeline
def mindfulness_agent(user_query):
    understanding = input_understanding(user_query)
    tracker = StateTracker()
    memory = tracker.update_state(understanding)
    prompt = plan_prompt(memory)
    output = output_generator(prompt)
    return output

if __name__ == "__main__":
    query = input("How are you feeling today or what kind of mindfulness prompt do you want? ")
    response = mindfulness_agent(query)
    print("\nYour Mindfulness Prompt for Today:\n", response)
