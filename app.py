from flask import Flask, render_template, request, jsonify
import re
from datetime import datetime
import random

app = Flask(__name__)

# ---------------- Bharath's Profile ---------------- #
PERSONAL_INFO = {
    "name": "Janagam Bharath",
    "location": "Hyderabad, India",
    "profession": "Aspiring LLM Engineer & Python Developer",
    "current_study": "Diploma in ECE → Computer Science",
    "interests": ["AI/LLM Development", "Python", "Flask Web Development", "Anime (One Piece, Naruto)", "Self-learning", "AI Tools"],
    "languages": ["Python", "C", "Java"],
    "web_tech": ["HTML", "CSS", "Flask"],
    "ai_tech": ["HuggingFace", "Chatbot Development"],
    "tools": ["Git", "Termux", "Render", "GitHub", "CapCut"],
    "current_projects": [
        "AI Chatbot using Python + Flask + HuggingFace",
        "Portfolio Website with resume and projects",
        "Learning DSA in C",
        "LLM Engineering studies"
    ],
    "mission": "To build AI solutions that make a difference and make my parents proud.",
    "contact": {
        "email": "janagambharath1107@gmail.com",
        "linkedin": "linkedin.com/in/janagam-bharath-9ab1b335b",
        "github": "github.com/janagambharath",
        "portfolio": "bharath-portfolio-otas.onrender.com"
    }
}

# ---------------- Chatbot Class ---------------- #
class IntelligentPersonalChatbot:
    def __init__(self):
        self.context_memory = []
        self.state = {"user_name": None, "depth": 0}
        self.patterns = {
            "greeting": [r"\b(hi|hello|hey|greetings)\b", r"^(yo|sup|what's up)"],
            "introduction": [r"\bwho\s*(are|is)\s*(you|bharath)\b", r"introduce|about bharath"],
            "skills": [r"\bskills?|languages?|technologies?|tools?\b"],
            "projects": [r"\bprojects?|portfolio|work\b"],
            "education": [r"\b(education|study|college|diploma)\b"],
            "experience": [r"\bexperience|career|background\b"],
            "motivation": [r"\b(why|motivation|goal|dream)\b"],
            "contact": [r"\b(contact|email|linkedin|github)\b"],
            "personal": [r"\b(anime|hobbies|interests?)\b"],
            "help": [r"\b(help|assist|guide)\b"]
        }
        print("✅ BharathBot Ready!")

    def detect_intent(self, message):
        message_lower = message.lower()
        for intent, pats in self.patterns.items():
            if any(re.search(p, message_lower) for p in pats):
                return intent
        return "general"

    def update_context(self, message, intent):
        self.context_memory.append({"msg": message, "intent": intent, "time": datetime.now()})
        if len(self.context_memory) > 5:
            self.context_memory.pop(0)
        self.state["depth"] += 1

    def respond(self, intent):
        responses = {
            "greeting": lambda: f"👋 Hey! I'm BharathBot. Ask me about {PERSONAL_INFO['name']}'s skills or projects.",
            "introduction": lambda: f"🌟 I'm {PERSONAL_INFO['name']} from {PERSONAL_INFO['location']} — {PERSONAL_INFO['profession']}.",
            "skills": lambda: f"💻 Skills: {', '.join(PERSONAL_INFO['languages'] + PERSONAL_INFO['web_tech'] + PERSONAL_INFO['ai_tech'])}",
            "projects": lambda: f"🚀 Projects: {', '.join(PERSONAL_INFO['current_projects'])}",
            "education": lambda: f"📚 Studying: {PERSONAL_INFO['current_study']}",
            "experience": lambda: "💼 Still a student, but working on real-world AI projects.",
            "motivation": lambda: f"🔥 Mission: {PERSONAL_INFO['mission']}",
            "contact": lambda: f"📩 Email: {PERSONAL_INFO['contact']['email']} | GitHub: {PERSONAL_INFO['contact']['github']}",
            "personal": lambda: f"🎌 Interests: {', '.join(PERSONAL_INFO['interests'])}",
            "help": lambda: "🤝 You can ask about skills, projects, education, or contact info.",
            "general": lambda: "🤔 I can tell you about Bharath's skills, projects, and journey!"
        }
        return responses.get(intent, responses["general"])()

    def chat(self, message):
        intent = self.detect_intent(message)
        self.update_context(message, intent)
        return self.respond(intent)

# ---------------- Flask Routes ---------------- #
bot = IntelligentPersonalChatbot()

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    try:
        user_message = request.json.get("message", "").strip()
        if not user_message:
            return jsonify({"response": "Ask me anything about Bharath! 🤖", "status": "success"})
        
        reply = bot.chat(user_message)
        return jsonify({
            "response": reply,
            "status": "success",
            "timestamp": datetime.now().strftime("%H:%M")
        })
    except Exception:
        return jsonify({"response": "⚠️ Error! Try again.", "status": "error"})

@app.route("/health")
def health():
    return jsonify({"status": "healthy", "bot": "online"})

if __name__ == "__main__":
    app.run(debug=True)
