import tkinter as tk
import UserRequest

def show_queue_window(app):
    """Display the current patient queue in a new window."""
    queue_window = tk.Toplevel(app.root)
    queue_window.title("Current Patient Queue")
    queue_window.geometry("600x500")

    # Fetch the current queue
    queue_list = UserRequest.check_current_queue()
    queue_text = "".join(queue_list) if queue_list else "No patients in the queue."

    # Display the queue
    tk.Label(queue_window, text="Current Patient Queue", font=("Arial", 14, "bold")).pack(pady=10)
    queue_text_box = tk.Text(queue_window, height=20, width=60, wrap="word", font=("Arial", 10))
    queue_text_box.insert("1.0", queue_text)
    queue_text_box.config(state="disabled")  # Make text box read-only
    queue_text_box.pack()

    # Close button
    tk.Button(queue_window, text="Close", command=queue_window.destroy).pack(pady=10)
