import tkinter as tk
from tkinter import ttk
from typing import TYPE_CHECKING


def show_login_screen(app):
    from Flight_Project.ui_elems.login import handle_login
    from Flight_Project.ui_elems.register_screen import show_register_screen

    """Display login screen"""
    app.clear_window()

    # Main container
    container = tk.Frame(app.root, bg="#f0f0f0")
    container.place(relx=0.5, rely=0.5, anchor="center")

    # Title
    title = tk.Label(
        container,
        text="Flight Booking System",
        font=("Arial", 28, "bold"),
        bg="#f0f0f0",
        fg="#2c3e50",
    )
    title.grid(row=0, column=0, columnspan=2, pady=(0, 30))

    # Login frame
    login_frame = tk.LabelFrame(
        container,
        text="Login",
        font=("Arial", 14, "bold"),
        bg="white",
        fg="#2c3e50",
        padx=30,
        pady=20,
    )
    login_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=20)

    # Email
    tk.Label(login_frame, text="Email:", font=("Arial", 11), bg="white").grid(
        row=0, column=0, sticky="w", pady=8
    )
    app.login_email = ttk.Entry(login_frame, width=30, font=("Arial", 10))
    app.login_email.grid(row=0, column=1, pady=8, padx=(10, 0))

    # Password
    tk.Label(login_frame, text="Password:", font=("Arial", 11), bg="white").grid(
        row=1, column=0, sticky="w", pady=8
    )
    app.login_password = ttk.Entry(login_frame, width=30, show="*", font=("Arial", 10))
    app.login_password.grid(row=1, column=1, pady=8, padx=(10, 0))

    # Buttons frame
    btn_frame = tk.Frame(container, bg="#f0f0f0")
    btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

    login_btn = tk.Button(
        btn_frame,
        text="Login",
        command=lambda: handle_login(app),
        bg="#3498db",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=30,
        pady=8,
        cursor="hand2",
        relief="flat",
    )
    login_btn.grid(row=0, column=0, padx=10)

    register_btn = tk.Button(
        btn_frame,
        text="Register",
        command=lambda: show_register_screen(app),
        bg="#2ecc71",
        fg="white",
        font=("Arial", 11, "bold"),
        padx=30,
        pady=8,
        cursor="hand2",
        relief="flat",
    )
    register_btn.grid(row=0, column=1, padx=10)
