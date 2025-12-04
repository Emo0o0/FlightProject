import random
import string
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import datetime
import bcrypt

from Flight_Project.entities.Booking import Booking
from Flight_Project.entities.Review import Review
from Flight_Project.entities.Ticket import Ticket
from Flight_Project.entities.User import User
from Flight_Project.repositories.AircraftTypesRepository import (
    AircraftTypesRepository,
)
from Flight_Project.repositories.AircraftsRepository import AircraftsRepository
from Flight_Project.repositories.AirlinesRepository import AirlinesRepository
from Flight_Project.repositories.AirportsRepository import AirportsRepository
from Flight_Project.repositories.AmenitiesRepository import AmenitiesRepository
from Flight_Project.repositories.BookingsRepository import BookingsRepository
from Flight_Project.repositories.CitiesRepository import CitiesRepository
from Flight_Project.repositories.CountriesRepository import CountriesRepository
from Flight_Project.repositories.FlightStatusesRepository import (
    FlightStatusesRepository,
)
from Flight_Project.repositories.FlightsRepository import FlightsRepository
from Flight_Project.repositories.IATACodesRepository import IATACodesRepository
from Flight_Project.repositories.ManufacturersRepository import (
    ManufacturersRepository,
)
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.ReviewsRepository import ReviewsRepository
from Flight_Project.repositories.TicketsRepository import TicketsRepository
from Flight_Project.repositories.UsersRepository import UsersRepository

db_manager = RepositoryManager()
countries_repo = CountriesRepository(db_manager)
cities_repo = CitiesRepository(db_manager, countries_repo)
iata_codes_repo = IATACodesRepository(db_manager)
airlines_repo = AirlinesRepository(
    db_manager, countries_repo, cities_repo, iata_codes_repo
)
manufacturer_repo = ManufacturersRepository(db_manager)
aircraft_types_repo = AircraftTypesRepository(db_manager, manufacturer_repo)
aircrafts_repo = AircraftsRepository(db_manager, aircraft_types_repo)
airports_repo = AirportsRepository(
    db_manager, iata_codes_repo, cities_repo, countries_repo
)
flights_status_repo = FlightStatusesRepository(db_manager)
amenities_repo = AmenitiesRepository(db_manager)
users_repo = UsersRepository(db_manager, countries_repo)
bookings_repo = BookingsRepository(db_manager, users_repo)
flights_repo = FlightsRepository(
    db_manager,
    airlines_repo,
    aircrafts_repo,
    airports_repo,
    flights_status_repo,
    amenities_repo,
    bookings_repo,
)
flights_repo.set_bookings_repo(bookings_repo)
bookings_repo.set_flights_repo(flights_repo)

tickets_repo = TicketsRepository(db_manager, bookings_repo, flights_repo, users_repo)
reviews_repo = ReviewsRepository(db_manager, users_repo, flights_repo)


