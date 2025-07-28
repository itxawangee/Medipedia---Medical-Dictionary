from PyQt6.QtWidgets import (QDialog, QFormLayout, QLineEdit, QTextEdit, 
                            QComboBox, QDialogButtonBox, QMessageBox)

class AddTermDialog(QDialog):
    def __init__(self, parent=None, initial_data=None):
        super().__init__(parent)
        self.setWindowTitle("Add New Medical Term")
        self.layout = QFormLayout()
        self.setLayout(self.layout)
        
        # Initialize form fields
        self.term_input = QLineEdit()
        self.definition_input = QTextEdit()
        self.definition_input.setMaximumHeight(100)
        self.symptoms_input = QLineEdit()
        self.symptoms_input.setPlaceholderText("Comma-separated list")
        self.treatments_input = QLineEdit()
        self.treatments_input.setPlaceholderText("Comma-separated list")
        self.prevalence_combo = QComboBox()
        self.prevalence_combo.addItems(["Common", "Uncommon", "Rare"])
        self.category_combo = QComboBox()
        
        # Get categories from parent if available
        if parent and hasattr(parent, 'data_handler'):
            self.category_combo.addItems(parent.data_handler.get_categories())
        else:
            self.category_combo.addItems(["Cardiovascular", "Endocrine", "Neurological", 
                                       "Respiratory", "Gastrointestinal", "Musculoskeletal",
                                       "Infectious Disease", "Genetic", "Autoimmune", "General"])
        
        # Pre-fill if initial data provided
        if initial_data:
            self.term_input.setText(initial_data.get("term", ""))
            self.definition_input.setPlainText(initial_data.get("definition", ""))
            self.symptoms_input.setText(", ".join(initial_data.get("symptoms", [])))
            self.treatments_input.setText(", ".join(initial_data.get("treatments", [])))
            self.prevalence_combo.setCurrentText(initial_data.get("prevalence", "Common"))
            self.category_combo.setCurrentText(initial_data.get("category", "General"))
        
        # Add fields to form
        self.layout.addRow("Term:", self.term_input)
        self.layout.addRow("Definition:", self.definition_input)
        self.layout.addRow("Symptoms:", self.symptoms_input)
        self.layout.addRow("Treatments:", self.treatments_input)
        self.layout.addRow("Prevalence:", self.prevalence_combo)
        self.layout.addRow("Category:", self.category_combo)
        
        # Buttons
        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        buttons.accepted.connect(self.validate_and_accept)
        buttons.rejected.connect(self.reject)
        self.layout.addRow(buttons)
    
    def validate_and_accept(self):
        term = self.term_input.text().strip()
        if not term:
            QMessageBox.warning(self, "Error", "Term name cannot be empty.")
            return
        
        self.accept()
    
    def get_term_data(self):
        return {
            "term": self.term_input.text().strip(),
            "definition": self.definition_input.toPlainText().strip(),
            "symptoms": [s.strip() for s in self.symptoms_input.text().split(",") if s.strip()],
            "treatments": [t.strip() for t in self.treatments_input.text().split(",") if t.strip()],
            "prevalence": self.prevalence_combo.currentText(),
            "category": self.category_combo.currentText()
        }