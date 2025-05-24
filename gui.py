import tkinter as tk
from tkinter import scrolledtext
from nlu import parse_command
from automation import execute_plan
import threading
import speech_recognition as sr

class WebAgentGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("AI Web Automation Agent")
        self.root.geometry("600x400")

        self.input_label = tk.Label(root, text="Enter command:")
        self.input_label.pack(pady=5)

        self.input_entry = tk.Entry(root, width=80)
        self.input_entry.pack(pady=5)
        self.input_entry.bind('<Return>', self.on_submit)

        frame = tk.Frame(root)
        frame.pack(pady=5)
        self.submit_button = tk.Button(frame, text="Submit", command=self.on_submit)
        self.submit_button.pack(side=tk.LEFT, padx=5)
        self.speak_button = tk.Button(frame, text="🎤 Speak", command=self.on_speak)
        self.speak_button.pack(side=tk.LEFT, padx=5)

        self.output_area = scrolledtext.ScrolledText(root, width=70, height=18, state='disabled')
        self.output_area.pack(pady=10)

    def on_submit(self, event=None):
        command = self.input_entry.get()
        if command.strip():
            self.input_entry.delete(0, tk.END)
            self.log(f"> {command}")
            threading.Thread(target=self.process_command, args=(command,), daemon=True).start()

    def process_command(self, command):
        plan = parse_command(command)
        self.log(f"[NLU] {plan}")
        try:
            execute_plan(plan)
        except Exception as e:
            self.log(f"[Error] {e}")

    def on_speak(self):
        self.log("[Voice] Listening...")
        threading.Thread(target=self.listen_and_fill, daemon=True).start()

    def listen_and_fill(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            try:
                audio = recognizer.listen(source, timeout=5)
                command = recognizer.recognize_google(audio)
                self.log(f"[Voice] You said: {command}")
                self.input_entry.delete(0, tk.END)
                self.input_entry.insert(0, command)
            except sr.WaitTimeoutError:
                self.log("[Voice] Listening timed out.")
            except sr.UnknownValueError:
                self.log("[Voice] Could not understand audio.")
            except sr.RequestError as e:
                self.log(f"[Voice] Recognition error: {e}")

    def log(self, message):
        self.output_area.config(state='normal')
        self.output_area.insert(tk.END, message + "\n")
        self.output_area.see(tk.END)
        self.output_area.config(state='disabled')

if __name__ == "__main__":
    root = tk.Tk()
    app = WebAgentGUI(root)
    root.mainloop() 