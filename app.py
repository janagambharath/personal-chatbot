from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime
import random

app = Flask(__name__)

# Personal information - Janagam Bharath's Details
PERSONAL_INFO = {
    "name": "Janagam Bharath",
    "age": "Student",
    "location": "Hyderabad, India",
    "profession": "Aspiring LLM Engineer & Python Developer",
    "current_study": "Diploma in ECE, transitioning to Computer Science",
    "interests": ["AI/LLM Development", "Python Programming", "Flask Web Development", "Anime (One Piece, Naruto)", "Self-learning", "Building AI-powered tools"],
    "education": "Diploma in ECE (current), Self-taught Computer Science foundations",
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
    "mission": "To become a skilled developer who builds AI solutions that make a difference — and to make my parents proud by creating a successful future through tech",
    "motivation": "Coming from a middle-class family in Hyderabad, driven by hard work, focus, and purpose. Deleted social media 100+ days ago to focus on career.",
    "philosophy": "Discipline and deep learning over distractions. Consistency compounds into mastery. Getting 1% better every day.",
    "inspiration": "Anime like One Piece and Naruto taught me to turn pain into purpose",
    "contact": {
        "email": "janagambharath1107@gmail.com",
        "linkedin": "linkedin.com/in/janagam-bharath-9ab1b335b",
        "github": "github.com/janagambharath",
        "portfolio": "bharath-portfolio-otas.onrender.com"
    }
}

