import pyautogui
import pyperclip
import time

def send_lines(lines):
    if not lines:
        print("No insults were extracted!")
        return
        
    print(f"Preparing to send {len(lines)} insults in 3 seconds...")
    time.sleep(3)  # Give user time to focus the target window
    
    for line in lines:
        # Use clipboard to handle Chinese characters
        pyperclip.copy(line)
        
        # Focus on chat input field (if needed)
        pyautogui.click()  # Optional: click to ensure focus
        
        # Paste text
        pyautogui.hotkey('ctrl', 'v')  # Use 'command', 'v' on Mac
        
        # Send message
        pyautogui.press("enter")
        
        # Wait between messages
        time.sleep(1.2)