class FlightBookingSystem:
    def __init__(self, root):
        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("1400x700")
        self.root.configure(bg="#f0f0f0")

        # Configure style
        self.style = ttk.Style()
        self.style.theme_use("clam")

        # Current user role (will be set after login)
        self.user_role = None  # 'passenger' or 'admin'
        self.current_user = None

        self.salt = bcrypt.gensalt()

        # Show login screen initially
        self.show_login_screen()

    def clear_window(self):
        """Clear all widgets from the window"""
        for widget in self.root.winfo_children():
            widget.destroy()

    # ==================== LOGIN/REGISTER SCREENS ====================

    def show_login_screen(self):
        """Display login screen"""
        self.clear_window()

        # Main container
        container = tk.Frame(self.root, bg="#f0f0f0")
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
        self.login_email = ttk.Entry(login_frame, width=30, font=("Arial", 10))
        self.login_email.grid(row=0, column=1, pady=8, padx=(10, 0))

        # Password
        tk.Label(login_frame, text="Password:", font=("Arial", 11), bg="white").grid(
            row=1, column=0, sticky="w", pady=8
        )
        self.login_password = ttk.Entry(
            login_frame, width=30, show="*", font=("Arial", 10)
        )
        self.login_password.grid(row=1, column=1, pady=8, padx=(10, 0))

        # Buttons frame
        btn_frame = tk.Frame(container, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        login_btn = tk.Button(
            btn_frame,
            text="Login",
            command=self.handle_login,
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
            command=self.show_register_screen,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=30,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        register_btn.grid(row=0, column=1, padx=10)

    def show_register_screen(self):
        """Display registration screen"""
        self.clear_window()

        # Main container with scrollbar
        canvas = tk.Canvas(self.root, bg="#f0f0f0")
        scrollbar = ttk.Scrollbar(self.root, orient="vertical", command=canvas.yview)
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
        self.fields = [
            ("First Name:", "first_name"),
            ("Last Name:", "last_name"),
            ("Email:", "email"),
            ("Password:", "password"),
            ("Phone:", "phone"),
            ("Date of Birth (YYYY-MM-DD):", "dob"),
            ("Passport Number:", "passport"),
            ("Nationality (Country):", "nationality"),
        ]

        self.register_fields = {}
        for idx, (label, field_name) in enumerate(self.fields):
            tk.Label(reg_frame, text=label, font=("Arial", 10), bg="white").grid(
                row=idx, column=0, sticky="w", pady=5
            )

            if field_name == "password":
                entry = ttk.Entry(reg_frame, width=35, show="*", font=("Arial", 10))
            else:
                entry = ttk.Entry(reg_frame, width=35, font=("Arial", 10))

            entry.grid(row=idx, column=1, pady=5, padx=(10, 0))
            self.register_fields[field_name] = entry

        # Role selection
        tk.Label(reg_frame, text="Role:", font=("Arial", 10), bg="white").grid(
            row=len(self.fields), column=0, sticky="w", pady=5
        )
        self.role_var = tk.StringVar(value="passenger")
        role_frame = tk.Frame(reg_frame, bg="white")
        role_frame.grid(
            row=len(self.fields), column=1, sticky="w", pady=5, padx=(10, 0)
        )

        ttk.Radiobutton(
            role_frame, text="Passenger", variable=self.role_var, value="passenger"
        ).pack(side="left", padx=5)
        ttk.Radiobutton(
            role_frame, text="Admin/Staff", variable=self.role_var, value="admin"
        ).pack(side="left", padx=5)

        # Buttons
        btn_frame = tk.Frame(scrollable_frame, bg="#f0f0f0")
        btn_frame.grid(row=2, column=0, columnspan=2, pady=20)

        register_btn = tk.Button(
            btn_frame,
            text="Register",
            command=self.handle_register,
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
            command=self.show_login_screen,
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

    def handle_login(self):
        """Handle login button click - you'll implement authentication logic"""
        # Placeholder - you'll connect this to your database
        email = self.login_email.get()
        password = self.login_password.get()

        # For demo purposes, simulating login
        if email and password:
            # You'll check credentials here
            # For now, assume passenger if contains 'passenger', else admin
            if "admin" in email.lower():
                self.user_role = "admin"
            else:
                self.user_role = "passenger"

            self.current_user = users_repo.find_by_email(email)
            if bcrypt.checkpw(password.encode(), self.current_user.password):
                self.show_main_screen()
            else:
                messagebox.showerror("Error", "Wrong credentials")
        else:
            messagebox.showerror("Error", "Please enter email and password")

    def handle_register(self):
        values = []
        for _, field_name in self.fields:
            values.append(self.register_fields[field_name].get())
        user = User(
            first_name=values[0],
            last_name=values[1],
            email=values[2],
            password=bcrypt.hashpw(values[3].encode(), self.salt),
            phone=values[4],
            date_of_birth=values[5],
            passport_number=values[6],
            nationality=countries_repo.get_by_name(values[7]),
            created_at=datetime.datetime.now().isoformat(),
        )
        users_repo.save(user)

        """Handle registration - you'll implement database insertion"""
        # Placeholder - you'll connect this to your database
        role = self.role_var.get()
        messagebox.showinfo("Success", f"Registration successful as {role}!")
        self.show_login_screen()

    def create_tickets_for_booking(self, booking: "Booking", user):
        for i in range(int(booking.number_of_passengers)):
            for flight in booking.flights:
                ticket = Ticket(
                    ticket_number=f"{flight.airline.iata_code.code}{random.randint(10**9,(10**10)-1)}",
                    booking=booking,
                    flight=flight,
                    user=user,
                    seat_number="A1",
                    ticket_class="economy",
                    ticket_status="active",
                    issued_at=datetime.datetime.now().isoformat(),
                    checked_in_at=None,
                    boarded_at=None,
                    cancelled_at=None,
                    no_show_at=None,
                )
                tickets_repo.save(ticket)

    def handle_book_selected_flights(self):
        ref = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        booking = Booking(
            ref,
            self.current_user,
            self.passengers_spin.get(),
            0,
            datetime.datetime.now().isoformat(),
        )
        for flight_id in self.tree.selection():
            flight_number = self.tree.item(flight_id, "values")[0]
            flight = flights_repo.get_flight_by_flight_number(flight_number)
            flight.available_seats = int(flight.available_seats) - int(
                self.passengers_spin.get()
            )
            flights_repo.update(flight)
            booking.total_amount += float(booking.number_of_passengers) * float(
                flight.seat_price
            )
            booking.add_flight(flight)

        bookings_repo.save(booking)

        self.create_tickets_for_booking(booking, self.current_user)

        messagebox.showinfo("Congratulations", "Booking was successful")

    def handle_cancel_booking(self):
        booking_id = self.my_bookings_tree.selection()
        booking_reference = self.my_bookings_tree.item(booking_id, "values")[0]
        booking = bookings_repo.fetch_booking_by_reference(booking_reference)
        for flight in bookings_repo.fetch_flights_for_booking(booking.id):
            flight.available_seats += int(booking.number_of_passengers)
            flights_repo.update(flight)

        bookings_repo.delete(booking.id)

        self.my_bookings_tree.delete(booking_id)
        messagebox.showinfo("", "Booking was successfully cancelled")

    # ==================== MAIN SCREENS ====================

    def show_main_screen(self):
        """Show appropriate main screen based on user role"""
        if self.user_role == "passenger":
            self.show_passenger_dashboard()
        else:
            self.show_admin_dashboard()

    # ==================== PASSENGER DASHBOARD ====================

    def show_passenger_dashboard(self):
        """Main dashboard for passengers"""
        self.clear_window()

        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Flight Booking System - Passenger Portal",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        logout_btn = tk.Button(
            header,
            text="Logout",
            command=self.show_login_screen,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            cursor="hand2",
            relief="flat",
        )
        logout_btn.pack(side="right", padx=20, pady=15)

        user_label = tk.Label(
            header,
            text=f"Welcome, {self.current_user.first_name} {self.current_user.last_name}",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="white",
        )
        user_label.pack(side="right", padx=20)

        # Navigation sidebar
        sidebar = tk.Frame(self.root, bg="#34495e", width=200)
        sidebar.pack(side="left", fill="y")

        nav_buttons = [
            ("Search Flights", self.show_search_flights),
            ("My Bookings", self.show_my_bookings),
            ("My Tickets", self.show_my_tickets),
            ("My Reviews", self.show_my_reviews),
            ("Write Review", self.show_write_review),
        ]

        for btn_text, command in nav_buttons:
            btn = tk.Button(
                sidebar,
                text=btn_text,
                command=command,
                bg="#34495e",
                fg="white",
                font=("Arial", 11),
                padx=20,
                pady=15,
                cursor="hand2",
                relief="flat",
                anchor="w",
                width=18,
            )
            btn.pack(fill="x", pady=2)
            btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#2c3e50"))
            btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#34495e"))

        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Show search flights by default
        self.show_search_flights()

    def show_searched_flights(self):
        for child in self.tree.get_children():
            self.tree.delete(child)

        origin = self.search_origin_combo.get().split(",")[0]
        destination = self.search_dest_combo.get().split(",")[0]
        passenger_count = int(self.passengers_spin.get())
        date = self.date_entry.get()
        for flight in flights_repo.fetch_flights_from_to(
            origin, destination, passenger_count, date
        ):
            self.tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    flight.flight_number,
                    flight.airline.name,
                    flight.expected_departure_time,
                    flight.expected_arrival_time,
                    "2 Hours",
                    flight.seat_price,
                    flight.available_seats,
                ),
            )

    def show_search_flights(self):
        """Search flights screen for passengers"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Search Flights",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Search form
        search_frame = tk.LabelFrame(
            self.content_frame,
            text="Flight Search",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=30,
            pady=20,
        )
        search_frame.pack(padx=30, pady=10, fill="x")

        # Origin
        tk.Label(search_frame, text="From:", font=("Arial", 10), bg="white").grid(
            row=0, column=0, sticky="w", pady=8
        )

        destination_values = list()
        for city in cities_repo.fetch_all():
            destination_values.append(f"{city.name}, {city.country.name}")
        self.search_origin_combo = ttk.Combobox(
            search_frame, width=25, font=("Arial", 10), values=destination_values
        )
        self.search_origin_combo.grid(row=0, column=1, pady=8, padx=10)

        # Destination
        tk.Label(search_frame, text="To:", font=("Arial", 10), bg="white").grid(
            row=0, column=2, sticky="w", pady=8, padx=(20, 0)
        )
        self.search_dest_combo = ttk.Combobox(
            search_frame, width=25, font=("Arial", 10), values=destination_values
        )
        self.search_dest_combo.grid(row=0, column=3, pady=8, padx=10)

        # Date
        tk.Label(
            search_frame, text="Departure Date:", font=("Arial", 10), bg="white"
        ).grid(row=1, column=0, sticky="w", pady=8)
        self.date_entry = ttk.Entry(search_frame, width=27, font=("Arial", 10))
        self.date_entry.grid(row=1, column=1, pady=8, padx=10)
        self.date_entry.insert(0, datetime.datetime.now().strftime("%Y-%m-%d"))

        # Passengers
        tk.Label(search_frame, text="Passengers:", font=("Arial", 10), bg="white").grid(
            row=1, column=2, sticky="w", pady=8, padx=(20, 0)
        )
        self.passengers_spin = ttk.Spinbox(
            search_frame, from_=1, to=15, width=25, font=("Arial", 10)
        )
        self.passengers_spin.grid(row=1, column=3, pady=8, padx=10)
        self.passengers_spin.set(1)

        # Search button
        search_btn = tk.Button(
            search_frame,
            text="Search Flights",
            bg="#3498db",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat",
            command=self.show_searched_flights,
        )
        search_btn.grid(row=2, column=0, columnspan=4, pady=(15, 5))

        # Results frame
        results_frame = tk.LabelFrame(
            self.content_frame,
            text="Available Flights",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        results_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Treeview for flight results
        columns = (
            "Flight",
            "From",
            "To",
            "Airline",
            "Departure",
            "Arrival",
            "Duration",
            "Price",
            "Seats",
        )
        self.tree = ttk.Treeview(
            results_frame, columns=columns, show="headings", height=12
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, anchor="center")

        # POPULATING THE VIEW
        for flight in flights_repo.fetch_all():
            expected_departure = flight.expected_departure_time
            expected_arrival = flight.expected_arrival_time
            t1 = datetime.datetime.fromisoformat(
                expected_departure.replace("Z", "+00:00")
            )
            t2 = datetime.datetime.fromisoformat(
                expected_arrival.replace("Z", "+00:00")
            )
            departure_time = (
                flight.expected_departure_time[:10]
                + "  "
                + flight.expected_departure_time[11:16]
            )
            arrival_time = (
                flight.expected_arrival_time[:10]
                + "  "
                + flight.expected_arrival_time[11:16]
            )
            self.tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    flight.flight_number,
                    flight.origin_airport.city.name
                    + ", "
                    + flight.origin_airport.country.country_code,
                    flight.destination_airport.city.name
                    + ", "
                    + flight.destination_airport.country.country_code,
                    flight.airline.name,
                    departure_time,
                    arrival_time,
                    f"{int((t2 - t1).total_seconds() / 3600)} hours",
                    flight.seat_price,
                    flight.available_seats,
                ),
            )

        # Scrollbar
        scrollbar = ttk.Scrollbar(
            results_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Book button
        book_btn = tk.Button(
            results_frame,
            text="Book Selected Flight",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat",
            command=self.handle_book_selected_flights,
        )
        book_btn.pack(pady=10)

    def show_booking_details(self, booking_data=None):

        booking_id = self.my_bookings_tree.selection()
        booking_reference = self.my_bookings_tree.item(booking_id, "values")[0]
        booking = bookings_repo.fetch_booking_by_reference(booking_reference)

        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Booking Details",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Create scrollable frame
        canvas = tk.Canvas(self.content_frame, bg="#ecf0f1")
        scrollbar = ttk.Scrollbar(
            self.content_frame, orient="vertical", command=canvas.yview
        )
        scrollable_frame = tk.Frame(canvas, bg="#ecf0f1")

        scrollable_frame.bind(
            "<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Booking Information
        info_frame = tk.LabelFrame(
            scrollable_frame,
            text="Booking Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=30,
            pady=20,
        )
        info_frame.pack(padx=30, pady=10, fill="x")

        # Mock data - you'll replace with actual booking_data

        if booking_data is None:
            booking_data = {
                "reference": booking.booking_reference,
                "created_at": booking.created_at,
                "number_of_passengers": booking.number_of_passengers,
                "total_amount": booking.total_amount,
                "user_email": booking.user.email,
                "user_name": f"{booking.user.first_name} {booking.user.last_name}",
            }

        details = [
            ("Booking Reference:", booking_data.get("reference", "N/A")),
            ("Booking Date:", booking_data.get("created_at", "N/A")),
            ("Passenger Name:", booking_data.get("user_name", "N/A")),
            ("Email:", booking_data.get("user_email", "N/A")),
            ("Number of Passengers:", str(booking_data.get("number_of_passengers", 0))),
            ("Total Amount:", f"${booking_data.get('total_amount', 0):.2f}"),
        ]

        for idx, (label, value) in enumerate(details):
            tk.Label(
                info_frame, text=label, font=("Arial", 10, "bold"), bg="white"
            ).grid(row=idx, column=0, sticky="w", pady=5, padx=(0, 20))
            tk.Label(info_frame, text=value, font=("Arial", 10), bg="white").grid(
                row=idx, column=1, sticky="w", pady=5
            )

        # Flights in this booking
        flights_frame = tk.LabelFrame(
            scrollable_frame,
            text="Flights in Booking",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=15,
        )
        flights_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Mock flight data - you'll replace with actual flights from booking
        flights = bookings_repo.fetch_flights_for_booking(booking.id)
        # flights = [
        #     {
        #         "flight_number": "AA101",
        #         "airline": "American Airlines",
        #         "origin": "JFK - New York",
        #         "destination": "LAX - Los Angeles",
        #         "departure": "2024-12-10 08:00:00",
        #         "arrival": "2024-12-10 11:30:00",
        #         "status": "Scheduled",
        #         "aircraft": "Boeing 737-800",
        #         "dep_gate": "A12",
        #         "dep_terminal": "Terminal 1",
        #         "arr_gate": "B5",
        #         "arr_terminal": "Terminal 3",
        #     },
        # ]

        for flight_idx, flight in enumerate(flights):
            # Individual flight card
            flight_card = tk.LabelFrame(
                flights_frame,
                text=f"Flight {flight_idx + 1}: {flight.flight_number}",
                font=("Arial", 11, "bold"),
                bg="#f8f9fa",
                padx=20,
                pady=15,
            )
            flight_card.pack(fill="x", pady=10)

            # Flight route header
            route_frame = tk.Frame(flight_card, bg="#f8f9fa")
            route_frame.pack(fill="x", pady=(0, 10))

            tk.Label(
                route_frame,
                text=f"{flight.origin_airport.iata_code.code} - {flight.origin_airport.city.name}",
                font=("Arial", 12, "bold"),
                bg="#f8f9fa",
                fg="#2c3e50",
            ).pack(side="left")
            tk.Label(
                route_frame,
                text="  →  ",
                font=("Arial", 12),
                bg="#f8f9fa",
                fg="#3498db",
            ).pack(side="left")
            tk.Label(
                route_frame,
                text=f"{flight.destination_airport.iata_code.code} - {flight.destination_airport.city.name}",
                font=("Arial", 12, "bold"),
                bg="#f8f9fa",
                fg="#2c3e50",
            ).pack(side="left")

            # Flight details in grid
            details_grid = tk.Frame(flight_card, bg="#f8f9fa")
            details_grid.pack(fill="x")

            flight_details = [
                ("Airline:", flight.airline.name),
                (
                    "Aircraft:",
                    f"{flight.aircraft.aircraft_type.model}",
                ),
                ("Departure:", flight.expected_departure_time),
                ("Arrival:", flight.expected_arrival_time),
                ("Status:", flight.flight_status.status),
                (
                    "Departure Gate:",
                    f"{flight.departure_gate} ({flight.departure_terminal})",
                ),
                ("Arrival Gate:", f"{flight.arrival_gate} ({flight.arrival_terminal})"),
            ]

            for idx, (label, value) in enumerate(flight_details):
                row = idx // 2
                col = (idx % 2) * 2

                tk.Label(
                    details_grid, text=label, font=("Arial", 9, "bold"), bg="#f8f9fa"
                ).grid(row=row, column=col, sticky="w", pady=3, padx=(0, 10))
                tk.Label(
                    details_grid, text=value, font=("Arial", 9), bg="#f8f9fa"
                ).grid(row=row, column=col + 1, sticky="w", pady=3, padx=(0, 30))

        # Passengers Information
        passengers_frame = tk.LabelFrame(
            scrollable_frame,
            text="Passengers",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=20,
            pady=15,
        )
        passengers_frame.pack(padx=30, pady=10, fill="x")

        # Mock passenger data
        passengers = [
            {
                "name": "John Doe",
                "passport": "P12345678",
                "nationality": "USA",
                "dob": "1985-05-15",
            },
            {
                "name": "Jane Doe",
                "passport": "P87654321",
                "nationality": "USA",
                "dob": "1987-08-22",
            },
        ]

        columns = ("Name", "Passport", "Nationality", "Date of Birth")
        tree = ttk.Treeview(
            passengers_frame, columns=columns, show="headings", height=len(passengers)
        )

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        for passenger in passengers:
            tree.insert(
                "",
                "end",
                values=(
                    passenger["name"],
                    passenger["passport"],
                    passenger["nationality"],
                    passenger["dob"],
                ),
            )

        tree.pack(fill="x", pady=10)

        # Payment Information
        payment_frame = tk.LabelFrame(
            scrollable_frame,
            text="Payment Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=30,
            pady=20,
        )
        payment_frame.pack(padx=30, pady=10, fill="x")

        payment_details = [
            ("Payment Method:", "Credit Card (****1234)"),
            ("Payment Status:", "Completed"),
            ("Payment Date:", "2024-12-01 10:35:00"),
            ("Transaction ID:", "TXN789456123"),
        ]

        for idx, (label, value) in enumerate(payment_details):
            tk.Label(
                payment_frame, text=label, font=("Arial", 10, "bold"), bg="white"
            ).grid(row=idx, column=0, sticky="w", pady=5, padx=(0, 20))
            tk.Label(payment_frame, text=value, font=("Arial", 10), bg="white").grid(
                row=idx, column=1, sticky="w", pady=5
            )

        # Action buttons
        btn_frame = tk.Frame(scrollable_frame, bg="#ecf0f1")
        btn_frame.pack(pady=20)

        back_btn = tk.Button(
            btn_frame,
            text="Back to Bookings",
            command=self.show_my_bookings,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        back_btn.pack(side="left", padx=5)

        print_btn = tk.Button(
            btn_frame,
            text="Print Booking",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        print_btn.pack(side="left", padx=5)

        canvas.pack(side="left", fill="both", expand=True, padx=30)
        scrollbar.pack(side="right", fill="y")

    def show_my_bookings(self):
        """Show user's bookings"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="My Bookings",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Bookings list
        bookings_frame = tk.LabelFrame(
            self.content_frame,
            text="Booking History",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        bookings_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "Reference",
            "Date",
            "Flights",
            "Passengers",
            "Total Amount",
        )
        self.my_bookings_tree = ttk.Treeview(
            bookings_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.my_bookings_tree.heading(col, text=col)
            self.my_bookings_tree.column(col, width=140, anchor="center")

        scrollbar = ttk.Scrollbar(
            bookings_frame, orient="vertical", command=self.my_bookings_tree.yview
        )
        self.my_bookings_tree.configure(yscrollcommand=scrollbar.set)

        self.my_bookings_tree.pack(
            side="left", fill="both", expand=True, padx=10, pady=10
        )
        scrollbar.pack(side="right", fill="y", pady=10)

        for booking in bookings_repo.fetch_user_bookings(self.current_user.id):
            flights = ""
            for flight in bookings_repo.fetch_flights_for_booking(booking.id):
                flights += f"{flight.flight_number} "
            self.my_bookings_tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    booking.booking_reference,
                    booking.created_at,
                    flights,
                    booking.number_of_passengers,
                    booking.total_amount,
                ),
            )

        # Action buttons
        btn_frame = tk.Frame(bookings_frame, bg="white")
        btn_frame.pack(pady=10)

        view_btn = tk.Button(
            btn_frame,
            text="View Details",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
            command=self.show_booking_details,
        )
        view_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel Booking",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
            command=self.handle_cancel_booking,
        )
        cancel_btn.pack(side="left", padx=5)

    def show_my_tickets(self):
        """Show user's tickets"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="My Tickets",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        tickets_frame = tk.LabelFrame(
            self.content_frame,
            text="Issued Tickets",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        tickets_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "Ticket #",
            "Flight",
            "Date",
            "Seat",
            "Class",
            "Status",
            "Gate",
            "Terminal",
        )
        self.my_tickets_tree = ttk.Treeview(
            tickets_frame, columns=columns, show="headings", height=15
        )

        for col in columns:
            self.my_tickets_tree.heading(col, text=col)
            self.my_tickets_tree.column(col, width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            tickets_frame, orient="vertical", command=self.my_tickets_tree.yview
        )
        self.my_tickets_tree.configure(yscrollcommand=scrollbar.set)

        self.my_tickets_tree.pack(
            side="left", fill="both", expand=True, padx=10, pady=10
        )
        scrollbar.pack(side="right", fill="y", pady=10)

        tickets = tickets_repo.fetch_user_tickets(self.current_user.id)
        for ticket in tickets:
            date = ticket.flight.expected_departure_time
            ui_date = date[:10] + " " + date[11:16]
            self.my_tickets_tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    ticket.ticket_number,
                    ticket.flight.flight_number,
                    ui_date,
                    ticket.seat_number,
                    ticket.ticket_class,
                    ticket.ticket_status,
                    ticket.flight.departure_gate,
                    ticket.flight.departure_terminal,
                ),
            )

        btn_frame = tk.Frame(tickets_frame, bg="white")
        btn_frame.pack(pady=10)

        print_btn = tk.Button(
            btn_frame,
            text="Print Ticket",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        print_btn.pack(side="left", padx=5)

        checkin_btn = tk.Button(
            btn_frame,
            text="Check In",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        checkin_btn.pack(side="left", padx=5)

    def handle_delete_review(self):
        pass

    def show_my_reviews(self):
        """Show user's reviews"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="My Reviews",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        reviews_frame = tk.LabelFrame(
            self.content_frame,
            text="Flight Reviews",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        reviews_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("Flight", "Airline", "Rating", "Date", "Comment")
        self.my_reviews_tree = ttk.Treeview(
            reviews_frame, columns=columns, show="headings", height=15
        )

        self.my_reviews_tree.heading("Flight", text="Flight")
        self.my_reviews_tree.heading("Airline", text="Airline")
        self.my_reviews_tree.heading("Rating", text="Rating")
        self.my_reviews_tree.heading("Date", text="Date")
        self.my_reviews_tree.heading("Comment", text="Comment")

        self.my_reviews_tree.column("Flight", width=100)
        self.my_reviews_tree.column("Airline", width=120)
        self.my_reviews_tree.column("Rating", width=80)
        self.my_reviews_tree.column("Date", width=100)
        self.my_reviews_tree.column("Comment", width=300)

        scrollbar = ttk.Scrollbar(
            reviews_frame, orient="vertical", command=self.my_reviews_tree.yview
        )
        self.my_reviews_tree.configure(yscrollcommand=scrollbar.set)

        self.my_reviews_tree.pack(
            side="left", fill="both", expand=True, padx=10, pady=10
        )
        scrollbar.pack(side="right", fill="y", pady=10)

        reviews = reviews_repo.fetch_user_reviews(self.current_user.id)
        for review in reviews:
            date = review.created_at
            ui_date = date[:10] + " " + date[11:16]
            self.my_reviews_tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    review.flight.flight_number,
                    review.flight.airline.name,
                    review.rating,
                    ui_date,
                    review.description,
                ),
            )

        btn_frame = tk.Frame(reviews_frame, bg="white")
        btn_frame.pack(pady=10)

        edit_btn = tk.Button(
            btn_frame,
            text="Edit Review",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Review",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
            command=self.handle_delete_review,
        )
        delete_btn.pack(side="left", padx=5)

    def handle_submit_review_button(self):

        flight = flights_repo.get_flight_by_flight_number(self.flight_combo.get())

        review = Review(
            user=self.current_user,
            flight=flight,
            rating=self.rating_var.get(),
            description=self.review_text.get("1.0", tk.END),
            created_at=datetime.datetime.now().isoformat(),
        )
        reviews_repo.save(review)

        messagebox.showinfo("", "We appreciate your feedback")
        self.review_text.delete("1.0", tk.END)

    def show_write_review(self):
        """Write a new review"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Write Flight Review",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        review_frame = tk.LabelFrame(
            self.content_frame,
            text="Review Details",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=30,
            pady=20,
        )
        review_frame.pack(padx=30, pady=10, fill="both", expand=True)

        flights = flights_repo.fetch_user_flights(self.current_user.id)
        values = [flight.flight_number for flight in flights]
        # Select flight
        tk.Label(
            review_frame, text="Select Flight:", font=("Arial", 11), bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10)
        self.flight_combo = ttk.Combobox(
            review_frame, width=40, font=("Arial", 10), values=values
        )
        self.flight_combo.grid(row=0, column=1, pady=10, sticky="w")

        # Rating
        tk.Label(review_frame, text="Rating:", font=("Arial", 11), bg="white").grid(
            row=1, column=0, sticky="w", pady=10
        )
        rating_frame = tk.Frame(review_frame, bg="white")
        rating_frame.grid(row=1, column=1, sticky="w", pady=10)

        self.rating_var = tk.IntVar(value=5)
        for i in range(1, 6):
            ttk.Radiobutton(
                rating_frame,
                text=f"{i} Star{'s' if i > 1 else ''}",
                variable=self.rating_var,
                value=i,
            ).pack(side="left", padx=5)

        # Comment
        tk.Label(
            review_frame, text="Your Review:", font=("Arial", 11), bg="white"
        ).grid(row=2, column=0, sticky="nw", pady=10)
        self.review_text = tk.Text(
            review_frame, width=50, height=10, font=("Arial", 10), wrap="word"
        )
        self.review_text.grid(row=2, column=1, pady=10, sticky="w")

        # Submit button
        submit_btn = tk.Button(
            review_frame,
            text="Submit Review",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=20,
            pady=8,
            cursor="hand2",
            relief="flat",
            command=self.handle_submit_review_button,
        )
        submit_btn.grid(row=3, column=0, columnspan=2, pady=20)

    # ==================== ADMIN DASHBOARD ====================

    def show_admin_dashboard(self):
        """Main dashboard for admin/staff"""
        self.clear_window()

        # Header
        header = tk.Frame(self.root, bg="#2c3e50", height=60)
        header.pack(fill="x")

        tk.Label(
            header,
            text="Flight Booking System - Admin Portal",
            font=("Arial", 18, "bold"),
            bg="#2c3e50",
            fg="white",
        ).pack(side="left", padx=20, pady=15)

        logout_btn = tk.Button(
            header,
            text="Logout",
            command=self.show_login_screen,
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=5,
            cursor="hand2",
            relief="flat",
        )
        logout_btn.pack(side="right", padx=20, pady=15)

        user_label = tk.Label(
            header,
            text=f"Admin: {self.current_user.first_name} {self.current_user.last_name}",
            font=("Arial", 11),
            bg="#2c3e50",
            fg="white",
        )
        user_label.pack(side="right", padx=20)

        # Navigation sidebar
        sidebar = tk.Frame(self.root, bg="#34495e", width=200)
        sidebar.pack(side="left", fill="y")

        # Management sections
        sections = [
            ("Dashboard", self.show_admin_home),
            ("--- Flights ---", None),
            ("Manage Flights", self.show_manage_flights),
            ("Flight Status", self.show_flight_status),
            ("--- Bookings ---", None),
            ("Manage Bookings", self.show_manage_bookings),
            ("Manage Tickets", self.show_manage_tickets),
            ("Payments", self.show_payments),
            ("--- Resources ---", None),
            ("Aircraft", self.show_aircraft),
            ("Airlines", self.show_airlines),
            ("Airports", self.show_airports),
            ("--- Users ---", None),
            ("Manage Users", self.show_manage_users),
            ("Reviews", self.show_all_reviews),
        ]

        for btn_text, command in sections:
            if command is None:
                # Section header
                label = tk.Label(
                    sidebar,
                    text=btn_text,
                    bg="#34495e",
                    fg="#95a5a6",
                    font=("Arial", 9, "bold"),
                    anchor="w",
                    padx=20,
                    pady=5,
                )
                label.pack(fill="x")
            else:
                btn = tk.Button(
                    sidebar,
                    text=btn_text,
                    command=command,
                    bg="#34495e",
                    fg="white",
                    font=("Arial", 10),
                    padx=20,
                    pady=12,
                    cursor="hand2",
                    relief="flat",
                    anchor="w",
                    width=18,
                )
                btn.pack(fill="x", pady=1)
                btn.bind("<Enter>", lambda e, b=btn: b.configure(bg="#2c3e50"))
                btn.bind("<Leave>", lambda e, b=btn: b.configure(bg="#34495e"))

        # Main content area
        self.content_frame = tk.Frame(self.root, bg="#ecf0f1")
        self.content_frame.pack(side="left", fill="both", expand=True)

        # Show dashboard by default
        self.show_admin_home()

    def show_admin_home(self):
        """Admin dashboard home"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Admin Dashboard",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Statistics cards
        stats_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        stats_frame.pack(pady=20, padx=30, fill="x")

        stats = [
            ("Total Flights", "1,234", "#3498db"),
            ("Active Bookings", "567", "#2ecc71"),
            ("Total Users", "8,901", "#9b59b6"),
            ("Revenue", "$123,456", "#f39c12"),
        ]

        for idx, (title, value, color) in enumerate(stats):
            card = tk.Frame(stats_frame, bg=color, relief="raised", bd=2)
            card.grid(row=0, column=idx, padx=10, pady=10, sticky="ew")
            stats_frame.grid_columnconfigure(idx, weight=1)

            tk.Label(card, text=title, font=("Arial", 12), bg=color, fg="white").pack(
                pady=(10, 0)
            )
            tk.Label(
                card, text=value, font=("Arial", 24, "bold"), bg=color, fg="white"
            ).pack(pady=(0, 10))

        # Recent activity
        activity_frame = tk.LabelFrame(
            self.content_frame,
            text="Recent Activity",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        activity_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("Time", "Type", "Description", "User")
        tree = ttk.Treeview(activity_frame, columns=columns, show="headings", height=10)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(activity_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

    def show_add_flight_form(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Add New Flight",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Form frame
        form_frame = tk.LabelFrame(
            self.content_frame,
            text="Flight Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=40,
            pady=20,
        )
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Flight Number
        tk.Label(
            form_frame, text="Flight Number:", font=("Arial", 10), bg="white"
        ).grid(row=0, column=0, sticky="w", pady=8)
        flight_number_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        flight_number_entry.grid(row=0, column=1, pady=8, padx=10, sticky="w")

        # Airline
        tk.Label(form_frame, text="Airline:", font=("Arial", 10), bg="white").grid(
            row=0, column=2, sticky="w", pady=8, padx=(20, 0)
        )
        airline_combo = ttk.Combobox(form_frame, width=28, font=("Arial", 10))
        airline_combo.grid(row=0, column=3, pady=8, padx=10, sticky="w")

        # Aircraft
        tk.Label(form_frame, text="Aircraft:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="w", pady=8
        )
        aircraft_combo = ttk.Combobox(form_frame, width=28, font=("Arial", 10))
        aircraft_combo.grid(row=1, column=1, pady=8, padx=10, sticky="w")

        # Origin Airport
        tk.Label(
            form_frame, text="Origin Airport:", font=("Arial", 10), bg="white"
        ).grid(row=1, column=2, sticky="w", pady=8, padx=(20, 0))
        origin_combo = ttk.Combobox(form_frame, width=28, font=("Arial", 10))
        origin_combo.grid(row=1, column=3, pady=8, padx=10, sticky="w")

        # Destination Airport
        tk.Label(
            form_frame, text="Destination Airport:", font=("Arial", 10), bg="white"
        ).grid(row=2, column=0, sticky="w", pady=8)
        dest_combo = ttk.Combobox(form_frame, width=28, font=("Arial", 10))
        dest_combo.grid(row=2, column=1, pady=8, padx=10, sticky="w")

        # Expected Departure Time
        tk.Label(
            form_frame, text="Departure Time:", font=("Arial", 10), bg="white"
        ).grid(row=2, column=2, sticky="w", pady=8, padx=(20, 0))
        departure_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        departure_entry.grid(row=2, column=3, pady=8, padx=10, sticky="w")
        departure_entry.insert(0, "YYYY-MM-DD HH:MM:SS")

        # Expected Arrival Time
        tk.Label(form_frame, text="Arrival Time:", font=("Arial", 10), bg="white").grid(
            row=3, column=0, sticky="w", pady=8
        )
        arrival_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        arrival_entry.grid(row=3, column=1, pady=8, padx=10, sticky="w")
        arrival_entry.insert(0, "YYYY-MM-DD HH:MM:SS")

        # Total Seats
        tk.Label(form_frame, text="Total Seats:", font=("Arial", 10), bg="white").grid(
            row=3, column=2, sticky="w", pady=8, padx=(20, 0)
        )
        seats_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        seats_entry.grid(row=3, column=3, pady=8, padx=10, sticky="w")

        # Seat Price
        tk.Label(
            form_frame, text="Seat Price ($):", font=("Arial", 10), bg="white"
        ).grid(row=4, column=0, sticky="w", pady=8)
        price_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        price_entry.grid(row=4, column=1, pady=8, padx=10, sticky="w")

        # Flight Status
        tk.Label(
            form_frame, text="Flight Status:", font=("Arial", 10), bg="white"
        ).grid(row=4, column=2, sticky="w", pady=8, padx=(20, 0))
        status_combo = ttk.Combobox(
            form_frame,
            values=[
                "Scheduled",
                "Delayed",
                "Boarding",
                "Departed",
                "Arrived",
                "Cancelled",
            ],
            width=28,
            font=("Arial", 10),
        )
        status_combo.grid(row=4, column=3, pady=8, padx=10, sticky="w")
        status_combo.set("Scheduled")

        # Departure Gate
        tk.Label(
            form_frame, text="Departure Gate:", font=("Arial", 10), bg="white"
        ).grid(row=5, column=0, sticky="w", pady=8)
        dep_gate_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        dep_gate_entry.grid(row=5, column=1, pady=8, padx=10, sticky="w")

        # Departure Terminal
        tk.Label(
            form_frame, text="Departure Terminal:", font=("Arial", 10), bg="white"
        ).grid(row=5, column=2, sticky="w", pady=8, padx=(20, 0))
        dep_terminal_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        dep_terminal_entry.grid(row=5, column=3, pady=8, padx=10, sticky="w")

        # Arrival Gate
        tk.Label(form_frame, text="Arrival Gate:", font=("Arial", 10), bg="white").grid(
            row=6, column=0, sticky="w", pady=8
        )
        arr_gate_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        arr_gate_entry.grid(row=6, column=1, pady=8, padx=10, sticky="w")

        # Arrival Terminal
        tk.Label(
            form_frame, text="Arrival Terminal:", font=("Arial", 10), bg="white"
        ).grid(row=6, column=2, sticky="w", pady=8, padx=(20, 0))
        arr_terminal_entry = ttk.Entry(form_frame, width=30, font=("Arial", 10))
        arr_terminal_entry.grid(row=6, column=3, pady=8, padx=10, sticky="w")

        # Amenities
        tk.Label(form_frame, text="Amenities:", font=("Arial", 10), bg="white").grid(
            row=7, column=0, sticky="nw", pady=8
        )
        amenities_frame = tk.Frame(form_frame, bg="white")
        amenities_frame.grid(row=7, column=1, columnspan=3, sticky="w", pady=8, padx=10)

        # Checkboxes for amenities
        amenity_vars = {}
        amenities_list = [
            "WiFi",
            "In-Flight Entertainment",
            "Meals",
            "Power Outlets",
            "Extra Legroom",
        ]
        for i, amenity in enumerate(amenities_list):
            var = tk.BooleanVar()
            cb = ttk.Checkbutton(amenities_frame, text=amenity, variable=var)
            cb.grid(row=i // 3, column=i % 3, sticky="w", padx=10, pady=2)
            amenity_vars[amenity] = var

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=8, column=0, columnspan=4, pady=(20, 0))

        def save_flight():
            # You'll implement the database save logic here
            flight_data = {
                "flight_number": flight_number_entry.get(),
                "airline": airline_combo.get(),
                "aircraft": aircraft_combo.get(),
                "origin": origin_combo.get(),
                "destination": dest_combo.get(),
                "departure_time": departure_entry.get(),
                "arrival_time": arrival_entry.get(),
                "total_seats": seats_entry.get(),
                "price": price_entry.get(),
                "status": status_combo.get(),
                "dep_gate": dep_gate_entry.get(),
                "dep_terminal": dep_terminal_entry.get(),
                "arr_gate": arr_gate_entry.get(),
                "arr_terminal": arr_terminal_entry.get(),
                "amenities": [k for k, v in amenity_vars.items() if v.get()],
            }

            # TODO: Add your database insertion logic here
            # For now, just show success message
            messagebox.showinfo(
                "Success", f"Flight {flight_data['flight_number']} added successfully!"
            )
            self.show_manage_flights()

        save_btn = tk.Button(
            btn_frame,
            text="Save Flight",
            command=save_flight,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.show_manage_flights,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        cancel_btn.pack(side="left", padx=5)

    def show_manage_flights(self):
        """Manage flights screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Manage Flights",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Action buttons
        btn_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        btn_frame.pack(pady=10)

        add_btn = tk.Button(
            btn_frame,
            text="+ Add New Flight",
            command=self.show_add_flight_form,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        add_btn.pack(side="left", padx=5)

        # Flights list
        flights_frame = tk.LabelFrame(
            self.content_frame,
            text="All Flights",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        flights_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Flight#",
            "Airline",
            "Aircraft",
            "From",
            "To",
            "Departure",
            "Arrival",
            "Status",
            "Seats",
            "Price",
        )
        tree = ttk.Treeview(flights_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=90, anchor="center")

        flights = flights_repo.fetch_all()
        for flight in flights:
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    flight.id,
                    flight.flight_number,
                    flight.airline.name,
                    flight.aircraft.aircraft_type.model,
                    flight.origin_airport.city.name
                    + ", "
                    + flight.origin_airport.country.country_code,
                    flight.destination_airport.city.name
                    + ", "
                    + flight.destination_airport.country.country_code,
                    flight.expected_departure_time,
                    flight.expected_arrival_time,
                    flight.flight_status.status,
                    flight.available_seats,
                    flight.seat_price,
                ),
            )

        scrollbar = ttk.Scrollbar(flights_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # CRUD buttons
        crud_frame = tk.Frame(flights_frame, bg="white")
        crud_frame.pack(pady=10)

        edit_btn = tk.Button(
            crud_frame,
            text="Edit",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            crud_frame,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        delete_btn.pack(side="left", padx=5)

        view_btn = tk.Button(
            crud_frame,
            text="View Details",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        view_btn.pack(side="left", padx=5)

    def show_flight_status(self):
        """Flight status management"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Flight Status Management",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        status_frame = tk.LabelFrame(
            self.content_frame,
            text="Update Flight Status",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        status_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "Flight#",
            "Route",
            "Current Status",
            "Departure",
            "Gate",
            "Terminal",
        )
        tree = ttk.Treeview(status_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=120, anchor="center")

        scrollbar = ttk.Scrollbar(status_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        # Status update controls
        control_frame = tk.Frame(status_frame, bg="white")
        control_frame.pack(pady=10)

        tk.Label(
            control_frame, text="New Status:", font=("Arial", 10), bg="white"
        ).pack(side="left", padx=5)
        status_combo = ttk.Combobox(
            control_frame,
            values=[
                "Scheduled",
                "Delayed",
                "Boarding",
                "Departed",
                "Arrived",
                "Cancelled",
            ],
            width=15,
        )
        status_combo.pack(side="left", padx=5)

        update_btn = tk.Button(
            control_frame,
            text="Update Status",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        update_btn.pack(side="left", padx=5)

    def show_manage_bookings(self):
        """Manage bookings screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Manage Bookings",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        bookings_frame = tk.LabelFrame(
            self.content_frame,
            text="All Bookings",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        bookings_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Reference",
            "User",
            "Date",
            "Flights",
            "Passengers",
            "Amount",
        )
        tree = ttk.Treeview(bookings_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        bookings = bookings_repo.fetch_all()
        for booking in bookings:
            ui_flights = ""
            for flight in booking.flights:
                ui_flights += flight.flight_number + " "
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    booking.id,
                    booking.booking_reference,
                    booking.user.id,
                    booking.created_at,
                    ui_flights,
                    booking.number_of_passengers,
                    booking.total_amount,
                ),
            )

        scrollbar = ttk.Scrollbar(bookings_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        btn_frame = tk.Frame(bookings_frame, bg="white")
        btn_frame.pack(pady=10)

        view_btn = tk.Button(
            btn_frame,
            text="View Details",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        view_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel Booking",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        cancel_btn.pack(side="left", padx=5)

    def show_manage_tickets(self):
        """Manage tickets screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Manage Tickets",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        tickets_frame = tk.LabelFrame(
            self.content_frame,
            text="All Tickets",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        tickets_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Ticket#",
            "Booking Ref",
            "Flight",
            "User",
            "Seat",
            "Class",
            "Status",
            "Issued",
        )
        tree = ttk.Treeview(tickets_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        tickets = tickets_repo.fetch_all()
        for ticket in tickets:
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    ticket.id,
                    ticket.ticket_number,
                    ticket.booking.booking_reference,
                    ticket.flight.flight_number,
                    ticket.user.email,
                    ticket.seat_number,
                    ticket.ticket_class,
                    ticket.ticket_status,
                    ticket.issued_at,
                ),
            )

        scrollbar = ttk.Scrollbar(tickets_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        btn_frame = tk.Frame(tickets_frame, bg="white")
        btn_frame.pack(pady=10)

        issue_btn = tk.Button(
            btn_frame,
            text="Issue Ticket",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        issue_btn.pack(side="left", padx=5)

        void_btn = tk.Button(
            btn_frame,
            text="Void Ticket",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        void_btn.pack(side="left", padx=5)

    def show_payments(self):
        """Payments screen"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Payment Transactions",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        payments_frame = tk.LabelFrame(
            self.content_frame,
            text="All Payments",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        payments_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("ID", "Booking Ref", "Amount", "Method", "Date", "Status")
        tree = ttk.Treeview(payments_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=130, anchor="center")

        scrollbar = ttk.Scrollbar(payments_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        btn_frame = tk.Frame(payments_frame, bg="white")
        btn_frame.pack(pady=10)

        view_btn = tk.Button(
            btn_frame,
            text="View Details",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        view_btn.pack(side="left", padx=5)

        refund_btn = tk.Button(
            btn_frame,
            text="Process Refund",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        refund_btn.pack(side="left", padx=5)

    # NEW===============================================================================================================
    def show_add_aircraft_form(self):
        """Show form to add a new aircraft"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Add New Aircraft",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Form frame
        form_frame = tk.LabelFrame(
            self.content_frame,
            text="Aircraft Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=40,
            pady=20,
        )
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Registration Number
        tk.Label(
            form_frame, text="Registration Number:", font=("Arial", 10), bg="white"
        ).grid(row=0, column=0, sticky="w", pady=10)
        registration_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        registration_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # Aircraft Type
        tk.Label(
            form_frame, text="Aircraft Type:", font=("Arial", 10), bg="white"
        ).grid(row=1, column=0, sticky="w", pady=10)
        type_combo = ttk.Combobox(form_frame, width=33, font=("Arial", 10))
        type_combo["values"] = (
            "Boeing 737-800",
            "Boeing 777-300ER",
            "Airbus A320",
            "Airbus A380",
            "Embraer E190",
        )
        type_combo.grid(row=1, column=1, pady=10, padx=10, sticky="w")

        # Manufacturer
        tk.Label(form_frame, text="Manufacturer:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="w", pady=10
        )
        manufacturer_combo = ttk.Combobox(form_frame, width=33, font=("Arial", 10))
        manufacturer_combo["values"] = (
            "Boeing",
            "Airbus",
            "Embraer",
            "Bombardier",
            "ATR",
        )
        manufacturer_combo.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Total Seats
        tk.Label(form_frame, text="Total Seats:", font=("Arial", 10), bg="white").grid(
            row=3, column=0, sticky="w", pady=10
        )
        seats_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        seats_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Manufacture Year
        tk.Label(
            form_frame, text="Manufacture Year:", font=("Arial", 10), bg="white"
        ).grid(row=4, column=0, sticky="w", pady=10)
        year_spin = ttk.Spinbox(
            form_frame, from_=1990, to=2025, width=33, font=("Arial", 10)
        )
        year_spin.set(2024)
        year_spin.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        # Engine Count
        tk.Label(form_frame, text="Engine Count:", font=("Arial", 10), bg="white").grid(
            row=5, column=0, sticky="w", pady=10
        )
        engine_count_spin = ttk.Spinbox(
            form_frame, from_=2, to=4, width=33, font=("Arial", 10)
        )
        engine_count_spin.set(2)
        engine_count_spin.grid(row=5, column=1, pady=10, padx=10, sticky="w")

        # Engine Type
        tk.Label(form_frame, text="Engine Type:", font=("Arial", 10), bg="white").grid(
            row=6, column=0, sticky="w", pady=10
        )
        engine_type_combo = ttk.Combobox(form_frame, width=33, font=("Arial", 10))
        engine_type_combo["values"] = ("Turbofan", "Turboprop", "Turbojet")
        engine_type_combo.grid(row=6, column=1, pady=10, padx=10, sticky="w")

        # Range (km)
        tk.Label(form_frame, text="Range (km):", font=("Arial", 10), bg="white").grid(
            row=7, column=0, sticky="w", pady=10
        )
        range_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        range_entry.grid(row=7, column=1, pady=10, padx=10, sticky="w")

        # Cruise Speed (km/h)
        tk.Label(
            form_frame, text="Cruise Speed (km/h):", font=("Arial", 10), bg="white"
        ).grid(row=8, column=0, sticky="w", pady=10)
        speed_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        speed_entry.grid(row=8, column=1, pady=10, padx=10, sticky="w")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=9, column=0, columnspan=2, pady=(20, 0))

        def save_aircraft():
            aircraft_data = {
                "registration_number": registration_entry.get(),
                "aircraft_type": type_combo.get(),
                "manufacturer": manufacturer_combo.get(),
                "total_seats": seats_entry.get(),
                "manufacture_year": year_spin.get(),
                "engine_count": engine_count_spin.get(),
                "engine_type": engine_type_combo.get(),
                "range_km": range_entry.get(),
                "cruise_speed_kmh": speed_entry.get(),
            }

            # TODO: Add your database insertion logic here
            messagebox.showinfo(
                "Success",
                f"Aircraft {aircraft_data['registration_number']} added successfully!",
            )
            self.show_aircraft()

        save_btn = tk.Button(
            btn_frame,
            text="Save Aircraft",
            command=save_aircraft,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.show_aircraft,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        cancel_btn.pack(side="left", padx=5)

    def show_add_airline_form(self):
        """Show form to add a new airline"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Add New Airline",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Form frame
        form_frame = tk.LabelFrame(
            self.content_frame,
            text="Airline Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=40,
            pady=20,
        )
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Airline Name
        tk.Label(form_frame, text="Airline Name:", font=("Arial", 10), bg="white").grid(
            row=0, column=0, sticky="w", pady=10
        )
        name_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        name_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # IATA Code
        tk.Label(form_frame, text="IATA Code:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="w", pady=10
        )
        iata_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        iata_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        # tk.Label(
        #     form_frame,
        #     text="(2-letter code, e.g., AA, UA)",
        #     font=("Arial", 8),
        #     bg="white",
        #     fg="#7f8c8d",
        # ).grid(row=1, column=2, sticky="w", padx=5)

        # Email
        tk.Label(form_frame, text="Email:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="w", pady=10
        )
        email_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        email_entry.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # Phone
        tk.Label(form_frame, text="Phone:", font=("Arial", 10), bg="white").grid(
            row=3, column=0, sticky="w", pady=10
        )
        phone_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        phone_entry.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Country
        tk.Label(form_frame, text="Country:", font=("Arial", 10), bg="white").grid(
            row=4, column=0, sticky="w", pady=10
        )
        country_combo = ttk.Combobox(form_frame, width=33, font=("Arial", 10))
        country_combo["values"] = (
            "USA",
            "United Kingdom",
            "Germany",
            "France",
            "Canada",
            "Australia",
            "Japan",
            "China",
        )
        country_combo.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        # Headquarters City
        tk.Label(
            form_frame, text="Headquarters City:", font=("Arial", 10), bg="white"
        ).grid(row=5, column=0, sticky="w", pady=10)
        headquarters_combo = ttk.Combobox(form_frame, width=33, font=("Arial", 10))
        headquarters_combo["values"] = (
            "New York",
            "London",
            "Paris",
            "Berlin",
            "Tokyo",
            "Sydney",
            "Toronto",
        )
        headquarters_combo.grid(row=5, column=1, pady=10, padx=10, sticky="w")

        # Fleet Size
        tk.Label(form_frame, text="Fleet Size:", font=("Arial", 10), bg="white").grid(
            row=6, column=0, sticky="w", pady=10
        )
        fleet_entry = ttk.Entry(form_frame, width=35, font=("Arial", 10))
        fleet_entry.grid(row=6, column=1, pady=10, padx=10, sticky="w")

        # Founded Year
        tk.Label(form_frame, text="Founded Year:", font=("Arial", 10), bg="white").grid(
            row=7, column=0, sticky="w", pady=10
        )
        founded_spin = ttk.Spinbox(
            form_frame, from_=1900, to=2025, width=33, font=("Arial", 10)
        )
        founded_spin.set(2000)
        founded_spin.grid(row=7, column=1, pady=10, padx=10, sticky="w")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=8, column=0, columnspan=3, pady=(20, 0))

        def save_airline():
            airline_data = {
                "name": name_entry.get(),
                "iata_code": iata_entry.get(),
                "email": email_entry.get(),
                "phone": phone_entry.get(),
                "country": country_combo.get(),
                "headquarters": headquarters_combo.get(),
                "fleet_size": fleet_entry.get(),
                "founded_year": founded_spin.get(),
            }

            # TODO: Add your database insertion logic here
            messagebox.showinfo(
                "Success", f"Airline {airline_data['name']} added successfully!"
            )
            self.show_airlines()

        save_btn = tk.Button(
            btn_frame,
            text="Save Airline",
            command=save_airline,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.show_airlines,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        cancel_btn.pack(side="left", padx=5)

    def show_add_airport_form(self):
        """Show form to add a new airport"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Add New Airport",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        # Form frame
        form_frame = tk.LabelFrame(
            self.content_frame,
            text="Airport Information",
            font=("Arial", 12, "bold"),
            bg="white",
            padx=40,
            pady=20,
        )
        form_frame.pack(padx=30, pady=10, fill="both", expand=True)

        # Airport Name
        tk.Label(form_frame, text="Airport Name:", font=("Arial", 10), bg="white").grid(
            row=0, column=0, sticky="w", pady=10
        )
        name_entry = ttk.Entry(form_frame, width=40, font=("Arial", 10))
        name_entry.grid(row=0, column=1, pady=10, padx=10, sticky="w")

        # IATA Code
        tk.Label(form_frame, text="IATA Code:", font=("Arial", 10), bg="white").grid(
            row=1, column=0, sticky="w", pady=10
        )
        iata_entry = ttk.Entry(form_frame, width=40, font=("Arial", 10))
        iata_entry.grid(row=1, column=1, pady=10, padx=10, sticky="w")
        # tk.Label(
        #     form_frame,
        #     text="(3-letter code, e.g., JFK, LAX)",
        #     font=("Arial", 8),
        #     bg="white",
        #     fg="#7f8c8d",
        # ).grid(row=1, column=2, sticky="w", padx=5)

        # Country
        tk.Label(form_frame, text="Country:", font=("Arial", 10), bg="white").grid(
            row=2, column=0, sticky="w", pady=10
        )
        country_combo = ttk.Combobox(form_frame, width=38, font=("Arial", 10))
        country_combo["values"] = (
            "USA",
            "United Kingdom",
            "Germany",
            "France",
            "Canada",
            "Australia",
            "Japan",
            "China",
            "Spain",
            "Italy",
        )
        country_combo.grid(row=2, column=1, pady=10, padx=10, sticky="w")

        # City
        tk.Label(form_frame, text="City:", font=("Arial", 10), bg="white").grid(
            row=3, column=0, sticky="w", pady=10
        )
        city_combo = ttk.Combobox(form_frame, width=38, font=("Arial", 10))
        city_combo["values"] = (
            "New York",
            "Los Angeles",
            "London",
            "Paris",
            "Berlin",
            "Tokyo",
            "Sydney",
            "Toronto",
            "Madrid",
            "Rome",
        )
        city_combo.grid(row=3, column=1, pady=10, padx=10, sticky="w")

        # Timezone
        tk.Label(form_frame, text="Timezone:", font=("Arial", 10), bg="white").grid(
            row=4, column=0, sticky="w", pady=10
        )
        timezone_combo = ttk.Combobox(form_frame, width=38, font=("Arial", 10))
        timezone_combo["values"] = (
            "UTC-5 (EST)",
            "UTC-8 (PST)",
            "UTC+0 (GMT)",
            "UTC+1 (CET)",
            "UTC+9 (JST)",
            "UTC+10 (AEST)",
        )
        timezone_combo.grid(row=4, column=1, pady=10, padx=10, sticky="w")

        # Elevation
        tk.Label(
            form_frame, text="Elevation (meters):", font=("Arial", 10), bg="white"
        ).grid(row=5, column=0, sticky="w", pady=10)
        elevation_entry = ttk.Entry(form_frame, width=40, font=("Arial", 10))
        elevation_entry.grid(row=5, column=1, pady=10, padx=10, sticky="w")

        # Buttons
        btn_frame = tk.Frame(form_frame, bg="white")
        btn_frame.grid(row=6, column=0, columnspan=3, pady=(20, 0))

        def save_airport():
            airport_data = {
                "name": name_entry.get(),
                "iata_code": iata_entry.get(),
                "country": country_combo.get(),
                "city": city_combo.get(),
                "timezone": timezone_combo.get(),
                "elevation": elevation_entry.get(),
            }

            # TODO: Add your database insertion logic here
            messagebox.showinfo(
                "Success",
                f"Airport {airport_data['name']} ({airport_data['iata_code']}) added successfully!",
            )
            self.show_airports()

        save_btn = tk.Button(
            btn_frame,
            text="Save Airport",
            command=save_airport,
            bg="#2ecc71",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        save_btn.pack(side="left", padx=5)

        cancel_btn = tk.Button(
            btn_frame,
            text="Cancel",
            command=self.show_airports,
            bg="#95a5a6",
            fg="white",
            font=("Arial", 11, "bold"),
            padx=25,
            pady=8,
            cursor="hand2",
            relief="flat",
        )
        cancel_btn.pack(side="left", padx=5)

    # NEW===============================================================================================================

    def show_aircraft(self):
        """Aircraft management"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Aircraft Management",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        btn_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        btn_frame.pack(pady=10)

        add_btn = tk.Button(
            btn_frame,
            text="+ Add Aircraft",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
            command=self.show_add_aircraft_form,
        )
        add_btn.pack(side="left", padx=5)

        aircraft_frame = tk.LabelFrame(
            self.content_frame,
            text="All Aircraft",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        aircraft_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Registration",
            "Type",
            "Model",
            "Manufacturer",
            "Seats",
            "Year",
        )
        tree = ttk.Treeview(aircraft_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        aircrafts = aircrafts_repo.fetch_all()
        for aircraft in aircrafts:
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    aircraft.id,
                    aircraft.registration_number,
                    aircraft.aircraft_type.model,
                    aircraft.total_seats,
                    aircraft.manufacture_year,
                    aircraft.total_seats,
                    aircraft.manufacture_year,
                ),
            )

        scrollbar = ttk.Scrollbar(aircraft_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        crud_frame = tk.Frame(aircraft_frame, bg="white")
        crud_frame.pack(pady=10)

        edit_btn = tk.Button(
            crud_frame,
            text="Edit",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            crud_frame,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        delete_btn.pack(side="left", padx=5)

    def show_airlines(self):
        """Airlines management"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Airlines Management",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        btn_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        btn_frame.pack(pady=10)

        add_btn = tk.Button(
            btn_frame,
            text="+ Add Airline",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
            command=self.show_add_airline_form,
        )
        add_btn.pack(side="left", padx=5)

        airlines_frame = tk.LabelFrame(
            self.content_frame,
            text="All Airlines",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        airlines_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Name",
            "IATA",
            "Country",
            "Headquarters",
            "Fleet Size",
            "Founded",
        )
        tree = ttk.Treeview(airlines_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        airlines = airlines_repo.fetch_all()
        for airline in airlines:
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    airline.id,
                    airline.name,
                    airline.iata_code.code,
                    airline.country.name,
                    airline.headquarters.name,
                    airline.fleet_size,
                    airline.founder_year,
                ),
            )

        scrollbar = ttk.Scrollbar(airlines_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        crud_frame = tk.Frame(airlines_frame, bg="white")
        crud_frame.pack(pady=10)

        edit_btn = tk.Button(
            crud_frame,
            text="Edit",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            crud_frame,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        delete_btn.pack(side="left", padx=5)

    def show_airports(self):
        """Airports management"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Airports Management",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        btn_frame = tk.Frame(self.content_frame, bg="#ecf0f1")
        btn_frame.pack(pady=10)

        add_btn = tk.Button(
            btn_frame,
            text="+ Add Airport",
            bg="#2ecc71",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
            command=self.show_add_airport_form,
        )
        add_btn.pack(side="left", padx=5)

        airports_frame = tk.LabelFrame(
            self.content_frame,
            text="All Airports",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        airports_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Name",
            "IATA",
            "City",
            "Country",
            "Timezone",
            "Elevation",
        )
        tree = ttk.Treeview(airports_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=110, anchor="center")

        airports = airports_repo.fetch_all()
        for airport in airports:
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    airport.id,
                    airport.name,
                    airport.iata_code.code,
                    airport.city.name,
                    airport.country.name,
                    airport.timezone,
                    airport.elevation,
                ),
            )

        scrollbar = ttk.Scrollbar(airports_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        crud_frame = tk.Frame(airports_frame, bg="white")
        crud_frame.pack(pady=10)

        edit_btn = tk.Button(
            crud_frame,
            text="Edit",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            crud_frame,
            text="Delete",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        delete_btn.pack(side="left", padx=5)

    def show_manage_users(self):
        """User management"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="User Management",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        users_frame = tk.LabelFrame(
            self.content_frame, text="All Users", font=("Arial", 12, "bold"), bg="white"
        )
        users_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = (
            "ID",
            "Email",
            "Name",
            "Phone",
            "Nationality",
            "DOB",
            "Created",
        )
        tree = ttk.Treeview(users_frame, columns=columns, show="headings", height=12)

        for col in columns:
            tree.heading(col, text=col)
            tree.column(col, width=100, anchor="center")

        users = users_repo.fetch_all()
        for user in users:
            tree.insert(
                "",
                "end",
                text="Something",
                values=(
                    user.id,
                    user.email,
                    user.first_name + " " + user.last_name,
                    user.phone,
                    user.nationality.name,
                    user.date_of_birth,
                    user.created_at,
                ),
            )

        scrollbar = ttk.Scrollbar(users_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        btn_frame = tk.Frame(users_frame, bg="white")
        btn_frame.pack(pady=10)

        view_btn = tk.Button(
            btn_frame,
            text="View Details",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        view_btn.pack(side="left", padx=5)

        edit_btn = tk.Button(
            btn_frame,
            text="Edit User",
            bg="#f39c12",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        edit_btn.pack(side="left", padx=5)

        deactivate_btn = tk.Button(
            btn_frame,
            text="Deactivate",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        deactivate_btn.pack(side="left", padx=5)

    def show_all_reviews(self):
        """View all reviews"""
        for widget in self.content_frame.winfo_children():
            widget.destroy()

        tk.Label(
            self.content_frame,
            text="Flight Reviews",
            font=("Arial", 20, "bold"),
            bg="#ecf0f1",
        ).pack(pady=20)

        reviews_frame = tk.LabelFrame(
            self.content_frame,
            text="All Reviews",
            font=("Arial", 12, "bold"),
            bg="white",
        )
        reviews_frame.pack(padx=30, pady=10, fill="both", expand=True)

        columns = ("ID", "User", "Flight", "Airline", "Rating", "Date", "Comment")
        tree = ttk.Treeview(reviews_frame, columns=columns, show="headings", height=12)

        tree.heading("ID", text="ID")
        tree.heading("User", text="User")
        tree.heading("Flight", text="Flight")
        tree.heading("Airline", text="Airline")
        tree.heading("Rating", text="Rating")
        tree.heading("Date", text="Date")
        tree.heading("Comment", text="Comment")

        tree.column("ID", width=50)
        tree.column("User", width=120)
        tree.column("Flight", width=90)
        tree.column("Airline", width=100)
        tree.column("Rating", width=70)
        tree.column("Date", width=100)
        tree.column("Comment", width=250)

        scrollbar = ttk.Scrollbar(reviews_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)

        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)

        btn_frame = tk.Frame(reviews_frame, bg="white")
        btn_frame.pack(pady=10)

        view_btn = tk.Button(
            btn_frame,
            text="View Full Review",
            bg="#3498db",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        view_btn.pack(side="left", padx=5)

        delete_btn = tk.Button(
            btn_frame,
            text="Delete Review",
            bg="#e74c3c",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=15,
            pady=6,
            cursor="hand2",
            relief="flat",
        )
        delete_btn.pack(side="left", padx=5)


# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = FlightBookingSystem(root)
    root.mainloop()
