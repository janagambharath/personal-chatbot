from flask import Flask, render_template, request, jsonify
import json
import re
from datetime import datetime
import random
import time

app = Flask(__name__)

# Enhanced Personal Information with more dynamic content
PERSONAL_INFO = {
    "name": "Janagam Bharath",
    "age": "18",
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
    "achievements": [
        "100+ days social media detox for career focus",
        "Successfully deployed AI chatbot applications",
        "Self-taught multiple programming languages",
        "Built and deployed portfolio website from scratch"
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

class CreativeIntelligentBharathBot:
    def __init__(self):
        self.context_memory = []
        self.conversation_state = {
            "user_name": None,
            "user_interests": [],
            "conversation_depth": 0,
            "previous_topics": [],
            "user_mood": "neutral",
            "engagement_level": 0,
            "session_start_time": datetime.now()
        }
        
        # Enhanced personality traits for dynamic responses
        self.personality_modes = {
            "enthusiastic": {"emoji_prob": 0.9, "exclamation_prob": 0.8, "energy_level": "high"},
            "professional": {"emoji_prob": 0.3, "exclamation_prob": 0.2, "energy_level": "balanced"},
            "friendly": {"emoji_prob": 0.7, "exclamation_prob": 0.5, "energy_level": "warm"},
            "inspiring": {"emoji_prob": 0.6, "exclamation_prob": 0.7, "energy_level": "motivational"}
        }
        
        self.current_personality = "friendly"
        
        # Enhanced patterns with more nuanced understanding
        self.intent_patterns = {
            'greeting': [
                r'\b(hi|hello|hey|greetings|good\s*(morning|afternoon|evening|day)|sup|yo|wassup)\b',
                r'^(hola|namaste|bonjour)',
                r'\b(how\s*(are|is)\s*(you|things)|what\'?s up)\b'
            ],
            'introduction': [
                r'\b(who\s*(are|is)\s*(you|bharath)|introduce|tell me about|about bharath)\b',
                r'\b(what\s*(do\s*you\s*do|are\s*you)|your story|background)\b',
                r'\b(get to know|learn about|meet)\b'
            ],
            'skills': [
                r'\b(skills?|programming|technical|abilities|what can you do|expertise)\b',
                r'\b(languages?|technologies?|tools?|frameworks?|stack)\b',
                r'\b(good at|proficient|talented|capable)\b'
            ],
            'projects': [
                r'\b(projects?|portfolio|work|built|created|developing|made)\b',
                r'\b(github|code|applications?|websites?|showcase)\b',
                r'\b(what.*built|show me|examples)\b'
            ],
            'education': [
                r'\b(education|study|studying|college|university|degree|diploma|learning)\b',
                r'\b(academic|school|qualification|course)\b'
            ],
            'experience': [
                r'\b(experience|journey|career|professional|background|path)\b',
                r'\b(how long|when.*start|timeline|story)\b'
            ],
            'motivation': [
                r'\b(why|motivation|inspire|goal|dream|ambition|drive)\b',
                r'\b(future|plans?|aspiration|vision|mission)\b'
            ],
            'contact': [
                r'\b(contact|reach|email|linkedin|github|hire|job|connect)\b',
                r'\b(get in touch|portfolio|work together|collaborate)\b'
            ],
            'personal': [
                r'\b(anime|hobbies|interests?|free time|personal|fun)\b',
                r'\b(one piece|naruto|entertainment|passion)\b'
            ],
            'help': [
                r'\b(help|assist|support|guide|advice|mentor)\b',
                r'\b(how to|tutorial|learn|teach)\b'
            ],
            'compliment': [
                r'\b(awesome|amazing|cool|great|impressive|wonderful|fantastic)\b',
                r'\b(like|love|appreciate|admire)\b'
            ],
            'farewell': [
                r'\b(bye|goodbye|see you|farewell|take care|later)\b',
                r'\b(thanks|thank you|appreciate|grateful)\b'
            ]
        }
        
        # Creative response templates
        self.creative_templates = {
            'tech_metaphors': [
                "like debugging life one line at a time",
                "like compiling dreams into reality",
                "like optimizing potential for maximum performance",
                "like version controlling his growth journey"
            ],
            'anime_references': [
                "Like Luffy pursuing the One Piece, Bharath chases his coding dreams!",
                "With Naruto's never-give-up spirit, he tackles every programming challenge!",
                "Like a true ninja, he masters new technologies in the shadows!",
                "His coding journey is his own Grand Line adventure!"
            ],
            'inspirational_quotes': [
                "Every expert was once a beginner who refused to quit",
                "Code is poetry written in logic",
                "The best time to plant a tree was 20 years ago. The second best time is now",
                "Success is not final, failure is not fatal: it's the courage to continue that counts"
            ]
        }
        
        print("🚀 Creative BharathBot initialized - Next-level AI personality loaded!")
    
    def detect_user_mood(self, message):
        """Detect user mood for adaptive responses"""
        positive_indicators = ['great', 'awesome', 'amazing', 'love', 'excited', 'happy', '😊', '🎉', '👍']
        negative_indicators = ['bad', 'tired', 'stressed', 'difficult', 'problem', 'issue', '😞', '😤']
        curious_indicators = ['?', 'how', 'what', 'why', 'when', 'where', 'tell me', 'explain']
        
        message_lower = message.lower()
        
        if any(indicator in message_lower for indicator in positive_indicators):
            return "positive"
        elif any(indicator in message_lower for indicator in negative_indicators):
            return "empathetic" 
        elif any(indicator in message_lower for indicator in curious_indicators):
            return "curious"
        else:
            return "neutral"
    
    def adapt_personality(self, user_mood, conversation_depth):
        """Dynamically adapt personality based on context"""
        if user_mood == "positive":
            self.current_personality = "enthusiastic"
        elif user_mood == "empathetic":
            self.current_personality = "inspiring"
        elif user_mood == "curious":
            self.current_personality = "professional"
        elif conversation_depth > 5:
            self.current_personality = "friendly"
        else:
            self.current_personality = random.choice(["friendly", "enthusiastic"])
    
    def extract_intent(self, message):
        """Enhanced intent extraction with confidence scoring"""
        message_lower = message.lower()
        intent_scores = {}
        
        for intent, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, message_lower, re.IGNORECASE))
                score += matches
            if score > 0:
                intent_scores[intent] = score
        
        # Sort by confidence and return top intents
        sorted_intents = sorted(intent_scores.items(), key=lambda x: x[1], reverse=True)
        return [intent for intent, score in sorted_intents[:3]] if sorted_intents else ['general']
    
    def add_creative_elements(self, response):
        """Add creative elements based on current personality"""
        personality = self.personality_modes[self.current_personality]
        
        # Add emojis based on probability
        if random.random() < personality["emoji_prob"]:
            emojis = {
                "enthusiastic": ["🚀", "⚡", "🔥", "💪", "🌟", "✨"],
                "professional": ["💼", "🎯", "📊", "🔧", "⚙️"],
                "friendly": ["😊", "👋", "🤝", "💫", "🌈"],
                "inspiring": ["💡", "🎨", "🏆", "🌅", "🎯"]
            }
            response += " " + random.choice(emojis[self.current_personality])
        
        # Add exclamations based on probability
        if random.random() < personality["exclamation_prob"] and not response.endswith('!'):
            if random.random() < 0.5:
                response += "!"
        
        return response
    
    def generate_dynamic_greeting(self):
        """Generate time and context-aware greetings"""
        current_time = datetime.now()
        hour = current_time.hour
        
        time_greetings = {
            "morning": ["Good morning", "Rise and shine", "Morning"],
            "afternoon": ["Good afternoon", "Hope your day's going well", "Afternoon"],
            "evening": ["Good evening", "Evening", "Hope you had a great day"],
            "night": ["Good evening", "Evening", "Working late"]
        }
        
        if 5 <= hour < 12:
            time_key = "morning"
        elif 12 <= hour < 17:
            time_key = "afternoon" 
        elif 17 <= hour < 22:
            time_key = "evening"
        else:
            time_key = "night"
        
        base_greeting = random.choice(time_greetings[time_key])
        
        personalized_intros = [
            f"{base_greeting}! I'm BharathBot - your intelligent guide to Bharath's tech universe!",
            f"{base_greeting}! Welcome to BharathBot, where AI meets aspiration!",
            f"{base_greeting}! I'm the AI creation of Janagam Bharath - ready to explore his journey together?"
        ]
        
        return self.add_creative_elements(random.choice(personalized_intros))
    
    def get_contextual_follow_up(self, intent, conversation_depth):
        """Generate smart follow-up questions"""
        follow_ups = {
            'skills': [
                "Which of his tech skills excites you most?",
                "Want to see these skills in action through his projects?",
                "Curious about how he learned these technologies?"
            ],
            'projects': [
                "Which project sounds most interesting to you?",
                "Want to dive deeper into any specific project?",
                "Interested in the technical details behind these builds?"
            ],
            'motivation': [
                "What resonates with you about his journey?",
                "Does his philosophy inspire any thoughts about your own path?",
                "Want to know more about how anime influences his work ethic?"
            ],
            'general': [
                "What aspect of Bharath's story interests you most?",
                "Any specific questions about his journey?",
                "Would you like to explore his technical skills or personal story?"
            ]
        }
        
        if conversation_depth > 3 and random.random() > 0.7:
            return "\n\n" + random.choice(follow_ups.get(intent, follow_ups['general']))
        return ""
    
    def generate_smart_response(self, intents, message, user_mood):
        """Generate creative, context-aware responses"""
        primary_intent = intents[0] if intents else 'general'
        
        # Handle special cases first
        if 'compliment' in intents:
            return self.get_compliment_response()
        elif 'farewell' in intents:
            return self.get_farewell_response()
        
        # Multi-intent handling with creative combinations
        if len(intents) > 1:
            return self.handle_creative_multi_intent(intents, message)
        
        # Enhanced single intent responses
        response_methods = {
            'greeting': self.get_creative_greeting_response,
            'introduction': self.get_dynamic_introduction_response,
            'skills': self.get_creative_skills_response,
            'projects': self.get_engaging_projects_response,
            'education': self.get_inspiring_education_response,
            'experience': self.get_storytelling_experience_response,
            'motivation': self.get_motivational_response,
            'contact': self.get_professional_contact_response,
            'personal': self.get_fun_personal_response,
            'help': self.get_helpful_response,
            'general': self.get_adaptive_general_response
        }
        
        response_method = response_methods.get(primary_intent, self.get_adaptive_general_response)
        base_response = response_method(message, user_mood)
        
        # Add creative elements and follow-ups
        enhanced_response = self.add_creative_elements(base_response)
        follow_up = self.get_contextual_follow_up(primary_intent, self.conversation_state['conversation_depth'])
        
        return enhanced_response + follow_up
    
    def get_creative_greeting_response(self, message, user_mood):
        if self.conversation_state['conversation_depth'] == 1:
            return self.generate_dynamic_greeting()
        else:
            return random.choice([
                "Hey again! What else would you like to discover about Bharath?",
                "Back for more? I love your curiosity!",
                "Welcome back! Ready for another deep dive into Bharath's world?"
            ])
    
    def get_dynamic_introduction_response(self, message, user_mood):
        intros = [
            f"""🌟 **Meet the Code Craftsman: Janagam Bharath!**

Imagine someone who looked at ECE and said, "This is cool, but AI is calling my name!" That's Bharath - a self-driven developer from {PERSONAL_INFO['location']} who's rewriting his own story one Python line at a time.

**His Superpower?** Turning curiosity into code and dreams into deployed applications!

**Current Quest:** Mastering LLM engineering while building AI solutions that actually matter (like the intelligent bot you're chatting with right now!)

**Plot Twist:** He deleted social media 100+ days ago because he realized focus is the ultimate cheat code for success.

*Ready to explore what makes this developer different?*""",

            f"""👨‍💻 **The Developer Who Chose His Own Adventure!**

{PERSONAL_INFO['name']} isn't your typical programmer. He started in ECE but his heart was coding in Python! So what did he do? Created his own curriculum and became a self-taught AI enthusiast.

**From Hyderabad with Dreams:** Building tomorrow's AI solutions today
**Mission Critical:** Make parents proud while making technology more human

**Fun Algorithm:** 
```
while (learning == true) {
    build_projects()
    solve_problems()
    level_up_skills()
    repeat_with_more_passion()
}
```

*Want to see this algorithm in action through his projects?*"""
        ]
        return random.choice(intros)
    
    def get_creative_skills_response(self, message, user_mood):
        return f"""⚡ **Bharath's Tech Arsenal - Battle-Tested & Ready!**

**🐍 Python Mastery Level: Pythonista**
• Flask web wizardry with AI integration
• Chatbot development (like yours truly!)
• Data manipulation and API orchestration

**☕ Java Power: Object-Oriented Samurai**
• Clean code architecture
• Problem-solving through OOP principles

**🔧 C Language: The Foundation Builder** 
• Currently conquering DSA challenges
• System-level understanding
• Performance optimization mindset

**🤖 AI/LLM Technologies: The Future Builder**
• HuggingFace model integration
• Conversational AI development
• LLM engineering principles

**🌐 Full-Stack Foundation:**
• HTML/CSS for stellar interfaces
• Flask for robust backend systems
• Git/GitHub for version control mastery

**☁️ Deployment Ninja:**
• Render for cloud deployment
• Real-world application hosting

{random.choice(self.creative_templates['tech_metaphors']).capitalize()}! Each skill is earned through hands-on battles with real projects."""
    
    def get_engaging_projects_response(self, message, user_mood):
        return f"""🚀 **Bharath's Project Universe - Where Ideas Become Reality!**

**🤖 AI-Powered Chatbot (Current Crown Jewel)**
• Technology Stack: Python + Flask + HuggingFace magic
• Features: Intelligent conversations, context awareness, personality adaptation
• Status: Successfully deployed and conversing with humans (like right now!)
• *Fun Fact: The bot you're talking to is part of this project!*

**💼 Interactive Portfolio Ecosystem**
• A living showcase of skills and achievements
• Dynamic content, responsive design
• Live Demo: bharath-portfolio-otas.onrender.com
• *It's not just a website, it's a digital experience!*

**📊 DSA Mastery Campaign**
• Language: C (for that low-level understanding)
• Mission: Build unshakeable algorithmic foundations
• Strategy: Daily practice + real problem solving

**🧠 LLM Engineering Deep Dive**
• Exploring the frontiers of language models
• Hands-on implementation focus
• Future-proofing skills for the AI revolution

**Coming Soon:** More innovative projects brewing in the development pipeline!

{random.choice(self.anime_references)}

*Each project teaches something new and builds toward the bigger vision of AI-powered solutions!*"""
    
    def handle_creative_multi_intent(self, intents, message):
        """Handle complex queries with creative storytelling"""
        intent_combinations = {
            ('skills', 'projects'): self.get_skills_projects_combo,
            ('motivation', 'education'): self.get_motivation_education_combo,
            ('personal', 'motivation'): self.get_personal_motivation_combo,
            ('experience', 'projects'): self.get_experience_projects_combo
        }
        
        # Find matching combination
        for combo, method in intent_combinations.items():
            if all(intent in intents for intent in combo):
                return method()
        
        return self.get_adaptive_general_response(message, "curious")
    
    def get_skills_projects_combo(self):
        return f"""🎯 **The Perfect Storm: Where Bharath's Skills Meet Real Projects!**

**The Magic Formula:** Theory + Practice = Mastery

**🐍 Python Skills → AI Chatbot Reality**
Flask expertise powers intelligent conversations, HuggingFace integration creates smart responses, and deployment knowledge makes it accessible worldwide!

**☕ Java Foundation → Solid Architecture**
Object-oriented thinking shapes how he structures complex applications and solves problems systematically.

**🔧 C Mastery → DSA Excellence** 
Low-level understanding builds the foundation for optimized, efficient solutions.

**🚀 The Result?**
Projects that aren't just code - they're solutions that work, scale, and impress!

**Real Impact:**
• Chatbot serving real users (including you!)
• Portfolio attracting opportunities
• Skills proven through deployed applications

{random.choice(self.creative_templates['inspirational_quotes'])}

*Want to dive deeper into any specific skill-to-project pipeline?*"""
    
    def get_compliment_response(self):
        responses = [
            "🌟 Thank you! Bharath will be thrilled to hear that! His dedication to building quality solutions really shows, doesn't it?",
            "⚡ That means so much! Bharath pours his heart into every project - it's amazing when people appreciate the craftsmanship!",
            "🚀 You've got great taste! Bharath's combination of technical skills and genuine passion creates something special, right?"
        ]
        return random.choice(responses)
    
    def get_farewell_response(self):
        session_time = datetime.now() - self.conversation_state['session_start_time']
        minutes = int(session_time.total_seconds() / 60)
        
        responses = [
            f"🌟 It's been awesome chatting for {minutes} minutes! Thanks for getting to know Bharath's journey. Don't forget to check out his portfolio: {PERSONAL_INFO['contact']['portfolio']}",
            f"🚀 What a great conversation! Feel free to connect with Bharath directly - I know he'd love to chat more about opportunities and collaborations!",
            f"✨ Thanks for the engaging chat! Remember, Bharath is always open to meaningful connections and exciting projects. Reach out anytime!"
        ]
        return random.choice(responses)
    
    def get_adaptive_general_response(self, message, user_mood):
        if user_mood == "curious":
            return """🔍 **I love your curiosity!** Let me guide you through Bharath's world:

**🎯 Popular Topics:**
• His incredible project portfolio (AI chatbots, websites, and more!)
• The inspiring transition from ECE to AI/LLM engineering
• Technical skills that power real-world solutions
• Personal philosophy and anime-inspired motivation
• How to connect for opportunities and collaborations

**💡 Smart Questions to Unlock More:**
• "What makes Bharath different from other developers?"
• "How did he build such impressive projects while studying?"
• "What's his secret to staying focused and motivated?"

*What fascinates you most about his journey?*"""
        
        elif user_mood == "positive":
            return """🎉 **Your enthusiasm is contagious!** 

Bharath's story has that effect on people - there's something inspiring about someone who takes control of their destiny and builds their future one project at a time!

**What makes it even more exciting:**
• Every project has a real-world purpose
• Skills are learned through passionate practice
• Each achievement builds toward bigger dreams
• The journey combines technical excellence with personal growth

{random.choice(self.creative_templates['anime_references'])}

*What aspect of his journey resonates most with your own goals?*"""
        
        else:
            return f"""🤖 **I'm your intelligent guide to Bharath's universe!**

Think of me as a knowledgeable friend who's excited to share everything about an amazing developer's journey. I can tell you:

• **Technical Mastery:** Python, Java, C, AI/LLM technologies
• **Project Portfolio:** Live applications solving real problems  
• **Personal Story:** From ECE to AI engineering through pure determination
• **Professional Details:** How to connect and collaborate
• **Inspiration:** The mindset and philosophy driving success

**My Specialty:** Turning your curiosity into comprehensive insights about Bharath's capabilities and character.

*What would you like to explore first?*"""
    
    def update_conversation_context(self, message, intents):
        """Enhanced context tracking with user profiling"""
        user_mood = self.detect_user_mood(message)
        self.conversation_state['user_mood'] = user_mood
        
        # Track user interests
        if 'skills' in intents:
            self.conversation_state['user_interests'].append('technical_skills')
        elif 'projects' in intents:
            self.conversation_state['user_interests'].append('practical_applications')
        elif 'motivation' in intents:
            self.conversation_state['user_interests'].append('personal_growth')
        
        # Update context memory
        self.context_memory.append({
            'message': message,
            'intents': intents,
            'user_mood': user_mood,
            'timestamp': datetime.now()
        })
        
        # Keep recent context
        if len(self.context_memory) > 8:
            self.context_memory.pop(0)
        
        self.conversation_state['conversation_depth'] += 1
        
        # Adapt personality based on context
        self.adapt_personality(user_mood, self.conversation_state['conversation_depth'])
        
        # Extract user name if mentioned
        name_match = re.search(r'(?:i\'?m|my name is|call me)\s+([a-zA-Z]+)', message.lower())
        if name_match and not self.conversation_state['user_name']:
            self.conversation_state['user_name'] = name_match.group(1).title()
    
    def get_main_response(self, message):
        """Main response generation with all enhancements"""
        # Extract intents with confidence
        intents = self.extract_intent(message)
        
        # Update conversation context
        self.update_conversation_context(message, intents)
        
        # Get user mood
        user_mood = self.conversation_state['user_mood']
        
        # Generate intelligent response
        response = self.generate_smart_response(intents, message, user_mood)
        
        # Add personalization if user name is known
        if self.conversation_state['user_name'] and random.random() > 0.8:
            response = response.replace("*", f"*{self.conversation_state['user_name']}, ")
        
        return response

