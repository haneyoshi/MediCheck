import tkinter as tk
import UserRequest

def show_visits_window(app):
    """Display today's patient visits in a new window."""
    visits_window = tk.Toplevel(app.root)
    visits_window.title("Today's Patient Visits")
    visits_window.geometry("600x500")

    # Fetch today's visits
    visit_list = UserRequest.check_today_visits()
    visit_text = "".join(visit_list) if visit_list else "No patients visited today."

    # Display the visits
    tk.Label(visits_window, text="Today's Patient Visits", font=("Arial", 14, "bold")).pack(pady=10)
    visits_text_box = tk.Text(visits_window, height=20, width=60, wrap="word", font=("Arial", 10))
    visits_text_box.insert("1.0", visit_text)
    visits_text_box.config(state="disabled")  # Make text box read-only
    visits_text_box.pack()

    # Close button
    tk.Button(visits_window, text="Close", command=visits_window.destroy).pack(pady=10)
