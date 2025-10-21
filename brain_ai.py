
import os
import google.generativeai as genai
from dotenv import load_dotenv
from study_planner_agent import study_planner_agent
from mindfulness_agent import mindfulness_agent
from video_idea_agent import video_idea_agent

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')

def classify_intent(user_input):
    system_prompt = """
    You are a smart AI router. Classify the user's request as one of:
    - "study_planner" (if it's about exams, revision, study plans)
    - "mindfulness" (if it's about mood, mindfulness, positivity, reflection)
    - "video_ideas" (if it's about content creation, video ideas, brainstorming)
    Return only the label: study_planner, mindfulness, or video_ideas.
    """
    response = model.generate_content(f"{system_prompt}\n\nUser: {user_input}")
    return response.text.strip().lower()

def brain_ai(user_input):
    intent = classify_intent(user_input)
    if "study_planner" in intent:
        return study_planner_agent(user_input)
    elif "mindfulness" in intent:
        return mindfulness_agent(user_input)
    elif "video_ideas" in intent or "video" in intent:
        return video_idea_agent(user_input)
    else:
        return "Sorry, I couldn't understand your request. Please try rephrasing."

if __name__ == "__main__":
    query = input("What do you want help with? ")
    response = brain_ai(query)
    print("\nAI Response:\n", response)
