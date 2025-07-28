import webbrowser
import os
from pathlib import Path
from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QLabel, 
                            QPushButton, QHBoxLayout, QMessageBox)

class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # about text
        about_text = QLabel()
        about_text.setText("""
        <h2>AI-Enhanced Medical Dictionary</h2>
        <p>Version 2.0</p>
        <p>This application provides comprehensive medical information enhanced with AI capabilities.</p>
        <p>Features include:</p>
        <ul>
            <li>Searchable medical dictionary</li>
            <li>Online medical term lookup</li>
            <li>AI-powered medical assistant</li>
            <li>Automatic categorization of terms</li>
            <li>Dynamic analytics and visualizations</li>
        </ul>
        <p>Developed for healthcare professionals, students, and curious minds.</p>
        """)
        about_text.setWordWrap(True)
        about_text.setStyleSheet("font-size: 14px; padding: 20px;")
        layout.addWidget(about_text)
        
        # Button layout
        button_layout = QHBoxLayout()
        button_layout.setContentsMargins(20, 10, 20, 20)
        
        # Documentation button
        doc_button = QPushButton("Documentation")
        doc_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        doc_button.clicked.connect(lambda: self.open_local_html("documentation.html"))
        
        # User Manual button
        manual_button = QPushButton("User Manual")
        manual_button.setStyleSheet("""
            QPushButton {
                padding: 10px;
                font-size: 14px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #f0f0f0;
            }
        """)
        manual_button.clicked.connect(lambda: self.open_local_html("manual.html"))
        
       
        
        # Add buttons to layout
        button_layout.addWidget(doc_button)
        button_layout.addWidget(manual_button)
        button_layout.addStretch()
        
        layout.addLayout(button_layout)
    
    def open_local_html(self, filename):
        """Open a local HTML file in the default web browser with proper path handling"""
        try:
            # Get the absolute path to the HTML file
            base_path = Path(__file__).parent
            file_path = (base_path / filename).resolve()
            
            # Check if file exists
            if not file_path.exists():
                raise FileNotFoundError(f"The file {filename} was not found")
                
            # Convert path to file:// URL
            file_url = file_path.as_uri()
            webbrowser.open(file_url)
            
        except Exception as e:
            QMessageBox.critical(
                self,
                "Error Opening File",
                f"Could not open {filename}:\n{str(e)}",
                QMessageBox.StandardButton.Ok
            )

    def show_about(self):
        about_text = """
        <h2>About AI-Enhanced Medical Dictionary</h2>
        <p>Version 2.0</p>
        <p>   </p>
        <p>Copyright © 2023 All Rights Reserved</p>
        <p>Contact: akrashnoor2580@gmail.com</p>
        """
        msg_box = QMessageBox()
        msg_box.setWindowTitle("About")
        msg_box.setTextFormat(1)  
        msg_box.setText(about_text)
        msg_box.setIcon(QMessageBox.Icon.Information)
        msg_box.exec()