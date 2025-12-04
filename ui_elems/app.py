import tkinter as tk
from tkinter import ttk
import bcrypt

from Flight_Project.repositories.AircraftTypesRepository import AircraftTypesRepository
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
from Flight_Project.repositories.ManufacturersRepository import ManufacturersRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.UsersRepository import UsersRepository

from Flight_Project.ui_elems.login_screen import show_login_screen
from Flight_Project.ui_elems.register_screen import show_register_screen


class FlightBookingSystem:
    def __init__(self, root):

        self.db_manager = RepositoryManager()
        self.countries_repo = CountriesRepository(self.db_manager)
        self.cities_repo = CitiesRepository(self.db_manager, self.countries_repo)
        self.iata_codes_repo = IATACodesRepository(self.db_manager)
        self.airlines_repo = AirlinesRepository(
            self.db_manager, self.countries_repo, self.cities_repo, self.iata_codes_repo
        )
        self.manufacturer_repo = ManufacturersRepository(self.db_manager)
        self.aircraft_types_repo = AircraftTypesRepository(
            self.db_manager, self.manufacturer_repo
        )
        self.aircrafts_repo = AircraftsRepository(
            self.db_manager, self.aircraft_types_repo
        )
        self.airports_repo = AirportsRepository(
            self.db_manager, self.iata_codes_repo, self.cities_repo, self.countries_repo
        )
        self.flights_status_repo = FlightStatusesRepository(self.db_manager)
        self.amenities_repo = AmenitiesRepository(self.db_manager)
        self.users_repo = UsersRepository(self.db_manager, self.countries_repo)
        self.bookings_repo = BookingsRepository(self.db_manager, self.users_repo)
        self.flights_repo = FlightsRepository(
            self.db_manager,
            self.airlines_repo,
            self.aircrafts_repo,
            self.airports_repo,
            self.flights_status_repo,
            self.amenities_repo,
            self.bookings_repo,
        )
        self.flights_repo.set_bookings_repo(self.bookings_repo)
        self.bookings_repo.set_flights_repo(self.flights_repo)

        self.root = root
        self.root.title("Flight Booking System")
        self.root.geometry("1200x700")
        self.root.configure(bg="#f0f0f0")

        self.style = ttk.Style()
        self.style.theme_use("clam")

        self.user_role = None
        self.current_user = None
        self.salt = bcrypt.gensalt()

        # Show login screen first
        self.show_login_screen()

    def clear_window(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    # ====================== SCREENS ===========================

    def show_login_screen(self):
        self.clear_window()
        show_login_screen(self)

    def show_register_screen(self):
        self.clear_window()
        show_register_screen(self)
