from PyQt6.QtWidgets import QWidget, QVBoxLayout, QPushButton
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from datetime import datetime

class AnalyticsTab(QWidget):
    def __init__(self):
        super().__init__()
        self.figure = Figure(figsize=(10, 8), dpi=100)
        self.canvas = FigureCanvas(self.figure)
        self.init_ui()
        self.update_graphs()
    
    def init_ui(self):
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        layout.addWidget(self.canvas)
        
        refresh_button = QPushButton("Refresh Analytics")
        refresh_button.setStyleSheet("padding: 8px; font-size: 14px; background-color: #3498db; color: white;")
        refresh_button.clicked.connect(self.update_graphs)
        layout.addWidget(refresh_button)
    
    def update_graphs(self):
        self.figure.clear()
        
        # Create subplots
        ax1 = self.figure.add_subplot(221)
        ax2 = self.figure.add_subplot(222)
        ax3 = self.figure.add_subplot(223)
        ax4 = self.figure.add_subplot(224)
        
        # Sample data for demonstration
        categories = ["Cardiovascular", "Endocrine", "Neurological", "Respiratory"]
        category_counts = [15, 8, 12, 5]
        
        treatment_types = ["Medication", "Surgery", "Therapy", "Lifestyle"]
        treatment_counts = [25, 10, 15, 20]
        
        prevalences = ["Common", "Uncommon", "Rare"]
        prevalence_counts = [30, 15, 5]
        
        dates = [datetime(2024, 1, 1), datetime(2024, 4, 1), 
                datetime(2024, 7, 1), datetime(2024, 10, 1), 
                datetime(2025, 1, 1)]
        counts = [5, 15, 25, 35, 50]
        
        # Plot 1: Terms by category
        ax1.bar(categories, category_counts, color='skyblue')
        ax1.set_title("Medical Terms by Category")
        ax1.tick_params(axis='x', rotation=45)
        
        # Plot 2: Treatment types distribution
        ax2.pie(treatment_counts, labels=treatment_types, autopct='%1.1f%%', startangle=90)
        ax2.set_title("Treatment Types Distribution")
        
        # Plot 3: Prevalence of conditions
        ax3.barh(prevalences, prevalence_counts, color='lightgreen')
        ax3.set_title("Prevalence of Conditions")
        
        # Plot 4: Term addition timeline
        ax4.plot(dates, counts, marker='o', color='orange')
        ax4.set_title("Term Addition Timeline")
        ax4.tick_params(axis='x', rotation=45)
        
        self.figure.tight_layout()
        self.canvas.draw()