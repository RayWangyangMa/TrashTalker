import tkinter as tk
import threading
import pyperclip
from ai_engine import generate_insults

class InsultGeneratorOverlay:
    def __init__(self, root):
        self.root = root
        self.root.title("Rage Key v2")
        self.root.geometry("400x450+50+50")  # Width x Height + X + Y position
        self.root.attributes("-topmost", True)  # Keep window on top
        self.root.configure(bg="#2E2E2E")
        
        # Status variables
        self.status_var = tk.StringVar(value="Ready - Press F9 to generate")
        
        # Create UI elements
        self.create_widgets()
        
        # For storing generated insults
        self.current_insults = []
        
        # Flag for generation in progress
        self.is_generating = False
        
        # Bind F9 key to generate insults
        self.root.bind("<F9>", lambda event: self.generate_button_clicked())
        
        # Focus the window to capture keypress events
        self.root.focus_set()

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
        
        # Instructions
        instructions = tk.Label(self.root, text="F9: Generate new insults | Click on an insult to copy to clipboard", 
                             bg="#2E2E2E", fg="yellow", font=("Arial", 9))
        instructions.pack(pady=5)

        
        # Preview frame
        preview_frame = tk.Frame(self.root, bg="#363636", bd=1, relief=tk.SUNKEN)
        preview_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        preview_label = tk.Label(preview_frame, text="Click on an insult to copy it", bg="#363636", fg="white")
        preview_label.pack(anchor=tk.W, padx=5, pady=5)
        
        # Create a frame to hold all insult buttons
        self.insult_frame = tk.Frame(preview_frame, bg="#363636")
        self.insult_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Generate initial insults when app starts
        self.generate_insults("English")  # Fixed function name here

    def generate_button_clicked(self):
        if self.is_generating:
            return
        
        self.is_generating = True
        threading.Thread(target=self.generate_insults, args=("English",)).start()

    def generate_insults(self, language="English"):  # Consistent function name
        try:
            self.status_var.set("Generating...")
            
            # Clear current insult buttons
            for widget in self.insult_frame.winfo_children():
                widget.destroy()
            
            # Generate insults
            insults = generate_insults(language)
            
            # Function to update UI in main thread
            def update_ui():
                # Set the insults in the main thread
                self.current_insults = insults.copy()  # Make a copy to ensure thread safety
                print(f"Updated self.current_insults to: {self.current_insults}")
                self.update_insult_buttons()
                self.status_var.set("Ready - Click an insult to copy")
            
            # Schedule the UI update function on the main thread
            self.root.after(100, update_ui)
        except Exception as e:
            print(f"Error in generate_insults: {str(e)}")
            self.root.after(0, lambda: self.status_var.set(f"Error: {str(e)[:20]}..."))
        finally:
            self.is_generating = False

    def update_insult_buttons(self):
        # Debug print
        print(f"update_insult_buttons called, insults: {self.current_insults}")
        
        # Clear any existing insult buttons
        for widget in self.insult_frame.winfo_children():
            widget.destroy()
        
        # Debug print
        print(f"Creating {len(self.current_insults)} buttons")
        
        # Create a new button for each insult
        for i, insult in enumerate(self.current_insults):
            print(f"Creating button for insult: {insult}")
            
            # Important: Create a closure to capture the current insult
            def create_command(insult_text=insult):
                return lambda: self.copy_to_clipboard(insult_text)
            
            button = tk.Button(
                self.insult_frame,
                text=f"{i+1}. {insult}",
                bg="#404040",
                fg="white",
                wraplength=350,
                justify=tk.LEFT,
                anchor="w",
                pady=8,
                padx=10,
                command=create_command()
            )
            button.pack(fill=tk.X, pady=5, padx=5)
            print(f"Created button for insult {i+1}")
    
    def copy_to_clipboard(self, text):
        pyperclip.copy(text)
        self.status_var.set("Copied to clipboard!")
        self.root.after(2000, lambda: self.status_var.set("Ready - Click an insult to copy"))

# Create the main application
def main():
    root = tk.Tk()
    app = InsultGeneratorOverlay(root)
    root.mainloop()

if __name__ == "__main__":
    main()