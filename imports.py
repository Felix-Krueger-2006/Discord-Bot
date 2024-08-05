import sys
import os

# Den Pfad zum 'module' Verzeichnis hinzufügen
aktueller_pfad = os.path.dirname(os.path.abspath(__file__))
module_verzeichnis = os.path.join(aktueller_pfad, 'module')
sys.path.append(module_verzeichnis)

# Modul importieren
import main