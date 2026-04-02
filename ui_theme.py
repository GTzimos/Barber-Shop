import tkinter as tk
from tkinter import ttk

BG = "#0B1220"
CARD_BG = "#111A2B"
TEXT = "#E2E8F0"
MUTED = "#94A3B8"
PRIMARY = "#14B8A6"
PRIMARY_ACTIVE = "#0D9488"
SECONDARY = "#1E293B"
SECONDARY_ACTIVE = "#334155"
DANGER = "#EF4444"
DANGER_ACTIVE = "#DC2626"
INPUT_BG = "#0F172A"
INPUT_BORDER = "#334155"
LISTBOX_BG = "#0F172A"
LISTBOX_SELECTED = "#14B8A6"


def apply_theme(window: tk.Tk | tk.Toplevel) -> ttk.Style:
    style = ttk.Style(window)
    style.theme_use("clam")

    window.configure(background=BG)

    style.configure("App.TFrame", background=BG)
    style.configure("Card.TFrame", background=CARD_BG)

    style.configure("Heading.TLabel", background=CARD_BG, foreground=TEXT, font=("Segoe UI Semibold", 20))
    style.configure("Subtle.TLabel", background=CARD_BG, foreground=MUTED, font=("Segoe UI", 10))
    style.configure("Field.TLabel", background=CARD_BG, foreground=TEXT, font=("Segoe UI Semibold", 10))

    style.configure("App.TEntry", fieldbackground=INPUT_BG, foreground=TEXT, bordercolor=INPUT_BORDER, insertcolor=TEXT, padding=8)

    style.configure(
        "Primary.TButton",
        background=PRIMARY,
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        padding=(14, 10),
        font=("Segoe UI Semibold", 10),
    )
    style.map("Primary.TButton", background=[("active", PRIMARY_ACTIVE), ("pressed", PRIMARY_ACTIVE)])

    style.configure(
        "Secondary.TButton",
        background=SECONDARY,
        foreground=TEXT,
        borderwidth=0,
        focusthickness=0,
        padding=(14, 10),
        font=("Segoe UI", 10),
    )
    style.map("Secondary.TButton", background=[("active", SECONDARY_ACTIVE), ("pressed", SECONDARY_ACTIVE)])

    style.configure(
        "Danger.TButton",
        background=DANGER,
        foreground="white",
        borderwidth=0,
        focusthickness=0,
        padding=(14, 10),
        font=("Segoe UI Semibold", 10),
    )
    style.map("Danger.TButton", background=[("active", DANGER_ACTIVE), ("pressed", DANGER_ACTIVE)])

    style.configure(
        "App.TCombobox",
        fieldbackground=INPUT_BG,
        background=INPUT_BG,
        foreground=TEXT,
        arrowcolor=MUTED,
        bordercolor=INPUT_BORDER,
        lightcolor=INPUT_BORDER,
        darkcolor=INPUT_BORDER,
    )
    style.map("App.TCombobox", fieldbackground=[("readonly", INPUT_BG)], foreground=[("readonly", TEXT)])

    style.configure("Vertical.TScrollbar", background=SECONDARY, troughcolor=BG, arrowcolor=MUTED, bordercolor=BG)
    return style


def center_window(window: tk.Tk | tk.Toplevel, width: int, height: int) -> None:
    screen_w = window.winfo_screenwidth()
    screen_h = window.winfo_screenheight()
    x = (screen_w - width) // 2
    y = (screen_h - height) // 3
    window.geometry(f"{width}x{height}+{x}+{y}")


def enable_borderless(window: tk.Tk | tk.Toplevel, title: str) -> ttk.Frame:
    window.overrideredirect(True)

    container = tk.Frame(window, bg=BG, highlightthickness=1, highlightbackground=INPUT_BORDER)
    container.pack(fill="both", expand=True)

    titlebar = tk.Frame(container, bg=CARD_BG, height=36)
    titlebar.pack(fill="x")
    titlebar.pack_propagate(False)

    title_label = tk.Label(
        titlebar,
        text=title,
        bg=CARD_BG,
        fg=TEXT,
        font=("Segoe UI Semibold", 10),
        padx=12,
    )
    title_label.pack(side="left")

    controls = tk.Frame(titlebar, bg=CARD_BG)
    controls.pack(side="right")

    def minimize_window() -> None:
        window.overrideredirect(False)
        window.iconify()

    close_button = tk.Button(
        controls,
        text="x",
        command=window.destroy,
        bg=CARD_BG,
        fg=TEXT,
        activebackground=DANGER,
        activeforeground="white",
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        font=("Segoe UI", 10),
        cursor="hand2",
    )
    close_button.pack(side="right")

    min_button = tk.Button(
        controls,
        text="-",
        command=minimize_window,
        bg=CARD_BG,
        fg=TEXT,
        activebackground=SECONDARY_ACTIVE,
        activeforeground=TEXT,
        relief="flat",
        bd=0,
        padx=12,
        pady=6,
        font=("Segoe UI", 10),
        cursor="hand2",
    )
    min_button.pack(side="right")

    drag_state = {"x": 0, "y": 0}

    def start_drag(event: tk.Event) -> None:
        drag_state["x"] = event.x_root - window.winfo_x()
        drag_state["y"] = event.y_root - window.winfo_y()

    def drag_window(event: tk.Event) -> None:
        x = event.x_root - drag_state["x"]
        y = event.y_root - drag_state["y"]
        window.geometry(f"+{x}+{y}")

    for draggable in (titlebar, title_label):
        draggable.bind("<ButtonPress-1>", start_drag)
        draggable.bind("<B1-Motion>", drag_window)

    def restore_borderless(_event: tk.Event) -> None:
        if window.state() == "normal":
            window.overrideredirect(True)

    window.bind("<Map>", restore_borderless, add="+")

    content = ttk.Frame(container, style="App.TFrame")
    content.pack(fill="both", expand=True)
    return content


def style_listbox(listbox: tk.Listbox) -> None:
    listbox.configure(
        bg=LISTBOX_BG,
        fg=TEXT,
        selectbackground=LISTBOX_SELECTED,
        selectforeground="#001314",
        highlightbackground=INPUT_BORDER,
        highlightcolor=PRIMARY,
        borderwidth=0,
        relief="flat",
        activestyle="none",
    )
