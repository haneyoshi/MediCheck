import UserRequest
from Main_app import MediCheckApp
import tkinter as tk
"""
**project demo is available on my portfolio: https://haneyoshi.github.io/
**UI is under developing
**Program instruction is written in README.md

some sample input for testing
patient id: Z567890123 (Taiwanese id format)
symptoms: cough, fever
diagnose: common cold
"""

def main():
    print("MediCheck System Starts")
    UserRequest.program_start()

    # Start the Tkinter application
    root = tk.Tk()  # Create the main application window
    app = MediCheckApp(root)  # Pass the window to the UI class
    root.mainloop()  # Run the main UI loop

if __name__ == "__main__":
    main()