import tkinter as tk
import threading
import pyautogui
import pyperclip
import time
from ai_engine import generate_insults
from config import SUPPORTED_LANGUAGES

class InsultGeneratorOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Insult Generator")
        self.root.geometry("300x400+50+50")  # Width x Height + X + Y position
        self.root.attributes("-topmost", True)  # Keep window on top
        self.root.configure(bg="#2E2E2E")
        
        # Status variables
        self.status_var = tk.StringVar(value="Ready")
        self.language_var = tk.StringVar(value="Choose language")
        
        # Create UI elements
        self.create_widgets()
        
        # For storing generated insults
        self.current_insults = []
        
        # Flag for generation in progress
        self.is_generating = False

    def create_widgets(self):
        # Title
        title_label = tk.Label(self.root, text="Rage Key v2", font=("Arial", 16, "bold"), 
                              bg="#2E2E2E", fg="white")
        title_label.pack(pady=10)
        
        # Status
        status_frame = tk.Frame(self.root, bg="#2E2E2E")
        status_frame.pack(fill=tk.X, pady=5)
        
        status_label = tk.Label(status_frame, text="Status:", bg="#2E2E2E", fg="white")
        status_label.pack(side=tk.LEFT, padx=10)
        
        status_value = tk.Label(status_frame, textvariable=self.status_var, 
                              bg="#2E2E2E", fg="#00FF00")
        status_value.pack(side=tk.LEFT)
        
        # Language selection
        language_frame = tk.Frame(self.root, bg="#2E2E2E")
        language_frame.pack(fill=tk.X, pady=5)
        
        language_label = tk.Label(language_frame, text="Language:", bg="#2E2E2E", fg="white")
        language_label.pack(side=tk.LEFT, padx=10)
        
        language_value = tk.Label(language_frame, textvariable=self.language_var, 
                                bg="#2E2E2E", fg="yellow")
        language_value.pack(side=tk.LEFT)
        
        # Language buttons
        lang_buttons_frame = tk.Frame(self.root, bg="#2E2E2E")
        lang_buttons_frame.pack(pady=10)
        
        for i, lang in enumerate(SUPPORTED_LANGUAGES):
            btn = tk.Button(lang_buttons_frame, text=lang, width=10,
                          command=lambda l=lang: self.set_language(l))
            btn.grid(row=i//2, column=i%2, padx=5, pady=5)
        
        # Generate button
        generate_btn = tk.Button(self.root, text="Generate Insults", width=15, height=2,
                               command=self.generate_button_clicked, bg="#4CAF50", fg="white")
        generate_btn.pack(pady=10)
        
        # Send button
        send_btn = tk.Button(self.root, text="Send Insults", width=15, height=2,
                          command=self.send_button_clicked, bg="#2196F3", fg="white")
        send_btn.pack(pady=5)
        
        # Preview frame
        preview_frame = tk.Frame(self.root, bg="#363636", bd=1, relief=tk.SUNKEN)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        preview_label = tk.Label(preview_frame, text="Preview", bg="#363636", fg="white")
        preview_label.pack(anchor=tk.W, padx=5, pady=5)
        
        self.preview_text = tk.Text(preview_frame, height=5, width=30, bg="#404040", fg="white")
        self.preview_text.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def set_language(self, language):
        self.language_var.set(language)
        self.status_var.set(f"Language set: {language}")

    def generate_button_clicked(self):
        if self.is_generating:
            return
            
        language = self.language_var.get()
        if language == "Choose language":
            self.status_var.set("Please select a language first")
            return
            
        # Start generation in a separate thread to keep UI responsive
        self.is_generating = True
        self.status_var.set("Generating...")
        self.preview_text.delete(1.0, tk.END)
        
        threading.Thread(target=self.generate_insults_thread, args=(language,)).start()

    def generate_insults_thread(self, language):
        try:
            self.current_insults = generate_insults(language)
            self.root.after(0, self.update_preview)
            self.root.after(0, lambda: self.status_var.set("Ready to send"))
        except Exception as e:
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)[:20]}..."))
        finally:
            self.is_generating = False

    def update_preview(self):
        self.preview_text.delete(1.0, tk.END)
        for i, insult in enumerate(self.current_insults, 1):
            self.preview_text.insert(tk.END, f"{i}. {insult}\n\n")

    def send_button_clicked(self):
        if not self.current_insults:
            self.status_var.set("No insults to send!")
            return
            
        self.status_var.set("Preparing to send...")
        threading.Thread(target=self.send_insults_thread).start()

    def send_insults_thread(self):
        self.root.after(0, lambda: self.status_var.set("Sending in 3s..."))
        time.sleep(3)  # Give time to focus target window
        
        for i, line in enumerate(self.current_insults, 1):
            self.root.after(0, lambda i=i: self.status_var.set(f"Sending {i}/{len(self.current_insults)}"))
            
            # Use clipboard to handle Unicode characters
            pyperclip.copy(line)
            pyautogui.click()  # Optional: ensure focus
            pyautogui.hotkey('ctrl', 'v')  # 'command', 'v' on Mac
            pyautogui.press("enter")
            time.sleep(1.2)
            
        self.root.after(0, lambda: self.status_var.set("Done!"))

# Create the main application
def main():
    root = tk.Tk()
    app = InsultGeneratorOverlay(root)
    root.mainloop()

if __name__ == "__main__":
    main()