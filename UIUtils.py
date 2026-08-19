import tkinter as tk
from tkinter import ttk


COLORS = {
    "navy": "#16324F", "navy_hover": "#21486E", "blue": "#2563EB",
    "blue_hover": "#1D4ED8", "canvas": "#F4F7FB", "surface": "#FFFFFF",
    "border": "#DCE4ED", "text": "#17212B", "muted": "#657384",
    "success": "#16794A", "success_bg": "#E9F7F0", "error": "#B42318",
    "error_bg": "#FDECEC", "info": "#245EA8", "info_bg": "#EAF2FD",
}


def configure_styles(root):
    """Configure the small, shared ttk visual language used by the app shell."""
    style = ttk.Style(root)
    if "clam" in style.theme_names():
        style.theme_use("clam")
    root.configure(background=COLORS["canvas"])
    style.configure("App.TFrame", background=COLORS["canvas"])
    style.configure("Surface.TFrame", background=COLORS["surface"])
    style.configure("Sidebar.TFrame", background=COLORS["navy"])
    style.configure("PageTitle.TLabel", background=COLORS["canvas"], foreground=COLORS["text"], font=("Segoe UI", 22, "bold"))
    style.configure("PageSubtitle.TLabel", background=COLORS["canvas"], foreground=COLORS["muted"], font=("Segoe UI", 10))
    style.configure("CardTitle.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=("Segoe UI", 11, "bold"))
    style.configure("Body.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=("Segoe UI", 10))
    style.configure("Muted.TLabel", background=COLORS["surface"], foreground=COLORS["muted"], font=("Segoe UI", 9))
    style.configure("Metric.TLabel", background=COLORS["surface"], foreground=COLORS["navy"], font=("Segoe UI", 24, "bold"))
    style.configure("ProfileName.TLabel", background=COLORS["surface"], foreground=COLORS["navy"], font=("Segoe UI", 18, "bold"))
    style.configure("FieldValue.TLabel", background=COLORS["surface"], foreground=COLORS["text"], font=("Segoe UI", 11, "bold"))
    style.configure("FieldError.TLabel", background=COLORS["surface"], foreground=COLORS["error"], font=("Segoe UI", 9))
    style.configure("Success.TLabel", background=COLORS["surface"], foreground=COLORS["success"], font=("Segoe UI", 9, "bold"))
    style.configure("EmptyTitle.TLabel", background=COLORS["surface"], foreground=COLORS["navy"], font=("Segoe UI", 12, "bold"))
    style.configure("VisitTitle.TLabel", background=COLORS["surface"], foreground=COLORS["navy"], font=("Segoe UI", 11, "bold"))
    style.configure("Primary.TButton", background=COLORS["blue"], foreground="white", borderwidth=0, font=("Segoe UI", 10, "bold"), padding=(16, 10))
    style.map("Primary.TButton", background=[("active", COLORS["blue_hover"]), ("disabled", "#A9B7C8")])
    style.configure("Secondary.TButton", background=COLORS["surface"], foreground=COLORS["navy"], bordercolor=COLORS["border"], font=("Segoe UI", 10, "bold"), padding=(14, 9))
    style.map("Secondary.TButton", background=[("active", "#EDF3F9")])
    style.configure("Danger.TButton", background=COLORS["surface"], foreground=COLORS["error"], bordercolor="#F2C7C3", font=("Segoe UI", 10, "bold"), padding=(14, 9))
    style.map("Danger.TButton", background=[("active", COLORS["error_bg"])])
    style.configure("Suggestion.TButton", background=COLORS["info_bg"], foreground=COLORS["info"], bordercolor="#C9DCF7", font=("Segoe UI", 9, "bold"), padding=(11, 8))
    style.map("Suggestion.TButton", background=[("active", "#DCEAFB")])
    style.configure("Mode.TButton", background=COLORS["surface"], foreground=COLORS["navy"], bordercolor=COLORS["border"], font=("Segoe UI", 10, "bold"), padding=(16, 10))
    style.configure("Active.Mode.TButton", background=COLORS["navy"], foreground="white", borderwidth=0, font=("Segoe UI", 10, "bold"), padding=(16, 10))
    style.map("Active.Mode.TButton", background=[("active", COLORS["navy_hover"])])
    style.configure("Form.TEntry", padding=(8, 7), fieldbackground="white", bordercolor=COLORS["border"])
    style.map("Form.TEntry", bordercolor=[("focus", COLORS["blue"])], lightcolor=[("focus", COLORS["blue"])])
    style.configure("Nav.TButton", background=COLORS["navy"], foreground="#DDE8F3", borderwidth=0, anchor="w", font=("Segoe UI", 10), padding=(18, 12))
    style.map("Nav.TButton", background=[("active", COLORS["navy_hover"])], foreground=[("active", "white")])
    style.configure("Active.Nav.TButton", background=COLORS["blue"], foreground="white", borderwidth=0, anchor="w", font=("Segoe UI", 10, "bold"), padding=(18, 12))
    style.map("Active.Nav.TButton", background=[("active", COLORS["blue_hover"])])
    style.configure("Treeview", rowheight=34, font=("Segoe UI", 10), fieldbackground=COLORS["surface"])
    style.configure("Treeview.Heading", font=("Segoe UI", 9, "bold"), padding=(8, 8))
    return style


def create_card(parent, padding=20):
    return ttk.Frame(parent, style="Surface.TFrame", padding=padding)


def create_empty_state(parent, title, message, action_text=None, action=None):
    """Render a compact, consistent empty state inside an existing surface."""
    state = ttk.Frame(parent, style="Surface.TFrame", padding=(24, 32))
    ttk.Label(state, text=title, style="EmptyTitle.TLabel").pack(anchor="center")
    ttk.Label(state, text=message, style="Muted.TLabel", justify="center", wraplength=520).pack(anchor="center", pady=(7, 0))
    if action_text and action:
        ttk.Button(state, text=action_text, style="Secondary.TButton", command=action).pack(pady=(16, 0))
    return state


def bind_vertical_mousewheel(widget, canvas):
    """Enable conventional wheel scrolling while the pointer is over a canvas."""
    widget.bind("<Enter>", lambda _event: widget.bind_all("<MouseWheel>", lambda event: canvas.yview_scroll(int(-event.delta / 120), "units")))
    widget.bind("<Leave>", lambda _event: widget.unbind_all("<MouseWheel>"))


class StatusBanner(tk.Label):
    """Persistent inline feedback with success, error, and information states."""

    def __init__(self, parent):
        super().__init__(parent, anchor="w", font=("Segoe UI", 9), padx=14, pady=9, borderwidth=0)
        self.show("Ready for the next patient.", "info")

    def show(self, message, level="info"):
        self.configure(text=message, foreground=COLORS.get(level, COLORS["info"]), background=COLORS.get(f"{level}_bg", COLORS["info_bg"]))


# Compatibility helpers for older screens while they are migrated.
def create_label(parent, text, row, column, padx=5, pady=5):
    label = ttk.Label(parent, text=text)
    label.grid(row=row, column=column, padx=padx, pady=pady)
    return label


def create_button(parent, text, command, row, column, padx=5, pady=5):
    button = ttk.Button(parent, text=text, command=command)
    button.grid(row=row, column=column, padx=padx, pady=pady)
    return button
