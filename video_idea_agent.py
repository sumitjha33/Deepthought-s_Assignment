# video_idea_agent.py
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
    You are an input analyzer for a Video Idea Brainstorm AI Agent.
    Understand if the user wants ideas for a specific topic, style (funny, educational, inspirational), or platform (YouTube Shorts, Instagram Reels, TikTok).
    Return a JSON with fields: {"intent": "", "topic": "", "style": "", "platform": "", "custom_notes": ""}
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
def plan_ideas(state):
    plan_prompt = f"""
    You are the task planner for a video idea brainstorming assistant.
    Based on the user's context below:
    {state}

    Generate 3 creative, engaging, and platform-appropriate short video ideas.
    Each idea should include a catchy title, a 1-2 sentence concept, and a suggested hook for the first 3 seconds.
    If a style or platform is specified, tailor the ideas accordingly.
    """
    response = model.generate_content(plan_prompt)
    return response.text

# 4. Output Generator Layer
def output_generator(ideas_text):
    output_prompt = f"""
    Format the following video ideas in a clear, energetic, and inspiring tone.
    Use markdown with bold titles and bullet points for each idea.
    Here are the raw ideas:
    {ideas_text}
    """
    response = model.generate_content(output_prompt)
    return response.text

# 5. Master function to run the pipeline
def video_idea_agent(user_query):
    understanding = input_understanding(user_query)
    tracker = StateTracker()
    memory = tracker.update_state(understanding)
    ideas = plan_ideas(memory)
    output = output_generator(ideas)
    return output

# 6. Example Run
if __name__ == "__main__":
    query = input("What kind of short video ideas do you want to brainstorm? ")
    response = video_idea_agent(query)
    print("\nYour Video Ideas:\n", response)
