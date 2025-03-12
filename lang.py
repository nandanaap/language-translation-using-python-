import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import pygame
import speech_recognition as sr
from io import BytesIO
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile

# Initialize pygame mixer for audio playback
pygame.mixer.init()

# Language mappings
LANGUAGES = {
    "English": "en", "Hindi": "hi", "Tamil": "ta", "Telugu": "te", "Gujarati": "gu",
    "Bengali": "bn", "Punjabi": "pa", "Marathi": "mr", "Kannada": "kn", "Malayalam": "ml",
    "Urdu": "ur", "French": "fr", "Spanish": "es", "German": "de"
}

def play_welcome_message():
    """Play a welcome message using text-to-speech."""
    speak_text("Welcome to the world of multi-languages", "en")

def translate_text_generic(text, src_lang, dest_lang):
    """Translate text from source to target language."""
    try:
        translator = GoogleTranslator(source=src_lang, target=dest_lang)
        return translator.translate(text)
    except Exception as e:
        return f"Translation error: {str(e)}"

def speak_text(text, lang):
    """Convert text to speech and play it."""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        with tempfile.NamedTemporaryFile(delete=True, suffix=".mp3") as temp_audio:
            tts.save(temp_audio.name)
            pygame.mixer.music.load(temp_audio.name)
            pygame.mixer.music.play()
    except Exception as e:
        print(f"Error in TTS: {str(e)}")

def recognize_speech():
    """Recognize speech and return the text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Please speak something...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            return recognizer.recognize_google(audio)
        except sr.UnknownValueError:
            return "Sorry, I couldn't understand."
        except sr.RequestError:
            return "Error: Speech recognition service unavailable."

def open_translation_gui(mode):
    """Open the GUI for text and speech translation."""
    root = tk.Tk()
    root.title("Multi-Language Translator")
    root.state('zoomed')  # Maximize window
    
    background_label = tk.Label(root, bg="lightgray")
    background_label.place(x=0, y=0, relwidth=1, relheight=1)
    
    frame = tk.Frame(root, bg="lightpink", bd=2)
    frame.place(relx=0.5, rely=0, relwidth=0.5, relheight=1.0)
    frame.grid_columnconfigure(0, weight=1)
    
    tk.Label(frame, text="Enter Text:" if mode == "text" else "Speak:", font=("Arial", 24, "bold"))\
        .grid(row=0, column=0, padx=10, pady=20, sticky="w")
    
    text_entry = tk.Entry(frame, font=("Arial", 20), width=25) if mode == "text" else None
    if text_entry:
        text_entry.grid(row=1, column=0, padx=10, pady=10, sticky="w")
    
    tk.Label(frame, text="Source Language:", font=("Arial", 16)).grid(row=2, column=0, padx=10, pady=5, sticky="w")
    src_lang_combo = ttk.Combobox(frame, values=list(LANGUAGES.keys()), font=("Arial", 14))
    src_lang_combo.grid(row=3, column=0, padx=10, pady=5, sticky="w")
    src_lang_combo.set("English")
    
    tk.Label(frame, text="Target Language:", font=("Arial", 16)).grid(row=4, column=0, padx=10, pady=5, sticky="w")
    dest_lang_combo = ttk.Combobox(frame, values=list(LANGUAGES.keys()), font=("Arial", 14))
    dest_lang_combo.grid(row=5, column=0, padx=10, pady=5, sticky="w")
    dest_lang_combo.set("Hindi")
    
    output_label = tk.Label(frame, text="Translation will appear here.", font=("Arial", 22), bg="white")
    output_label.grid(row=7, column=0, pady=20, sticky="ew")
    
    def process_translation():
        src_lang, dest_lang = LANGUAGES[src_lang_combo.get()], LANGUAGES[dest_lang_combo.get()]
        input_text = text_entry.get() if mode == "text" else recognize_speech()
        if input_text:
            translated_text = translate_text_generic(input_text, src_lang, dest_lang)
            output_label.config(text=translated_text)
            speak_text(translated_text, dest_lang)
    
    tk.Button(frame, text="Translate" if mode == "text" else "Speak and Translate", command=process_translation,
              font=("Arial", 22, "bold"), bg="lightblue", fg="black").grid(row=6, column=0, pady=20, sticky="ew")
    
    tk.Button(frame, text="Main Menu", command=lambda: [root.destroy(), open_welcome_page(False)],
              font=("Arial", 20, "bold")).grid(row=8, column=0, pady=20, sticky="ew")
    tk.Button(frame, text="Exit", command=root.destroy, font=("Arial", 20, "bold"))\
        .grid(row=9, column=0, pady=20, sticky="ew")
    
    root.mainloop()

def open_welcome_page(play_welcome=True):
    """Open the welcome page with options for text and speech translation."""
    welcome_root = tk.Tk()
    welcome_root.title("Welcome Page")
    welcome_root.state('zoomed')
    
    tk.Label(welcome_root, bg="lightgray").place(x=0, y=0, relwidth=1, relheight=1)
    
    tk.Button(welcome_root, text="Text Translation", command=lambda: [welcome_root.destroy(), open_translation_gui("text")],
              font=("Arial", 22, "bold"), bg="lightgreen").place(relx=0.3, rely=0.5, anchor=tk.CENTER)
    tk.Button(welcome_root, text="Voice Translation", command=lambda: [welcome_root.destroy(), open_translation_gui("voice")],
              font=("Arial", 22, "bold"), bg="lightcoral").place(relx=0.7, rely=0.5, anchor=tk.CENTER)
    
    if play_welcome:
        play_welcome_message()
    
    welcome_root.mainloop()

# Start the application
open_welcome_page()