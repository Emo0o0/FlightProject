import tkinter as tk
from tkinter import ttk
from tkinter import messagebox

import bcrypt


def handle_login(app):
    """Handle login button click - you'll implement authentication logic"""
    # Placeholder - you'll connect this to your database
    email = app.login_email.get()
    password = app.login_password.get()

    # For demo purposes, simulating login
    if email and password:
        # You'll check credentials here
        # For now, assume passenger if contains 'passenger', else admin
        if "admin" in email.lower():
            app.user_role = "admin"
        else:
            app.user_role = "passenger"

        app.current_user = app.users_repo.find_by_email(email)
        if bcrypt.checkpw(password.encode(), app.current_user.password):
            app.show_main_screen()
        else:
            messagebox.showerror("Error", "Wrong credentials")
    else:
        messagebox.showerror("Error", "Please enter email and password")
