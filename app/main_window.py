from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QLabel, 
                            QTabWidget, QStatusBar)
from PyQt6.QtGui import QFont
from PyQt6.QtCore import Qt, QTimer

from app.dictionary_tab import DictionaryTab
from app.ai_assistant_tab import AIAssistantTab
from app.analytics_tab import AnalyticsTab
from app.about_tab import AboutTab

class MedicalDictionaryApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("AI-Enhanced Medical Dictionary")
        self.setGeometry(100, 100, 1200, 800)
        
        # Initialize UI
        self.init_ui()
        
        # Initialize dynamic graph timer
        self.graph_timer = QTimer()
        self.graph_timer.timeout.connect(self.update_dynamic_graphs)
        self.graph_timer.start(5000)  # 5 seconds
        
    def init_ui(self):
        # Main widget and layout
        main_widget = QWidget()
        main_layout = QVBoxLayout()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        
        # Header
        header = QLabel("AI-Enhanced Medical Dictionary")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        header.setStyleSheet("color: #2c3e50; padding: 15px;")
        main_layout.addWidget(header)
        
        # Tab widget for different sections
        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)
        
        # Add tabs
        self.dictionary_tab = DictionaryTab()
        self.ai_assistant_tab = AIAssistantTab()
        self.analytics_tab = AnalyticsTab()
        self.about_tab = AboutTab()
        
        self.tabs.addTab(self.dictionary_tab, "Medical Dictionary")
        self.tabs.addTab(self.ai_assistant_tab, "AI Assistant")
        self.tabs.addTab(self.analytics_tab, "Analytics")
        self.tabs.addTab(self.about_tab, "About")
        
        # Status bar
        self.statusBar().showMessage("Ready")
    
    def update_dynamic_graphs(self):
        self.analytics_tab.update_graphs()