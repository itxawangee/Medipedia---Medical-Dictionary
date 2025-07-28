from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTextEdit, 
                            QLineEdit, QPushButton, QLabel)
from PyQt6.QtCore import Qt
import openai

class AIAssistantTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # AI Chat area
        ai_layout = QVBoxLayout()
        
        self.ai_chat_display = QTextEdit()
        self.ai_chat_display.setReadOnly(True)
        self.ai_chat_display.setStyleSheet("padding: 6px; font-size: 14px;")
        ai_layout.addWidget(self.ai_chat_display)
        
        self.ai_chat_input = QLineEdit()
        self.ai_chat_input.setPlaceholderText("Ask the AI medical assistant...")
        self.ai_chat_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.ai_chat_input.returnPressed.connect(self.query_ai_assistant)
        ai_layout.addWidget(self.ai_chat_input)
        
        ai_button_layout = QHBoxLayout()
        
        send_button = QPushButton("Send")
        send_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #3498db; color: white;")
        send_button.clicked.connect(self.query_ai_assistant)
        ai_button_layout.addWidget(send_button)
        
        clear_button = QPushButton("Clear")
        clear_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #e74c3c; color: white;")
        clear_button.clicked.connect(self.clear_ai_chat)
        ai_button_layout.addWidget(clear_button)
        
        ai_layout.addLayout(ai_button_layout)
        
        layout.addLayout(ai_layout)
        
        # Quick prompts
        prompt_layout = QHBoxLayout()
        prompt_layout.addWidget(QLabel("Quick prompts:"))
        
        prompt1 = QPushButton("Explain like I'm 5")
        prompt1.setStyleSheet("padding: 5px; font-size: 12px;")
        prompt1.clicked.connect(lambda: self.set_ai_prompt("Explain this medical concept in simple terms as if I'm 5 years old:"))
        prompt_layout.addWidget(prompt1)
        
        prompt2 = QPushButton("Latest treatments")
        prompt2.setStyleSheet("padding: 5px; font-size: 12px;")
        prompt2.clicked.connect(lambda: self.set_ai_prompt("What are the latest treatment options for"))
        prompt_layout.addWidget(prompt2)
        
        prompt3 = QPushButton("Differential diagnosis")
        prompt3.setStyleSheet("padding: 5px; font-size: 12px;")
        prompt3.clicked.connect(lambda: self.set_ai_prompt("What are possible differential diagnoses for symptoms including"))
        prompt_layout.addWidget(prompt3)
        
        layout.addLayout(prompt_layout)
    
    def query_ai_assistant(self):
        query = self.ai_chat_input.text().strip()
        if not query:
            return
        
        self.ai_chat_display.append(f"<b>User:</b> {query}")
        self.ai_chat_input.clear()
        
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": """You are a medical AI assistant. Provide accurate, 
                    up-to-date medical information. For complex cases, always recommend consulting 
                    a healthcare professional. Be clear and concise in your explanations."""},
                    {"role": "user", "content": query}
                ],
                temperature=0.7,
                max_tokens=500
            )
            
            ai_response = response.choices[0].message.content
            self.ai_chat_display.append(f"<b>AI Assistant:</b> {ai_response}")
            
        except Exception as e:
            self.ai_chat_display.append(f"<b>Error:</b> Could not get AI response. {str(e)}")
    
    def clear_ai_chat(self):
        self.ai_chat_display.clear()
    
    def set_ai_prompt(self, prompt):
        self.ai_chat_input.setText(prompt)
        self.ai_chat_input.setFocus()