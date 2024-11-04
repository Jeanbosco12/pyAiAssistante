import tkinter as tk
from tkinter import messagebox
from gtts import gTTS
import os
import PyPDF2
import speech_recognition as sr
import threading
import time

# Mot de passe vocal attendu
MOT_DE_PASSE_VOCAL = "ouvre"
recognizer = sr.Recognizer()

def verifier_mot_de_passe_vocal():
    with sr.Microphone() as source:
        audio = recognizer.listen(source)
    try:
        texte_reconnu = recognizer.recognize_google(audio, language="fr-FR")
        if texte_reconnu.lower() == MOT_DE_PASSE_VOCAL.lower():
            return True
        else:
            return False
    except sr.UnknownValueError:
        return False
    except sr.RequestError as e:
        print(f"Erreur de service; {e}")
        return False

def lire_pdf(chemin_fichier):
    if not os.path.exists(chemin_fichier):
        return None
    texte_complet = ""
    with open(chemin_fichier, "rb") as file:
        lecteur = PyPDF2.PdfReader(file)
        for page in lecteur.pages:
            texte = page.extract_text()
            if texte:
                texte_complet += texte + "\n"
    return texte_complet

def lire_texte_complet_avec_gtts(texte_complet, nom_fichier_entree):
    if texte_complet:
        # Extraire le nom de fichier sans extension
        nom_fichier_sans_extension = os.path.splitext(nom_fichier_entree)[0]
        # Créer le nom du fichier de sortie
        nom_fichier_sortie = f"{nom_fichier_sans_extension}.mp3"
        
        # Générer le fichier mp3
        tts = gTTS(text=texte_complet, lang='fr')
        tts.save(nom_fichier_sortie)
        
        # Jouer le fichier audio selon le système d'exploitation
        if os.name == 'posix':  # Pour Linux et macOS
            os.system(f"cvlc {nom_fichier_sortie}")
        else:  # Pour Windows
            os.system(f"start {nom_fichier_sortie}")

def animate_loading_bar():
    loading_label.config(text="Chargement...")
    root.update()
    time.sleep(0.5)
    loading_label.config(text="Chargement..")
    root.update()
    time.sleep(0.5)
    loading_label.config(text="Chargement...")
    root.update()
    time.sleep(0.5)
    loading_label.config(text="Chargement..")
    root.update()

def charger_et_lire_pdf():
    nom_pdf = entry_pdf.get()
    texte_complet = lire_pdf(nom_pdf)
    if texte_complet:
        animate_loading_bar()
        lire_texte_complet_avec_gtts(texte_complet, nom_pdf)  # Passer le nom du fichier PDF
        loading_label.config(text="")
    else:
        messagebox.showerror("Erreur", "Fichier introuvable.")

def on_button_click():
    if verifier_mot_de_passe_vocal():
        charger_et_lire_pdf()
    else:
        messagebox.showerror("Erreur", "Accès refusé.")

# Configuration de l'interface
root = tk.Tk()
root.title("AI Assistante")

# Élément d'interface
label_instruction = tk.Label(root, text="Entrez le nom du fichier PDF (avec .pdf) :")
label_instruction.pack()

entry_pdf = tk.Entry(root)
entry_pdf.pack()

button_lire = tk.Button(root, text="Lire PDF", command=on_button_click)
button_lire.pack()

loading_label = tk.Label(root, text="")
loading_label.pack()

# Boucle principale
root.mainloop()
