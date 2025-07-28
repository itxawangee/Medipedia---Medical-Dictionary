import sys
from PyQt6.QtWidgets import QApplication
from app.main_window import MedicalDictionaryApp

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = MedicalDictionaryApp()
    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()