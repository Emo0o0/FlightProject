from tkinter import messagebox
import bcrypt
from Flight_Project.entities.User import User


def handle_register(app):
    values = []
    for _, field_name in app.fields:
        values.append(app.register_fields[field_name].get())
    user = User(
        first_name=values[0],
        last_name=values[1],
        email=values[2],
        password=bcrypt.hashpw(values[3].encode(), app.salt),
        phone=values[4],
        date_of_birth=values[5],
        passport_number=values[6],
        nationality=app.countries_repo.get_by_name(values[7]),
        created_at=app.datetime.datetime.now().isoformat(),
    )
    app.users_repo.save(user)

    """Handle registration - you'll implement database insertion"""
    # Placeholder - you'll connect this to your database
    role = app.role_var.get()
    messagebox.showinfo("Success", f"Registration successful as {role}!")
    app.show_login_screen()
