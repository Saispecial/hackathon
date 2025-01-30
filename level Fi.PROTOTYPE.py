import sys
import random
import speech_recognition as sr
import pyttsx3
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QTextEdit, QFrame, QProgressBar, QCheckBox
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt
import json
import google.generativeai as genai

# Configure Google Gemini API
genai.configure(api_key="AIzaSyCYSNRpsYaSBKPojYSHxNgAELZDDASusls")

# Initialize Text-to-Speech Engine
engine = pyttsx3.init()
engine.setProperty("rate", 150)  # Set speaking speed

def speak(text):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)  # Replace `1` with the desired index (0 for David, 1 for Zira, etc.)
    engine.setProperty("rate", 150)  # Adjust speaking rate if needed
    engine.say(text)
    engine.runAndWait()
    

def query_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-pro")
        response = model.generate_content(prompt)
        return response.text if response else "Error generating response."
    except Exception as e:
        return f"Error connecting to Gemini: {str(e)}"
import random

# def query_gemini(user_input):
#     # Simulated LLM response for unmatched queries
#     return f"I'm not sure about that, but here's something to think about: {user_input}"

def processConversation(user_input):
    user_input = user_input.strip().lower()
    
    intents = {
        "greet": ["hello", "hi", "hey", "greetings"],
        "morning_greet": ["good morning"],
        "afternoon_greet": ["good afternoon"],
        "evening_greet": ["good evening"],
        "night_greet": ["good night"],
        "goodbye": ["goodbye", "bye", "see you", "farewell"],
        "ask_for_motivation": ["motivate me", "i need motivation", "give me motivation", "inspire me"],
        "ask_for_tip": ["give me a tip", "i need a productivity tip", "how can i be more productive"],
        "tell_about_solo_leveling": ["tell me about solo leveling", "what is solo leveling"],
        "mood_great": ["i feel great", "i'm happy", "i feel good"],
        "mood_unhappy": ["i feel sad", "i'm unhappy", "i'm down"],
        "affirm": ["yes", "sure", "yep"],
        "deny": ["no", "not really", "nope"]
    }

    responses = {
        "utter_greet": ["Hello! How can I assist you today?", "Hi there! What can I help you level up with today?"],
        "utter_morning_greet": ["Good morning! Ready to start leveling up today?"],
        "utter_afternoon_greet": ["Good afternoon! How can I help you level up this afternoon?"],
        "utter_evening_greet": ["Good evening! Ready for some evening productivity?"],
        "utter_night_greet": ["Good night! Rest well and be ready to level up tomorrow!"],
        "utter_goodbye": ["Goodbye! Have a great day leveling up!"],
        "utter_solo_leveling_motivation": [
            "Remember, even the strongest characters in Solo Leveling faced challenges. Keep pushing forward!"
        ],
        "utter_productivity_tip": [
            "Break tasks into smaller chunks and take regular breaks."
        ],
        "utter_solo_leveling_info": [
            "Solo Leveling is a popular webtoon about a weak hunter who gains incredible powers. Would you like to know more?"
        ],
        "utter_happy": ["I'm glad to hear you're feeling great!"],
        "utter_cheer_up": [
            "I'm sorry to hear that. Let's try to find something positive."
        ],
        "utter_did_that_help": ["Did that help you feel better?"]
    }

    matched_intent = None
    for intent, phrases in intents.items():
        if any(phrase in user_input for phrase in phrases):
            matched_intent = intent
            break
        
    if matched_intent:
        if matched_intent == "greet":
            return random.choice(responses["utter_greet"])
        elif matched_intent == "morning_greet":
            return random.choice(responses["utter_morning_greet"])
        elif matched_intent == "afternoon_greet":
            return random.choice(responses["utter_afternoon_greet"])
        elif matched_intent == "evening_greet":
            return random.choice(responses["utter_evening_greet"])
        elif matched_intent == "night_greet":
            return random.choice(responses["utter_night_greet"])
        elif matched_intent == "goodbye":
            return random.choice(responses["utter_goodbye"])
        elif matched_intent == "ask_for_motivation":
            return random.choice(responses["utter_solo_leveling_motivation"])
        elif matched_intent == "ask_for_tip":
            return random.choice(responses["utter_productivity_tip"])
        elif matched_intent == "tell_about_solo_leveling":
            return random.choice(responses["utter_solo_leveling_info"])
        elif matched_intent == "mood_great":
            return random.choice(responses["utter_happy"])
        elif matched_intent == "mood_unhappy":
            return random.choice(responses["utter_cheer_up"]) + " " + random.choice(responses["utter_did_that_help"])
        elif matched_intent == "affirm":
            return random.choice(responses["utter_happy"])
        elif matched_intent == "deny":
            return random.choice(responses["utter_goodbye"])
    
    for intent, phrases in intents.items():
        if any(phrase in user_input for phrase in phrases):
            return random.choice(responses.get(f"utter_{intent}", []))
    return query_gemini(user_input)

