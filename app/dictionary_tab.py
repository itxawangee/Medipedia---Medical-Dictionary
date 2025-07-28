from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, 
                            QPushButton, QComboBox, QScrollArea, QFrame, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from app.data_handler import MedicalDataHandler
from app.web_search import WebSearchThread
from app.add_term_dialog import AddTermDialog

class DictionaryTab(QWidget):
    def __init__(self):
        super().__init__()
        self.data_handler = MedicalDataHandler()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Search area
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search medical terms...")
        self.search_input.setStyleSheet("padding: 8px; font-size: 14px;")
        self.search_input.returnPressed.connect(self.search_term)
        search_layout.addWidget(self.search_input)
        
        search_button = QPushButton("Search")
        search_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #3498db; color: white;")
        search_button.clicked.connect(self.search_term)
        search_layout.addWidget(search_button)
        
        online_search_button = QPushButton("Search Online")
        online_search_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #9b59b6; color: white;")
        online_search_button.clicked.connect(self.search_online_term)
        search_layout.addWidget(online_search_button)
        
        layout.addLayout(search_layout)
        
        # Filter by category
        filter_layout = QHBoxLayout()
        filter_layout.addWidget(QLabel("Filter by category:"))
        
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(self.data_handler.get_categories())
        self.category_filter.currentTextChanged.connect(self.search_term)
        filter_layout.addWidget(self.category_filter)
        
        layout.addLayout(filter_layout)
        
        # Results area
        results_frame = QFrame()
        results_frame.setFrameShape(QFrame.Shape.StyledPanel)
        results_layout = QVBoxLayout()
        results_frame.setLayout(results_layout)
        
        self.results_scroll = QScrollArea()
        self.results_scroll.setWidgetResizable(True)
        self.results_scroll.setWidget(results_frame)
        
        self.results_container = QWidget()
        self.results_container_layout = QVBoxLayout()
        self.results_container.setLayout(self.results_container_layout)
        results_layout.addWidget(self.results_container)
        
        layout.addWidget(self.results_scroll)
        
        # Add term button
        add_term_button = QPushButton("Add New Medical Term")
        add_term_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #2ecc71; color: white;")
        add_term_button.clicked.connect(self.show_add_term_dialog)
        layout.addWidget(add_term_button)
    
    def search_term(self):
        search_text = self.search_input.text().strip().lower()
        selected_category = self.category_filter.currentText()
        
        self.results_container_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        
        # Clear previous results
        for i in reversed(range(self.results_container_layout.count())): 
            self.results_container_layout.itemAt(i).widget().setParent(None)
        
        if search_text or selected_category != "All Categories":
            search_label = QLabel(f"Showing results for: '{search_text}'" + 
                                 (f" in category '{selected_category}'" if selected_category != "All Categories" else ""))
            search_label.setStyleSheet("font-weight: bold; font-size: 14px; padding: 10px;")
            self.results_container_layout.addWidget(search_label)
        
        found_results = False
        
        for term, details in self.data_handler.get_terms().items():
            if (search_text in term.lower() or 
                search_text in details["definition"].lower() or
                any(search_text in symptom.lower() for symptom in details["symptoms"])):
                
                if selected_category == "All Categories" or details["category"] == selected_category:
                    found_results = True
                    self.display_term_result(term, details)
        
        if not found_results:
            no_results = QLabel("No matching terms found.")
            no_results.setStyleSheet("font-size: 14px; padding: 20px; color: #7f8c8d;")
            self.results_container_layout.addWidget(no_results)
    
    def display_term_result(self, term, details):
        term_frame = QFrame()
        term_frame.setFrameShape(QFrame.Shape.StyledPanel)
        term_frame.setStyleSheet("background-color: #f8f9fa; margin: 5px; padding: 10px;")
        
        layout = QVBoxLayout()
        term_frame.setLayout(layout)
        
        term_label = QLabel(term)
        term_label.setStyleSheet("font-weight: bold; font-size: 16px; color: #2c3e50;")
        layout.addWidget(term_label)
        
        category_label = QLabel(f"Category: {details['category']}")
        category_label.setStyleSheet("font-size: 12px; color: #7f8c8d;")
        layout.addWidget(category_label)
        
        definition_label = QLabel(f"Definition: {details['definition']}")
        definition_label.setWordWrap(True)
        definition_label.setStyleSheet("font-size: 14px; margin-top: 5px;")
        layout.addWidget(definition_label)
        
        symptoms_label = QLabel("Symptoms: " + ", ".join(details["symptoms"]))
        symptoms_label.setWordWrap(True)
        symptoms_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(symptoms_label)
        
        treatments_label = QLabel("Treatments: " + ", ".join(details["treatments"]))
        treatments_label.setWordWrap(True)
        treatments_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(treatments_label)
        
        prevalence_label = QLabel(f"Prevalence: {details['prevalence']}")
        prevalence_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(prevalence_label)
        
        ai_button = QPushButton("Get AI Explanation")
        ai_button.setStyleSheet("padding: 5px; font-size: 12px; background-color: #3498db; color: white;")
        ai_button.clicked.connect(lambda: self.get_ai_explanation(term, details))
        layout.addWidget(ai_button)
        
        self.results_container_layout.addWidget(term_frame)
    
    def search_online_term(self):
        term = self.search_input.text().strip()
        if not term:
            QMessageBox.warning(self, "Error", "Please enter a term to search online")
            return
        
        self.search_thread = WebSearchThread(term)
        self.search_thread.result_ready.connect(self.handle_online_search_result)
        self.search_thread.error_occurred.connect(self.handle_online_search_error)
        self.search_thread.start()
    
    def handle_online_search_result(self, result):
        dialog = AddTermDialog(self, result)
        if dialog.exec():
            term_data = dialog.get_term_data()
            self.data_handler.add_term(term_data)
            self.search_term()
            QMessageBox.information(self, "Success", f"Term '{term_data['term']}' added successfully.")
    
    def handle_online_search_error(self, error):
        QMessageBox.warning(self, "Search Error", error)
    
    def show_add_term_dialog(self, initial_data=None):
        dialog = AddTermDialog(self, initial_data)
        if dialog.exec():
            term_data = dialog.get_term_data()
            self.data_handler.add_term(term_data)
            self.search_term()
            QMessageBox.information(self, "Success", f"Term '{term_data['term']}' added successfully.")
    
    def get_ai_explanation(self, term, details):
        # This would connect to the AI Assistant tab
        pass