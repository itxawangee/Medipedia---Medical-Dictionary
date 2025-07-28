import json
from pathlib import Path

class MedicalDataHandler:
    def __init__(self):
        self.data_file = Path("medical_database.json")
        self.medical_data = self._load_data()
    
    def _load_data(self):
        try:
            with open(self.data_file, "r") as f:
                data = json.load(f)
                if "terms" not in data:
                    data["terms"] = {}
                if "categories" not in data:
                    data["categories"] = self._default_categories()
                return data
        except (FileNotFoundError, json.JSONDecodeError):
            return {
                "terms": self._sample_terms(),
                "categories": self._default_categories()
            }
    
    def _default_categories(self):
        return ["Cardiovascular", "Endocrine", "Neurological", 
                "Respiratory", "Gastrointestinal", "Musculoskeletal",
                "Infectious Disease", "Genetic", "Autoimmune", "General"]
    
    def _sample_terms(self):
        return {
            "Hypertension": {
                "definition": "A condition of abnormally high blood pressure.",
                "symptoms": ["Headache", "Dizziness", "Blurred vision"],
                "treatments": ["Lifestyle changes", "Medications"],
                "prevalence": "Common",
                "category": "Cardiovascular"
            },
            "Diabetes": {
                "definition": "A metabolic disease causing high blood sugar.",
                "symptoms": ["Increased thirst", "Frequent urination", "Fatigue"],
                "treatments": ["Insulin therapy", "Diet management"],
                "prevalence": "Common",
                "category": "Endocrine"
            }
        }
    
    def save_data(self):
        with open(self.data_file, "w") as f:
            json.dump(self.medical_data, f, indent=4)
    
    def get_terms(self):
        return self.medical_data["terms"]
    
    def get_categories(self):
        return self.medical_data["categories"]
    
    def add_term(self, term_data):
        term = term_data["term"]
        self.medical_data["terms"][term] = {
            "definition": term_data["definition"],
            "symptoms": term_data["symptoms"],
            "treatments": term_data["treatments"],
            "prevalence": term_data["prevalence"],
            "category": term_data["category"]
        }
        
        if term_data["category"] not in self.medical_data["categories"]:
            self.medical_data["categories"].append(term_data["category"])
        
        self.save_data()