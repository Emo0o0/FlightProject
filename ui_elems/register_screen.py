import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING


def show_register_screen(app):
    from Flight_Project.ui_elems.login_screen import show_login_screen
    from Flight_Project.ui_elems.register import handle_register

    """Display registration screen"""
    app.clear_window()

    # Main container with scrollbar
    canvas = tk.Canvas(app.root, bg="#f0f0f0")
    scrollbar = ttk.Scrollbar(app.root, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="#f0f0f0")

    scrollable_frame.bind(
        "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )

    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)

    # Title
    title = tk.Label(
        scrollable_frame,
        text="Register New Account",
        font=("Arial", 24, "bold"),
        bg="#f0f0f0",
        fg="#2c3e50",
    )
    title.grid(row=0, column=0, columnspan=2, pady=20, padx=50)

    # Registration frame
    reg_frame = tk.LabelFrame(
        scrollable_frame,
        text="Personal Information",
        font=("Arial", 12, "bold"),
        bg="white",
        fg="#2c3e50",
        padx=30,
        pady=20,
    )
    reg_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=50, pady=10)

    # Fields
    app.fields = [
        ("First Name:", "first_name"),
        ("Last Name:", "last_name"),
        ("Email:", "email"),
        ("Password:", "password"),
        ("Phone:", "phone"),
        ("Date of Birth (YYYY-MM-DD):", "dob"),
        ("Passport Number:", "passport"),
        ("Nationality (Country):", "nationality"),
    ]

    app.register_fields = {}
    for idx, (label, field_name) in enumerate(app.fields):
        tk.Label(reg_frame, text=label, font=("Arial", 10), bg="white").grid(
            row=idx, column=0, sticky="w", pady=5
        )

        if field_name == "password":
            entry = ttk.Entry(reg_frame, width=35, show="*", font=("Arial", 10))
        else:
            entry = ttk.Entry(reg_frame, width=35, font=("Arial", 10))

        entry.grid(row=idx, column=1, pady=5, padx=(10, 0))
        app.register_fields[field_name] = entry

    # Role selection
    tk.Label(reg_frame, text="Role:", font=("Arial", 10), bg="white").grid(
        row=len(app.fields), column=0, sticky="w", pady=5
    )
    app.role_var = tk.StringVar(value="passenger")
    role_frame = tk.Frame(reg_frame, bg="white")
    role_frame.grid(row=len(app.fields), column=1, sticky="w", pady=5, padx=(10, 0))

    ttk.Radiobutton(
        role_frame, text="Passenger", variable=app.role_var, value="passenger"
    ).pack(side="left", padx=5)
    ttk.Radiobutton(
        role_frame, text="Admin/Staff", variable=app.role_var, value="admin"
    ).pack(side="left", padx=5)

    # Buttons
    btn_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

    register_btn = tk.Button(
        btn_frame,
        text="Register",
        command=lambda: handle_register(app),
        bg="#2ecc71",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=30,
        pady=8,
        cursor="hand2",
        relief="flat",
    )
    register_btn.grid(row=0, column=0, padx=10)

    back_btn = tk.Button(
        btn_frame,
        text="Back to Login",
        command=lambda: show_login_screen(app),
        bg="#95a5a6",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=30,
        pady=8,
        cursor="hand2",
        relief="flat",
    )
    back_btn.grid(row=0, column=1, padx=10)

    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
