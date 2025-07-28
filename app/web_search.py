from PyQt6.QtCore import QThread, pyqtSignal
import requests
from bs4 import BeautifulSoup
import json
import openai

class WebSearchThread(QThread):
    result_ready = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)
    
    def __init__(self, term):
        super().__init__()
        self.term = term
    
    def run(self):
        try:
            # Try Merriam-Webster first
            url = f"https://www.merriam-webster.com/medical/{self.term.lower().replace(' ', '')}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                definition = soup.find('div', class_='entry-word-section-container')
                if definition:
                    definition_text = definition.get_text(separator='\n').strip()
                    structured_info = self._get_structured_info(self.term, definition_text)
                    self.result_ready.emit(structured_info)
                    return
            
            # Fallback to MedlinePlus
            url = f"https://medlineplus.gov/ency/article/{self.term.lower().replace(' ', '')}"
            response = requests.get(url, timeout=10)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                definition = soup.find('div', id='ency_summary')
                if definition:
                    definition_text = definition.get_text(separator='\n').strip()
                    structured_info = self._get_structured_info(self.term, definition_text)
                    self.result_ready.emit(structured_info)
                    return
            
            self.error_occurred.emit("No definition found in online sources")
            
        except Exception as e:
            self.error_occurred.emit(f"Error searching online: {str(e)}")
    
    def _get_structured_info(self, term, definition_text):
        try:
            prompt = f"""Extract medical information from this text about '{term}':
            {definition_text}
            
            Return a JSON object with these fields:
            - "term": the medical term
            - "definition": concise definition
            - "symptoms": array of symptoms
            - "treatments": array of treatments
            - "prevalence": one of ["Common", "Uncommon", "Rare"]
            - "category": one of ["Cardiovascular", "Endocrine", "Neurological", 
                               "Respiratory", "Gastrointestinal", "Musculoskeletal",
                               "Infectious Disease", "Genetic", "Autoimmune"]
            
            Only return the JSON object, nothing else."""
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a medical information extractor. Return only JSON."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            result = json.loads(response.choices[0].message.content)
            result["term"] = term  # Ensure term is included
            return result
            
        except Exception as e:
            return {
                "term": term,
                "definition": definition_text[:500] + "..." if len(definition_text) > 500 else definition_text,
                "symptoms": [],
                "treatments": [],
                "prevalence": "Common",
                "category": "General"
            }