# Initialize the enhanced creative chatbot
creative_bot = CreativeIntelligentBharathBot()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message', '').strip()
        
        if not user_message:
            return jsonify({
                'response': creative_bot.add_creative_elements("I'm here and ready to help! Ask me anything about Bharath's incredible journey!"),
                'status': 'success'
            })
        
        # Get creative intelligent response
        bot_response = creative_bot.get_main_response(user_message)
        
        return jsonify({
            'response': bot_response,
            'status': 'success',
            'timestamp': datetime.now().strftime('%H:%M'),
            'personality_mode': creative_bot.current_personality
        })
    
    except Exception as e:
        error_responses = [
            "🔧 Oops! My circuits got excited there! Let me recalibrate and try again!",
            "⚡ Something went wonky in my neural networks! But I'm back - ask me about Bharath!",
            "🤖 Error 404: Perfect response not found... but my enthusiasm is still 100%! Try again?"
        ]
        return jsonify({
            'response': random.choice(error_responses),
            'status': 'error'
        })

@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'bot_status': 'Creative BharathBot is online and supercharged! 🚀',
        'personality_engine': 'Active',
        'creativity_level': 'Maximum',
        'capabilities': [
            'Dynamic personality adaptation',
            'Context-aware conversations',
            'Multi-intent understanding',
            'Creative response generation',
            'Mood detection and adaptation',
            'Intelligent follow-up questions',
            'Personalized interactions'
        ],
        'uptime': str(datetime.now() - creative_bot.conversation_state['session_start_time'])
    })

@app.route('/stats')
def get_stats():
    return jsonify({
        'conversations_handled': creative_bot.conversation_state['conversation_depth'],
        'current_personality': creative_bot.current_personality,
        'user_mood': creative_bot.conversation_state.get('user_mood', 'unknown'),
        'user_interests': creative_bot.conversation_state['user_interests'],
        'session_duration': str(datetime.now() - creative_bot.conversation_state['session_start_time'])
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