class IntelligentPersonalChatbot:
    def __init__(self):
        self.context_memory = []
        self.conversation_state = {
            "user_name": None,
            "topic_interest": None,
            "conversation_depth": 0,
            "previous_questions": []
        }
        
        # Enhanced patterns for more natural language understanding
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|greetings|good\s*(morning|afternoon|evening))\b',
                r'^(yo|sup|what\'?s up)'
            ],
            'introduction': [
                r'\b(who\s*(are|is)\s*(you|bharath)|introduce|tell me about|about bharath)\b',
                r'\b(what\s*(do\s*you\s*do|are\s*you))\b'
            ],
            'skills': [
                r'\b(skills?|programming|technical|abilities|what can you do)\b',
                r'\b(languages?|technologies?|tools?|frameworks?)\b'
            ],
            'projects': [
                r'\b(projects?|portfolio|work|built|created|developing)\b',
                r'\b(github|code|applications?|websites?)\b'
            ],
            'education': [
                r'\b(education|study|studying|college|university|degree|diploma)\b',
                r'\b(background|academic|learning)\b'
            ],
            'experience': [
                r'\b(experience|journey|career|professional|background)\b',
                r'\b(how long|when did you start)\b'
            ],
            'motivation': [
                r'\b(why|motivation|inspire|goal|dream|ambition)\b',
                r'\b(future|plans?|aspiration)\b'
            ],
            'contact': [
                r'\b(contact|reach|email|linkedin|github|hire|job)\b',
                r'\b(get in touch|connect|portfolio)\b'
            ],
            'personal': [
                r'\b(anime|hobbies|interests?|free time|personal)\b',
                r'\b(one piece|naruto|entertainment)\b'
            ],
            'help': [
                r'\b(help|assist|support|guide|advice)\b',
                r'\b(how to|tutorial|learn)\b'
            ]
        }
        
        print("✨ Intelligent BharathBot initialized - Advanced AI-like responses ready!")
    
    def extract_intent(self, message):
        """Extract intent from user message using pattern matching"""
        message_lower = message.lower()
        detected_intents = []
        
        for intent, patterns in self.intent_patterns.items():
            for pattern in patterns:
                if re.search(pattern, message_lower, re.IGNORECASE):
                    detected_intents.append(intent)
                    break
        
        return detected_intents if detected_intents else ['general']
    
    def update_conversation_context(self, message, intent):
        """Maintain conversation context for more natural responses"""
        self.context_memory.append({
            'message': message,
            'intent': intent,
            'timestamp': datetime.now()
        })
        
        # Keep only last 5 exchanges for context
        if len(self.context_memory) > 5:
            self.context_memory.pop(0)
        
        self.conversation_state['conversation_depth'] += 1
        
        # Extract user name if mentioned
        name_match = re.search(r'(?:i\'?m|my name is|call me)\s+([a-zA-Z]+)', message.lower())
        if name_match and not self.conversation_state['user_name']:
            self.conversation_state['user_name'] = name_match.group(1).title()
    
    def get_contextual_greeting(self):
        """Generate contextual greetings"""
        greetings = [
            "Hey there! 👋 I'm BharathBot, your AI assistant created by Janagam Bharath.",
            "Hello! 🤖 Great to meet you! I'm here to tell you all about Bharath's tech journey.",
            "Hi! ✨ I'm BharathBot - ask me anything about Bharath's skills, projects, or aspirations!"
        ]
        
        greeting = random.choice(greetings)
        
        if self.conversation_state['user_name']:
            greeting = f"Hey {self.conversation_state['user_name']}! " + greeting.split('!', 1)[1] if '!' in greeting else greeting
        
        return greeting
    
    def generate_smart_response(self, intents, message):
        """Generate intelligent, context-aware responses"""
        primary_intent = intents[0] if intents else 'general'
        
        # Multi-intent handling
        if len(intents) > 1:
            return self.handle_multi_intent_query(intents, message)
        
        # Single intent responses
        response_map = {
            'greeting': self.get_contextual_greeting,
            'introduction': self.get_introduction_response,
            'skills': self.get_skills_response,
            'projects': self.get_projects_response,
            'education': self.get_education_response,
            'experience': self.get_experience_response,
            'motivation': self.get_motivation_response,
            'contact': self.get_contact_response,
            'personal': self.get_personal_response,
            'help': self.get_help_response,
            'general': self.get_general_response
        }
        
        return response_map.get(primary_intent, self.get_general_response)(message)
    
    def handle_multi_intent_query(self, intents, message):
        """Handle complex queries with multiple intents"""
        if 'skills' in intents and 'projects' in intents:
            return """🚀 **Bharath's Tech Arsenal & Projects:**

**Core Skills:**
• Python, Java, C programming
• Flask web development + AI integration
• HuggingFace for LLM applications

**Current Projects:**
• AI-powered chatbot (like me!) using Flask + HuggingFace
• Personal portfolio with interactive features
• DSA mastery in C language

*He combines technical skills with real project experience - theory meets practice!* 💪

Want to dive deeper into any specific area?"""
        
        elif 'motivation' in intents and 'education' in intents:
            return """📚 **Bharath's Learning Journey & Drive:**

Starting with Diploma in ECE, but his passion led him to self-teach Computer Science fundamentals. Why? Because he believes in following your true calling!

**His Philosophy:** "Discipline over distractions. 1% better every day."

He even deleted social media 100+ days ago to laser-focus on building his tech career. That's dedication! 🎯

**Mission:** Build AI solutions that matter while making his family proud.

What aspect of his journey interests you most?"""
        
        return self.get_general_response(message)
    
    def get_introduction_response(self, message):
        responses = [
            f"""🌟 **Meet Janagam Bharath!**

I'm an aspiring LLM Engineer and Python developer from {PERSONAL_INFO['location']}. Currently pursuing Diploma in ECE, but my heart beats for AI and programming!

**What drives me:** Building AI-powered solutions that make a real impact while staying true to my roots and making my family proud.

**Current focus:** Mastering Python, Flask, and LLM development through hands-on projects.

*Fun fact: I deleted social media 100+ days ago to focus entirely on my tech journey!* 🎯

What would you like to know more about?""",

            f"""👨‍💻 **I'm {PERSONAL_INFO['name']} - Nice to meet you!**

Think of me as someone who turned curiosity into code! I'm transitioning from ECE to Computer Science because I discovered my true passion lies in AI and software development.

**My Story:** Self-taught developer building real-world projects while studying. From Hyderabad with big dreams and the discipline to make them reality.

**Philosophy:** "Consistency compounds into mastery" - inspired by anime heroes who never give up!

Ready to explore my technical world? 🚀"""
        ]
        return random.choice(responses)
    
    def get_skills_response(self, message):
        return """⚡ **Bharath's Technical Superpowers:**

**Programming Languages:**
🐍 **Python** - My main weapon! Flask, chatbots, AI integration
☕ **Java** - Object-oriented problem solving
🔧 **C** - Currently mastering DSA fundamentals

**Web Development:**
🌐 HTML, CSS, Flask framework
🤖 AI-powered web applications

**AI/LLM Technologies:**
🧠 HuggingFace integration
💬 Intelligent chatbot development
🚀 LLM engineering principles

**Developer Tools:**
📦 Git, GitHub for version control
☁️ Render for deployment
📱 Termux for mobile development

*Each skill is battle-tested through real projects!* Want to see them in action? 💪"""
    
    def get_projects_response(self, message):
        return """🚀 **Bharath's Project Showcase:**

**🤖 AI Chatbot (Current)**
• Python + Flask + HuggingFace integration
• Intelligent conversation handling
• Deployed and ready for real users!

**💼 Interactive Portfolio Website**
• Personal brand showcase
• Resume, projects, contact integration
• Live at: bharath-portfolio-otas.onrender.com

**📊 DSA Mastery Journey**
• Learning Data Structures in C
• Building strong algorithmic foundation
• Problem-solving skills development

**🧠 LLM Engineering Studies**
• Deep dive into language models
• Practical implementation focus
• Future-ready AI skills

*Each project teaches something new and builds toward the bigger vision!* 

Check out his GitHub: github.com/janagambharath 🔥"""
    
    def get_education_response(self, message):
        return """📚 **Bharath's Learning Path:**

**Formal Education:**
• Diploma in ECE (Electronics & Communication)
• Strong technical foundation

**Self-Directed Learning:**
• Computer Science fundamentals (self-taught)
• Python programming mastery
• AI/LLM engineering principles

**Learning Philosophy:**
"Why limit yourself to one field when technology is interconnected?"

**Current Focus:**
• Bridging ECE knowledge with software development
• Hands-on project-based learning
• Building industry-relevant skills

**The Transition Story:**
Started with ECE but discovered passion for AI and programming. Instead of waiting, took charge and began self-learning while still in college!

*That's the spirit of a true lifelong learner!* 🌟"""
    
    def get_experience_response(self, message):
        return """🌟 **Bharath's Tech Journey:**

**The Beginning:**
Started as an ECE student but felt the magnetic pull toward programming and AI. Made the bold decision to self-learn while continuing formal education.

**Key Milestones:**
• 📅 100+ days without social media (laser focus mode!)
• 🐍 Python mastery through practical projects
• 🤖 First AI chatbot deployment success
• 🌐 Portfolio website launched and live

**Growth Mindset:**
• Daily learning and coding practice
• Project-driven skill development
• Community engagement through GitHub

**What Sets Him Apart:**
Combines theoretical knowledge with real-world application. Not just learning - building, deploying, and iterating!

**Current Status:**
Actively developing AI solutions while preparing for advanced LLM engineering roles.

*From curiosity to capability - that's the journey so far!* 🚀"""
    
    def get_motivation_response(self, message):
        return """🔥 **What Drives Bharath:**

**Core Mission:**
"Build AI solutions that make a difference while making my parents proud through tech success."

**Personal Why:**
Coming from a middle-class family in Hyderabad, driven by purpose over profit. Every line of code is written with gratitude and determination.

**Philosophy:**
• "Discipline and deep learning over distractions"
• "Consistency compounds into mastery"
• "Getting 1% better every day"

**Inspiration Sources:**
🏴‍☠️ **One Piece & Naruto:** "Turn pain into purpose" - like his favorite anime heroes who never give up despite challenges.

**The Social Media Detox:**
Deleted all social platforms 100+ days ago. Why? Because focus is the ultimate superpower in a distracted world.

**Long-term Vision:**
Become a skilled developer whose AI solutions create positive impact. Success measured by problems solved, not just money earned.

*That's the heart of a true builder!* ❤️"""
    
    def get_contact_response(self, message):
        return f"""📞 **Ready to Connect with Bharath?**

**Professional Channels:**
✉️ **Email:** {PERSONAL_INFO['contact']['email']}
💼 **LinkedIn:** {PERSONAL_INFO['contact']['linkedin']}
🔗 **GitHub:** {PERSONAL_INFO['contact']['github']}
🌐 **Portfolio:** {PERSONAL_INFO['contact']['portfolio']}

**What to Expect:**
• Quick response (he's always learning/building!)
• Genuine conversation about tech and opportunities
• Collaborative mindset and problem-solving approach

**Perfect for:**
• Job opportunities and internships
• Collaborative projects
• Tech discussions and mentorship
• AI/LLM development partnerships

**Fun Fact:** His email and LinkedIn are checked daily - part of his disciplined routine!

*Don't hesitate to reach out. Bharath believes great connections lead to greater opportunities!* 🌟"""
    
    def get_personal_response(self, message):
        return """🎌 **Beyond the Code - Personal Side:**

**Anime Inspiration:**
🏴‍☠️ **One Piece:** "Dreams don't have expiration dates!" - Luffy's determination resonates with his coding journey
🍥 **Naruto:** "Hard work beats talent when talent doesn't work hard" - this defines his self-learning approach

**Life Philosophy:**
• Turn struggles into strength
• Stay humble, keep building
• Focus on growth over glory

**Personal Discipline:**
• 100+ days social media free (and counting!)
• Daily coding and learning routine
• Anime breaks for motivation and relaxation

**Hobbies:**
• Building cool AI projects
• Learning new programming concepts
• Watching anime for life lessons
• Self-improvement through discipline

**What Anime Taught Him:**
"Every hero starts as a beginner with big dreams. The difference? They never quit training!"

*That's the mindset behind every project he builds!* 💪"""
    
    def get_help_response(self, message):
        return """🤝 **How BharathBot Can Help You:**

**I can tell you about:**
• 🔧 Bharath's technical skills and expertise
• 🚀 His current and past projects
• 📚 Educational background and learning journey
• 💡 Career goals and motivations
• 📞 Contact information for opportunities
• 🎌 Personal interests and inspirations

**Smart Questions to Ask:**
• "What projects is Bharath working on?"
• "How did he transition from ECE to programming?"
• "What makes him different from other developers?"
• "How can I connect with him for opportunities?"

**Need Something Specific?**
Just ask naturally! I understand context and can provide detailed information about any aspect of Bharath's journey.

*I'm here to help you discover why Bharath would be a great addition to your team or project!* ✨"""
    
    def get_general_response(self, message):
        general_responses = [
            """🤔 **Interesting question!** 

I'm focused on sharing Bharath's tech journey and capabilities. Could you ask me about:
• His programming skills and projects
• Educational background and learning path
• Career goals and motivations
• Contact information for opportunities

*What aspect of Bharath's profile interests you most?*""",

            """💭 **I'd love to help you learn about Bharath!**

I'm specialized in discussing his:
• Technical expertise (Python, AI, Flask)
• Project portfolio and achievements
• Professional background and goals
• Personal motivation and work ethic

*What would you like to discover about his capabilities?*""",

            """🎯 **Let me guide you to the right information!**

I can provide detailed insights about:
• Bharath's programming skills and experience
• His current AI and web development projects
• Educational journey and self-learning approach
• Professional goals and contact details

*Ask me anything about his tech profile!*"""
        ]
        return random.choice(general_responses)
    
    def get_personal_response_main(self, message):
        """Main response generation with context awareness"""
        # Extract user intent
        intents = self.extract_intent(message)
        
        # Update conversation context
        self.update_conversation_context(message, intents)
        
        # Generate intelligent response
        response = self.generate_smart_response(intents, message)
        
        # Add follow-up questions for engagement
        if self.conversation_state['conversation_depth'] % 3 == 0:
            follow_ups = [
                "\n*Is there anything specific you'd like to explore further?*",
                "\n*What other aspects of Bharath's journey interest you?*",
                "\n*Any particular skills or projects you'd like to know more about?*"
            ]
            response += random.choice(follow_ups)
        
        return response

# Initialize the intelligent chatbot
chatbot = IntelligentPersonalChatbot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': "I'm here to help! Ask me anything about Bharath's skills, projects, or journey! 🤖",
                'status': 'success'
            })
        
        # Get intelligent response
        bot_response = chatbot.get_personal_response_main(user_message)
        
        return jsonify({
            'response': bot_response,
            'status': 'success',
            'timestamp': datetime.now().strftime('%H:%M')
        })
    
    except Exception as e:
        return jsonify({
            'response': "🔧 Oops! Something went wrong. Let me recalibrate... Try asking about Bharath's skills or projects!",
            'status': 'error'
        })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'bot_status': 'BharathBot AI is online and ready! 🤖',
        'capabilities': [
            'Natural language understanding',
            'Context-aware responses', 
            'Mult
