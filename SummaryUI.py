import tkinter as tk
import UserRequest

def show_summary_ui(app):
    """Display the final summary of the diagnosis."""
    summary_window = tk.Toplevel(app.root)
    summary_window.title("Diagnosis Summary")
    summary_window.geometry("700x600")

    # Fetch the diagnosis summary from the backend
    summary = UserRequest.case_complete()

    # Display the summary text
    tk.Label(summary_window, text="Diagnosis Summary", font=("Arial", 14, "bold")).pack(pady=10)
    summary_text_box = tk.Text(summary_window, height=20, width=60, wrap="word", font=("Arial", 10))
    summary_text_box.insert("1.0", summary)
    summary_text_box.config(state="disabled")  # Make text box read-only
    summary_text_box.pack(pady=10)

    # Close button to finish the process
    def close_summary():
        summary_window.destroy()

    tk.Button(summary_window, text="Close", command=close_summary).pack(pady=10)
