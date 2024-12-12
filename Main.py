import UserRequest
from Main_app import MediCheckApp
import tkinter as tk
"""
**UI is under developing
**introduction about this program is in README.md

some sample input for testing
patient id: Z567890123
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