class AccountManager:
    def __init__(self):
        self.accounts = self.load_accounts()

    def load_accounts(self):
        try:
            with open('accounts.json', 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            return {}

    def save_accounts(self):
        with open('accounts.json', 'w') as f:
            json.dump(self.accounts, f)

    def create_account(self, username, password):
        if username in self.accounts:
            return False
        self.accounts[username] = password
        self.save_accounts()
        return True

    def verify_account(self, username, password):
        return self.accounts.get(username) == password


class LoginPage(QWidget):
    def __init__(self, account_manager, on_login):
        super().__init__()
        self.account_manager = account_manager
        self.on_login = on_login
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Login")
        self.setGeometry(200, 200, 400, 300)

        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)
        layout.addWidget(self.login_button)

        self.create_account_button = QPushButton("Create Account", self)
        self.create_account_button.clicked.connect(self.create_account)
        layout.addWidget(self.create_account_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.account_manager.verify_account(username, password):
            self.on_login(username)
            self.close()
        else:
            speak("Login failed. Incorrect username or password.")

    def create_account(self):
        username = self.username_input.text()
        password = self.password_input.text()

        if self.account_manager.create_account(username, password):
            speak("Account created successfully! You can now log in.")
        else:
            speak("Account creation failed. Username already exists.")

# Initialize Speech Recognition
recognizer = sr.Recognizer()

class SoloLevelingAssistantApp(QWidget):
    def __init__(self, username):
        super().__init__()
        self.username = username
        self.user_level = 1
        self.strength = 5
        self.intelligence = 5
        self.xp = 0
        self.daily_tasks = []
        self.task_checkboxes = []
        self.initUI()
        self.generateDailyTasks()

    def initUI(self):
        self.setWindowTitle("Solo Leveling AI Assistant")
        self.setGeometry(200, 200, 800, 600)
        self.setStyleSheet("background-color: #1e1e2e; color: #f0f0f5;")

        main_layout = QHBoxLayout()
        sidebar = QVBoxLayout()
        sidebar.setContentsMargins(10, 10, 10, 10)

        # Daily Tasks Section
        daily_tasks_label = QLabel("Daily Tasks")
        daily_tasks_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        sidebar.addWidget(daily_tasks_label)

        self.task_checkboxes_layout = QVBoxLayout()
        sidebar.addLayout(self.task_checkboxes_layout)

        submit_tasks_button = QPushButton("Submit Completed Tasks")
        submit_tasks_button.setFont(QFont("Helvetica", 12))
        submit_tasks_button.clicked.connect(self.submitTasks)
        sidebar.addWidget(submit_tasks_button)



    
        # Level and XP Section
        self.level_label = QLabel(f"Level: {self.user_level}")
        self.level_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        sidebar.addWidget(self.level_label)

        self.xp_bar = QProgressBar()
        self.xp_bar.setRange(0, 1000)
        self.xp_bar.setValue(self.xp)
        self.xp_bar.setStyleSheet("QProgressBar { text-align: center; }")
        sidebar.addWidget(self.xp_bar)

        # Attribute Points Section
        points_table_label = QLabel("Attribute Points")
        points_table_label.setFont(QFont("Helvetica", 14, QFont.Bold))
        sidebar.addWidget(points_table_label)

        self.strength_label = QLabel(f"Strength: {self.strength}")
        self.strength_label.setFont(QFont("Helvetica", 12))
        sidebar.addWidget(self.strength_label)

        increase_strength_button = QPushButton("Increase Strength")
        increase_strength_button.setFont(QFont("Helvetica", 12))
        increase_strength_button.clicked.connect(lambda: self.increaseAttribute("strength"))
        sidebar.addWidget(increase_strength_button)

        self.intelligence_label = QLabel(f"Intelligence: {self.intelligence}")
        self.intelligence_label.setFont(QFont("Helvetica", 12))
        sidebar.addWidget(self.intelligence_label)

        increase_intelligence_button = QPushButton("Increase Intelligence")
        increase_intelligence_button.setFont(QFont("Helvetica", 12))
        increase_intelligence_button.clicked.connect(lambda: self.increaseAttribute("intelligence"))
        sidebar.addWidget(increase_intelligence_button)

        # Divider and Content Area
        divider = QFrame()
        divider.setFrameShape(QFrame.VLine)
        divider.setFrameShadow(QFrame.Sunken)
        main_layout.addLayout(sidebar)
        main_layout.addWidget(divider)

        content_area = QVBoxLayout()

        title = QLabel("Solo Leveling AI Assistant")
        title.setFont(QFont("Helvetica", 18, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        content_area.addWidget(title)

        self.chat_input = QLineEdit(self)
        self.chat_input.setPlaceholderText("Ask something... (e.g., 'What is my level')")
        self.chat_input.setFont(QFont("Helvetica", 12))
        content_area.addWidget(self.chat_input)

        chat_button = QPushButton("Chat", self)
        chat_button.setFont(QFont("Helvetica", 12, QFont.Bold))
        chat_button.clicked.connect(self.chatWithAI)
        content_area.addWidget(chat_button)

        voice_button = QPushButton("Speak", self)
        voice_button.setFont(QFont("Helvetica", 12, QFont.Bold))
        voice_button.clicked.connect(self.speakWithAI)
        content_area.addWidget(voice_button)

        self.response_display = QTextEdit(self)
        self.response_display.setFont(QFont("Helvetica", 12))
        self.response_display.setReadOnly(True)
        content_area.addWidget(self.response_display)

        main_layout.addLayout(content_area)
        self.setLayout(main_layout)

    def generateDailyTasks(self):
        tasks = [
            "Complete maths exercises", "Exercise for 15 minutes",
            "Read a strategy book", "Practice meditation",
            "Write a journal entry", "Complete a coding challenge"
        ]
        self.daily_tasks = random.sample(tasks, 3)
        for checkbox in self.task_checkboxes:
            checkbox.deleteLater()
        self.task_checkboxes = []
        for task in self.daily_tasks:
            checkbox = QCheckBox(task, self)
            self.task_checkboxes.append(checkbox)
            self.task_checkboxes_layout.addWidget(checkbox)

    def submitTasks(self):
        completed_tasks = sum(checkbox.isChecked() for checkbox in self.task_checkboxes)
        xp_earned = completed_tasks * 200
        self.xp += xp_earned

        if xp_earned > 0:
            self.displayResponse(f"Great job! You earned {xp_earned} XP for completing tasks.")
            speak(f"Great job! You earned {xp_earned} XP for completing tasks.")
        else:
            speak("No tasks completed. Try again.")

        if self.xp >= 1000:
            self.levelUp()

    # Set XP progress bar within current level
        self.xp_bar.setValue(self.xp % 1000)

    # Generate new daily tasks if XP is below threshold for a level-up
        if self.xp < 1000:
            self.generateDailyTasks()


    def levelUp(self):
        self.user_level += 1
        self.xp -= 1000
        self.level_label.setText(f"Level: {self.user_level}")
        self.xp_bar.setValue(self.xp % 1000)
        self.generateDailyTasks()
        self.displayResponse("Level up! Congratulations!")
        speak("Level up! Congratulations!")

    def increaseAttribute(self, attribute):
        if attribute == "strength":
            self.strength += 1
            self.strength_label.setText(f"Strength: {self.strength}")
        elif attribute == "intelligence":
            self.intelligence += 1
            self.intelligence_label.setText(f"Intelligence: {self.intelligence}")
        speak(f"{attribute.capitalize()} increased!")

    def chatWithAI(self):
        user_input = self.chat_input.text()
        response = processConversation(user_input)
        self.displayResponse(response)
        speak(response)
    def speakWithAI(self):
        with sr.Microphone() as source:
            recognizer.adjust_for_ambient_noise(source)
            audio = recognizer.listen(source)
        try:
            user_input = recognizer.recognize_google(audio)
            self.displayResponse(f"You said: {user_input}")
            response = processConversation(user_input)
            self.displayResponse(response)
            speak(response)
        except sr.UnknownValueError:
            self.displayResponse("Sorry, I didn't catch that.")
        except sr.RequestError:
            self.displayResponse("Speech Recognition API is unavailable.")

    def displayResponse(self, response):
        self.response_display.append(response)
        self.chat_input.clear()

# Define app_window globally
app_window = None

def on_login(username):
    global app_window
    app_window = SoloLevelingAssistantApp(username)
    app_window.show()

def main():
    app = QApplication(sys.argv)

    account_manager = AccountManager()

    login_page = LoginPage(account_manager, on_login)
    login_page.show()

    sys.exit(app.exec_())  # Ensure the app continues running

if __name__ == "__main__":
    main()
