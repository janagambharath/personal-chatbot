
from flask import Flask, render_template, request, jsonify
from transformers import pipeline, AutoTokenizer, AutoModelForCausalLM
import torch
import json
import re
from datetime import datetime

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

# Initialize the chatbot model
class PersonalChatbot:
    def __init__(self):
        try:
            # Using a lightweight model for better performance
            model_name = "microsoft/DialoGPT-small"
            self.tokenizer = AutoTokenizer.from_pretrained(model_name)
            self.model = AutoModelForCausalLM.from_pretrained(model_name)
            
            # Add padding token if not present
            if self.tokenizer.pad_token is None:
                self.tokenizer.pad_token = self.tokenizer.eos_token
                
            self.chat_history_ids = None
            print("Chatbot model loaded successfully!")
            
        except Exception as e:
            print(f"Error loading model: {e}")
            # Fallback to a simple rule-based system
            self.model = None
            self.tokenizer = None
    
    def get_personal_response(self, message):
        """Generate smart, engaging responses based on Bharath's personal information"""
        message_lower = message.lower()
        
        # 1. Personal Introduction - Enhanced
        if any(word in message_lower for word in ["who are you", "introduce", "about bharath"]):
            return "Hey! I'm BharathBot 🤖, created by Janagam Bharath. Ask me anything about his skills, projects, or how he's building his tech journey!\n\nI can help you explore his background, current work, and even connect you with him directly!"
        
        elif any(word in message_lower for word in ["name"]) and not any(word in message_lower for word in ["skills", "projects"]):
            return f"Hi! I'm {PERSONAL_INFO['name']}, an aspiring LLM Engineer and Python developer from {PERSONAL_INFO['location']}. I'm passionate about building AI-powered tools and web applications!"
        
        # 2. Quick Skill Summary - Enhanced
        elif any(word in message_lower for word in ["what skills", "skills does bharath", "technical skills", "programming skills"]):
            return """Here's a quick overview:

🐍 **Programming:** Python, Java, C
🌐 **Web Development:** HTML, CSS, Flask  
🧠 **AI/LLM:** Chatbot & LLM development
🛠️ **Tools:** Git, GitHub, Render, Termux

Ask me about any of these and I'll explain more! 💪"""
        
        elif any(word in message_lower for word in ["skills", "languages", "programming", "code"]) and not any(word in message_lower for word in ["what skills"]):
            languages = ", ".join(PERSONAL_INFO['languages'])
            web_tech = ", ".join(PERSONAL_INFO['web_tech'])
            return f"**Programming Languages:** {languages}\n**Web Technologies:** {web_tech}\n**AI/ML:** {', '.join(PERSONAL_INFO['ai_tech'])}\n**Tools:** {', '.join(PERSONAL_INFO['tools'])}\n\n💡 Want to know more about any specific technology?"
        
        # 3. Project Highlight - Enhanced
        elif any(word in message_lower for word in ["show me project", "portfolio projects", "what projects"]):
            return """🚀 **Current Project Highlight:**
Bharath is building an AI-powered chatbot using Flask + HuggingFace (like me!)

You can explore more projects on his portfolio 👉 bharath-portfolio-otas.onrender.com

Want to know more about his development process? Just ask! 💻"""
        
        elif any(word in message_lower for word in ["projects", "building", "working on", "current"]):
            projects = '\n• '.join(PERSONAL_INFO['current_projects'])
            return f"**Currently working on:**\n• {projects}\n\n🔥 Each project is a step toward mastering AI and web development!"
        
        # 4. Resume Download Tip
        elif any(word in message_lower for word in ["download resume", "resume download", "can i download", "resume"]):
            return """📄 **Yes! You can download Bharath's resume!**

Click the **Resume** button on the portfolio site to download the latest version.
👉 bharath-portfolio-otas.onrender.com

It includes all his projects, skills, and contact information! 📋"""
        
        # 5. Contact Tip - Enhanced
        elif any(word in message_lower for word in ["how can i contact", "contact bharath", "email", "reach bharath"]):
            return """📬 **You can reach Bharath directly at:**

📧 **Email:** janagambharath1107@gmail.com
💼 **LinkedIn:** linkedin.com/in/janagam-bharath-9ab1b335b
💻 **GitHub:** github.com/janagambharath
🌐 **Portfolio:** bharath-portfolio-otas.onrender.com

He's always excited to connect with fellow tech enthusiasts! 🤝"""
        
        # 6. Learning Journey - Enhanced  
        elif any(word in message_lower for word in ["what is bharath learning", "current focus", "learning journey", "studying"]):
            return """📚 **He's currently focused on:**

🔸 **Mastering Flask** - Building robust web applications
🔸 **Exploring LLM Engineering** - The future of AI development  
🔸 **Strengthening DSA in C** - Solid programming fundamentals

Ask about any topic and I can share what he's doing! 🚀"""
        
        # 7. Motivation Quote
        elif any(word in message_lower for word in ["motivate me", "quote", "inspiration", "motivation"]):
            return """✨ **Here's some motivation from Bharath:**

> *"Discipline today builds the future you want tomorrow."* – Bharath

🔥 He deleted social media 100+ days ago to focus entirely on his tech career. That's the power of commitment! 

What's your next step toward your goals? 💪"""
        
        # 8. Chatbot Abilities - Enhanced
        elif any(word in message_lower for word in ["what can you do", "help", "abilities", "how can you help"]):
            return """🤖 **I can help you with:**

✅ Learn about Bharath's skills & background
✅ Share his resume and portfolio  
✅ List his current projects
✅ Explain technologies he works with
✅ Connect you with him directly
✅ Share his learning journey & motivation

**Try asking:** "What projects is Bharath working on?" or "How can I contact him?" 💬"""
        
        # 9. All-in-One Links - Enhanced
        elif any(word in message_lower for word in ["give me all links", "bharath's links", "all links", "social links"]):
            contact = PERSONAL_INFO['contact']
            return f"""🔗 **Here you go - All of Bharath's links:**

🌐 **Portfolio:** {contact['portfolio']}
📄 **Resume:** Available on portfolio  
💼 **LinkedIn:** {contact['linkedin']}
💻 **GitHub:** {contact['github']}
📧 **Email:** {contact['email']}

Bookmark these to stay connected! 🚀"""
        
        # 10. Navigation Tip
        elif any(word in message_lower for word in ["how to explore portfolio", "portfolio help", "navigate portfolio"]):
            return """🧭 **Portfolio Navigation Tip:**

Use the **sidebar** on the portfolio to easily view:
• **About** - His background & journey
• **Projects** - Live demos & code  
• **Resume** - Download latest version
• **Contact** - Get in touch directly

It's designed to be smooth and responsive! 📱💻"""
        
        # Enhanced existing responses
        elif any(word in message_lower for word in ["age", "old", "student"]):
            return f"Bharath is currently pursuing {PERSONAL_INFO['current_study']}, with a strong self-taught foundation in computer science. Age is just a number when you're focused on growth! 🌱"
        
        elif any(word in message_lower for word in ["where", "location", "live", "from"]):
            return f"📍 Based in {PERSONAL_INFO['location']}, coming from a middle-class family that motivates him to work hard every day. Hyderabad has a great tech scene! 🏙️"
        
        elif any(word in message_lower for word in ["job", "work", "profession", "career", "what do you do"]):
            return f"🎯 He's an {PERSONAL_INFO['profession']}. Currently {PERSONAL_INFO['current_study']} while building real-world AI and web development skills!"
        
        elif any(word in message_lower for word in ["education", "study", "school", "diploma", "ece"]):
            return f"🎓 {PERSONAL_INFO['education']}. He's transitioning from ECE to Computer Science - proving that passion and dedication can reshape your path!"
        
        elif any(word in message_lower for word in ["interests", "hobbies", "like", "enjoy", "passionate"]):
            return f"❤️ **Passionate about:** {', '.join(PERSONAL_INFO['interests'][:4])}\n\n🍃 He also loves anime like One Piece and Naruto - they taught him to turn pain into purpose!"
        
        elif any(word in message_lower for word in ["mission", "goal", "purpose", "future"]):
            return f"🎯 **His Mission:** {PERSONAL_INFO['mission']}\n\nIt's not just about coding - it's about making a meaningful impact! 💫"
        
        elif any(word in message_lower for word in ["anime", "one piece", "naruto", "inspiration"]):
            return f"🍃 {PERSONAL_INFO['inspiration']}! These shows taught him that with determination and hard work, you can overcome any obstacle.\n\n*'I'll become the Pirate King!'* - That's the energy he brings to coding! 🏴‍☠️"
        
        elif any(word in message_lower for word in ["social media", "focus", "discipline", "deleted"]):
            return "📵 **100+ days social media free!** That's the level of commitment to his tech career.\n\n*'Discipline and deep learning over distractions'* - That's his motto! 🎯"
        
        elif any(word in message_lower for word in ["family", "parents", "background"]):
            return f"👨‍👩‍👦 Coming from a middle-class family in Hyderabad, his biggest motivation is making his parents proud through tech.\n\nFamily support + personal drive = Unstoppable! 💪"
        
        elif any(word in message_lower for word in ["flask", "python", "ai", "llm", "huggingface"]):
            return "🤖 **AI Development Focus:** Building chatbots with Python, Flask, and HuggingFace!\n\nCurrently learning LLM engineering step-by-step. The future is AI, and he's preparing for it! 🚀"
        
        elif any(word in message_lower for word in ["hello", "hi", "hey", "namaste"]):
            return f"👋 Hello! I'm BharathBot, representing {PERSONAL_INFO['name']} - an aspiring LLM Engineer from Hyderabad!\n\n🚀 Ask me about his journey, projects, skills, or what drives him to code every day!"
        
        elif any(word in message_lower for word in ["dsa", "data structures", "algorithms", "c programming"]):
            return "📊 **DSA in C:** Building rock-solid programming fundamentals!\n\nStrong foundations lead to advanced mastery. Every algorithm learned is a problem-solving tool gained! 🧠"
        
        elif any(word in message_lower for word in ["render", "deployment", "hosting"]):
            return "☁️ **Deployment Platform:** Using Render for hosting projects!\n\nCheck out his live portfolio at bharath-portfolio-otas.onrender.com to see his work in action! 🌐"
        
        return None
    
    def generate_response(self, message):
        # First try to get a personal response
        personal_response = self.get_personal_response(message)
        if personal_response:
            return personal_response
        
        # If no model is loaded, use fallback responses
        if not self.model or not self.tokenizer:
            return "I'm sorry, I didn't quite understand that. Try asking me about my background, skills, experience, or interests!"
        
        try:
            # Encode the message and chat history
            new_user_input_ids = self.tokenizer.encode(
                message + self.tokenizer.eos_token, return_tensors='pt'
            )
            
            # Append to chat history
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_user_input_ids], dim=-1)
            else:
                bot_input_ids = new_user_input_ids
            
            # Generate response
            with torch.no_grad():
                self.chat_history_ids = self.model.generate(
                    bot_input_ids,
                    max_length=1000,
                    num_beams=3,
                    no_repeat_ngram_size=3,
                    do_sample=True,
                    temperature=0.7,
                    pad_token_id=self.tokenizer.eos_token_id
                )
            
            # Decode the response
            response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                skip_special_tokens=True
            )
            
            return response if response else "I'm not sure how to respond to that. Ask me about my background!"
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "I'm having trouble generating a response right now. Try asking me about my background, skills, or experience!"

# Initialize chatbot
chatbot = PersonalChatbot()

@app.route('/')
def home():
    return render_template('index.html', personal_info=PERSONAL_INFO)

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        user_message = data.get('message', '').strip()
        
        if not user_message:
            return jsonify({'error': 'No message provided'}), 400
        
        # Generate response
        response = chatbot.generate_response(user_message)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({'error': 'Sorry, I encountered an error. Please try again.'}), 500

@app.route('/reset', methods=['POST'])
def reset_chat():
    """Reset chat history"""
    global chatbot
    if chatbot.model:
        chatbot.chat_history_ids = None
    return jsonify({'status': 'Chat history reset'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
