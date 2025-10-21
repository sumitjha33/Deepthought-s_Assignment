Gemini Multi-Agent AI System
Overview
This repository implements a modular multi-agent AI system powered by Google Gemini. The system features a manager agent (brain_ai.py) that intelligently routes user requests to specialized agents for study planning, mindfulness prompts, and video idea brainstorming. Each agent uses a robust 4-layer architecture for input understanding, state tracking, task planning, and output generation.

Architecture & Workflow
System Diagram
text
+---------+        +------------------+
|  User   | -----> |   brain_ai.py    | (Manager/Router)
+---------+        +------------------+
                          |
        +-----------------+-----------------+
        |                 |                 |
+----------------+ +----------------+ +----------------+
| study_planner  | | mindfulness    | | video_idea     |
| _agent.py      | | _agent.py      | | _agent.py      |
+----------------+ +----------------+ +----------------+
User interacts with the system via a single entry point (brain_ai.py).

brain_ai.py analyzes the request and routes it to the correct specialized agent.

Specialized agents process the request and return a formatted response.

Agents Explained
1. Study Planner Agent (study_planner_agent.py)
Purpose: Generates personalized, chapter-wise study revision plans for students.

Workflow:

Input Understanding: Extracts subject, exam date, and revision needs.

State Tracker: Maintains session context (subject, timeframe).

Task Planner: Designs a step-by-step study plan.

Output Generator: Formats the plan in Markdown with motivational tips.

2. Mindfulness Prompter Agent (mindfulness_agent.py)
Purpose: Delivers daily, actionable mindfulness prompts tailored to user mood or preference.

Workflow:

Input Understanding: Detects mood, desired prompt type.

State Tracker: Remembers user’s emotional context.

Task Planner: Crafts a relevant mindfulness prompt.

Output Generator: Presents the prompt with a motivational message.

3. Video Idea Brainstorm Agent (video_idea_agent.py)
Purpose: Suggests creative, catchy short video ideas for creators, customized by topic, style, and platform.

Workflow:

Input Understanding: Extracts topic, style, platform.

State Tracker: Tracks user’s creative context.

Task Planner: Generates 3 video ideas with hooks and titles.

Output Generator: Formats ideas in Markdown for easy reading.

4. Manager Agent (brain_ai.py)
Purpose: Serves as the system’s entry point and router.

Workflow:

Intent Classification: Uses Gemini to analyze the user’s request and select the right agent.

Agent Routing: Calls the correct specialized agent based on intent.

Unified Interface: Returns the agent’s response to the user.

File Structure
text
.
├── brain_ai.py
├── study_planner_agent.py
├── mindfulness_agent.py
├── video_idea_agent.py
├── .env
├── README.md
Setup Instructions
Clone the repository:

bash
git clone https://github.com/yourusername/gemini-multi-agent-ai.git
cd gemini-multi-agent-ai
Create and activate a Python virtual environment:

bash
python -m venv venv
source venv/bin/activate  # (Linux/Mac)
venv\Scripts\activate     # (Windows)
Install dependencies:

bash
pip install google-generativeai python-dotenv
Add your Gemini API key to a .env file:

text
GEMINI_API_KEY=your_api_key_here
Never share your API key publicly or include it in submissions.

How to Run
Main Entry Point:
Run the manager agent to access all features:

bash
python brain_ai.py
Example requests:

“Help me make a 7-day study plan for my math exam.”

“I feel stressed, give me a mindfulness prompt.”

“Brainstorm funny video ideas about AI for YouTube Shorts.”

Run Individual Agents:
You can also run any agent directly:

bash
python study_planner_agent.py
python mindfulness_agent.py
python video_idea_agent.py
