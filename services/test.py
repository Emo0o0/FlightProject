import datetime
from typing import Optional, List

from Flight_Project.entities.Aircraft import Aircraft
from Flight_Project.entities.AircraftType import AircraftType
from Flight_Project.entities.Airline import Airline
from Flight_Project.entities.Airport import Airport
from Flight_Project.entities.Amenity import Amenity
from Flight_Project.entities.Booking import Booking
from Flight_Project.entities.City import City
from Flight_Project.entities.Country import Country
from Flight_Project.entities.Flight import Flight
from Flight_Project.entities.FlightStatus import FlightStatus
from Flight_Project.entities.FlightStatusHistory import FlightStatusHistory
from Flight_Project.entities.IATACode import IATACode
from Flight_Project.entities.Manufacturer import Manufacturer
from Flight_Project.entities.Payment import Payment
from Flight_Project.entities.PaymentMethod import PaymentMethod
from Flight_Project.entities.Review import Review
from Flight_Project.entities.Ticket import Ticket
from Flight_Project.entities.TicketStatusHistory import TicketStatusHistory
from Flight_Project.entities.User import User
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
from Flight_Project.repositories.FlightsStatusHistoryRepository import (
    FlightsStatusHistoryRepository,
)
from Flight_Project.repositories.IATACodesRepository import IATACodesRepository
from Flight_Project.repositories.ManufacturersRepository import ManufacturersRepository
from Flight_Project.repositories.PaymentMethodsRepository import (
    PaymentMethodsRepository,
)
from Flight_Project.repositories.PaymentsRepository import PaymentsRepository
from Flight_Project.repositories.RepositoryManager import RepositoryManager
from Flight_Project.repositories.ReviewsRepository import ReviewsRepository
from Flight_Project.repositories.TicketsRepository import TicketsRepository
from Flight_Project.repositories.TicketsStatusHistoryRepository import (
    TicketsStatusHistoryRepository,
)
from Flight_Project.repositories.UsersRepository import UsersRepository


def create_amenity(name: str):
    return Amenity(name=name, id=None)


def create_flight_status_history(flight, old_status, new_status, notes):
    return FlightStatusHistory(
        flight=flight,
        old_status=old_status,
        new_status=new_status,
        changed_at=datetime.datetime.now().isoformat(),
        notes=notes,
        id=None,
    )


def create_payment_method(method: str):
    return PaymentMethod(method=method, id=None)


def create_payment(booking, amount, payment_method):
    return Payment(
        booking=booking,
        amount=amount,
        payment_method=payment_method,
        paid_at=datetime.datetime.now().isoformat(),
        id=None,
    )


def create_review(user, flight, rating, description):
    return Review(
        user=user,
        flight=flight,
        rating=rating,
        description=description,
        created_at=datetime.datetime.now().isoformat(),
        id=None,
    )


def create_ticket(
    ticket_number, booking, flight, user, seat_number, ticket_class, ticket_status
):
    # Simplified timestamps for issued/checked in/etc.
    now = datetime.datetime.now().isoformat()
    return Ticket(
        ticket_number=ticket_number,
        booking=booking,
        flight=flight,
        user=user,
        seat_number=seat_number,
        ticket_class=ticket_class,
        ticket_status=ticket_status,
        issued_at=now,
        checked_in_at=None,
        boarded_at=None,
        cancelled_at=None,
        no_show_at=None,
        id=None,
    )


def create_ticket_status_history(ticket, old_status, new_status, notes):
    return TicketStatusHistory(
        ticket=ticket,
        old_status=old_status,
        new_status=new_status,
        changed_at=datetime.datetime.now().isoformat(),
        notes=notes,
        id=None,
    )


# =============================================================================


def create_country(name, code):
    return Country(name=name, country_code=code, id=None)


def create_city(name, country):
    return City(name=name, country=country, id=None)


def create_iata_code(code):
    return IATACode(code=code, id=None)


def create_manufacturer(name):
    return Manufacturer(name=name, id=None)


def create_aircraft_type(
    model, manufacturer, engine_count, engine_type, range_km, cruise_speed_kmh
):
    return AircraftType(
        model=model,
        manufacturer=manufacturer,
        engine_count=engine_count,
        engine_type=engine_type,
        range_km=range_km,
        cruise_speed_kmh=cruise_speed_kmh,
        id=None,
    )


def create_aircraft(aircraft_type, registration_number, total_seats, manufacture_year):
    return Aircraft(
        aircraft_type=aircraft_type,
        registration_number=registration_number,
        total_seats=total_seats,
        manufacture_year=manufacture_year,
        id=None,
    )


def create_airport(name, iata_code, country, city, timezone, elevation):
    return Airport(
        name=name,
        iata_code=iata_code,
        country=country,
        city=city,
        timezone=timezone,
        elevation=elevation,
        id=None,
    )


def create_airline(
    name, iata_code, email, phone, country, headquarters, fleet_size, founded_year
):
    return Airline(
        name=name,
        iata_code=iata_code,
        email=email,
        phone=phone,
        country=country,
        headquarters=headquarters,
        fleet_size=fleet_size,
        founded_year=founded_year,
        id=None,
    )


def create_flight_status(status_str):
    return FlightStatus(status=status_str, id=None)


def create_user(
    email,
    password,
    first_name,
    last_name,
    phone,
    nationality,
    date_of_birth,
    passport_number,
):
    return User(
        email=email,
        password=password,
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        nationality=nationality,
        date_of_birth=date_of_birth,
        passport_number=passport_number,
        created_at=datetime.datetime.now().isoformat(),
        id=None,
    )


# ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# --- Sample Data Generation ---
db_manager = RepositoryManager()
# 1. Base Geographical Data
country_repo = CountriesRepository(db_manager)
country_repo.create_table()
usa = create_country("United States", "US")
france = create_country("France", "FR")
japan = create_country("Japan", "JP")
country_repo.save(usa)
country_repo.save(france)
country_repo.save(japan)


cities_repo = CitiesRepository(db_manager, country_repo)
cities_repo.create_table()
nyc = create_city("New York City", usa)
paris = create_city("Paris", france)
tokyo = create_city("Tokyo", japan)
cities_repo.save(nyc)
cities_repo.save(paris)
cities_repo.save(tokyo)


# 2. Manufacturers & Aircraft Types
manufacturers_repo = ManufacturersRepository(db_manager)
manufacturers_repo.create_table()
boeing_mfg = create_manufacturer("Boeing")
airbus_mfg = create_manufacturer("Airbus")
manufacturers_repo.save(boeing_mfg)
manufacturers_repo.save(airbus_mfg)

aircraft_types_repo = AircraftTypesRepository(db_manager, manufacturers_repo)
aircraft_types_repo.create_table()
b737_type = create_aircraft_type("Boeing 737-800", boeing_mfg, 2, "Jet", 5430, 840)
a380_type = create_aircraft_type("Airbus A380-800", airbus_mfg, 4, "Jet", 15200, 900)
aircraft_types_repo.save(b737_type)
aircraft_types_repo.save(a380_type)


# 3. Specific Aircrafts
aircrafts_repo = AircraftsRepository(db_manager, aircraft_types_repo)
aircrafts_repo.create_table()
aircraft_n1 = create_aircraft(b737_type, "N123AA", 180, 2018)
aircraft_n2 = create_aircraft(a380_type, "F-ABCD", 550, 2010)
aircrafts_repo.save(aircraft_n1)
aircrafts_repo.save(aircraft_n2)

# IATA Codes
iata_codes_repo = IATACodesRepository(db_manager)
iata_codes_repo.create_table()
jfk_iata = create_iata_code("JFK")
cdg_iata = create_iata_code("CDG")
hnd_iata = create_iata_code("HND")
aa_iata = create_iata_code("AA")
af_iata = create_iata_code("AF")
iata_codes_repo.save(jfk_iata)
iata_codes_repo.save(cdg_iata)
iata_codes_repo.save(hnd_iata)
iata_codes_repo.save(aa_iata)
iata_codes_repo.save(af_iata)

# 4. Airports

airports_repo = AirportsRepository(
    db_manager, iata_codes_repo, cities_repo, country_repo
)
airports_repo.create_table()
jfk = create_airport(
    "John F. Kennedy Intl", jfk_iata, usa, nyc, "America/New_York", "4m"
)
cdg = create_airport(
    "Charles de Gaulle Airport", cdg_iata, france, paris, "Europe/Paris", "42m"
)
hnd = create_airport("Haneda Airport", hnd_iata, japan, tokyo, "Asia/Tokyo", "6m")
print(jfk.iata_code.id)
print(cdg.iata_code.id)
print(hnd.iata_code.id)
airports_repo.save(jfk)
airports_repo.save(cdg)
airports_repo.save(hnd)


# 5. Airlines
airlines_repo = AirlinesRepository(
    db_manager, country_repo, cities_repo, iata_codes_repo
)
airlines_repo.create_table()
american_airlines = create_airline(
    "American Airlines",
    aa_iata,
    "contact@aa.com",
    "+1-800-433-7300",
    usa,
    nyc,
    900,
    1926,
)
air_france = create_airline(
    "Air France",
    af_iata,
    "support@airfrance.fr",
    "+33-9-69-36-79-79",
    france,
    paris,
    230,
    1933,
)
airlines_repo.save(american_airlines)
airlines_repo.save(air_france)

# 6. Flight Statuses
flight_statuses_repo = FlightStatusesRepository(db_manager)
flight_statuses_repo.create_table()
scheduled_status = create_flight_status("Scheduled")
departed_status = create_flight_status("Departed")
arrived_status = create_flight_status("Arrived")
flight_statuses_repo.save(scheduled_status)
flight_statuses_repo.save(departed_status)
flight_statuses_repo.save(arrived_status)


# Amenities
amenities_repo = AmenitiesRepository(db_manager)
amenities_repo.create_table()
wifi = create_amenity("In-flight WiFi")
meal = create_amenity("Complimentary Meal")
priority = create_amenity("Priority Boarding")
amenities_repo.save(wifi)
amenities_repo.save(meal)
amenities_repo.save(priority)

# --- 5 Flights ---
users_repo = UsersRepository(db_manager, country_repo)
users_repo.create_table()
bookings_repo = BookingsRepository(db_manager, users_repo)
bookings_repo.create_table()
flights_repo = FlightsRepository(
    db_manager,
    airlines_repo,
    aircrafts_repo,
    airports_repo,
    flight_statuses_repo,
    bookings_repo,
)
flights_repo.create_table()
bookings_repo.set_flights_repo(flights_repo)

flights: List[Flight] = [
    Flight(
        flight_number="AA100",
        airline=american_airlines,
        aircraft=aircraft_n1,
        origin_airport=jfk,
        destination_airport=cdg,
        expected_departure_time="2025-12-10T08:00:00Z",
        expected_arrival_time="2025-12-10T16:00:00Z",
        actual_departure_time="2025-12-10T08:05:00Z",
        actual_arrival_time="2025-12-10T15:55:00Z",
        total_seats=180,
        available_seats=25,
        seat_price=750.00,
        flight_status=arrived_status,
        departure_gate="B42",
        departure_terminal="T8",
        arrival_gate="M10",
        arrival_terminal="T2E",
        amenities=[wifi, meal],
    ),
    Flight(
        flight_number="AF007",
        airline=air_france,
        aircraft=aircraft_n2,
        origin_airport=cdg,
        destination_airport=jfk,
        expected_departure_time="2025-12-11T10:00:00Z",
        expected_arrival_time="2025-12-11T13:00:00Z",
        actual_departure_time=None,
        actual_arrival_time=None,
        total_seats=550,
        available_seats=450,
        seat_price=820.50,
        flight_status=scheduled_status,
        departure_gate="L45",
        departure_terminal="T2E",
        arrival_gate="A10",
        arrival_terminal="T1",
        amenities=[wifi, priority],
    ),
    Flight(
        flight_number="AA201",
        airline=american_airlines,
        aircraft=aircraft_n1,
        origin_airport=jfk,
        destination_airport=hnd,
        expected_departure_time="2025-12-12T14:00:00Z",
        expected_arrival_time="2025-12-13T18:00:00Z",
        actual_departure_time="2025-12-12T14:00:00Z",
        actual_arrival_time=None,
        total_seats=180,
        available_seats=10,
        seat_price=1200.00,
        flight_status=departed_status,
        departure_gate="C3",
        departure_terminal="T8",
        arrival_gate=None,
        arrival_terminal=None,
        amenities=[wifi],
    ),
    Flight(
        flight_number="AF888",
        airline=air_france,
        aircraft=aircraft_n2,
        origin_airport=hnd,
        destination_airport=cdg,
        expected_departure_time="2025-12-15T22:00:00Z",
        expected_arrival_time="2025-12-16T06:00:00Z",
        actual_departure_time=None,
        actual_arrival_time=None,
        total_seats=550,
        available_seats=500,
        seat_price=950.00,
        flight_status=scheduled_status,
        departure_gate="101",
        departure_terminal="3",
        arrival_gate=None,
        arrival_terminal=None,
        amenities=[wifi, meal],
    ),
    Flight(
        flight_number="AA500",
        airline=american_airlines,
        aircraft=aircraft_n1,
        origin_airport=jfk,
        destination_airport=jfk,  # Round trip example for demo
        expected_departure_time="2025-12-14T09:00:00Z",
        expected_arrival_time="2025-12-14T12:00:00Z",
        actual_departure_time=None,
        actual_arrival_time=None,
        total_seats=180,
        available_seats=180,
        seat_price=250.00,
        flight_status=scheduled_status,
        departure_gate="A1",
        departure_terminal="T8",
        arrival_gate="A1",
        arrival_terminal="T8",
        amenities=[
            meal,
        ],
    ),
]
for flight in flights:
    flights_repo.save(flight)

# --- Users (for Bookings) ---
user1 = create_user(
    "alice@example.com",
    "securepass123",
    "Alice",
    "Smith",
    "555-1234",
    usa,
    "1990-01-01",
    "AB1234567",
)
user2 = create_user(
    "bob@example.com",
    "bobspass",
    "Bob",
    "Johnson",
    "555-5678",
    france,
    "1985-05-15",
    "CD7654321",
)
user3 = create_user(
    "charlie@example.com",
    "password456",
    "Charlie",
    "Williams",
    "555-8765",
    japan,
    "2000-11-20",
    "EF9876543",
)
users_repo.save(user1)
users_repo.save(user2)
users_repo.save(user3)


# --- 10 Bookings ---
bookings: List[Booking] = [
    Booking(
        booking_reference="BK10001",
        user=user1,
        number_of_passengers=2,
        total_amount=1500.00,
        created_at="2025-11-01T10:00:00Z",
        id=1,
        flights=[flights[0]],  # Flight AA100
    ),
    Booking(
        booking_reference="BK10002",
        user=user2,
        number_of_passengers=1,
        total_amount=820.50,
        created_at="2025-11-05T14:30:00Z",
        id=2,
        flights=[flights[1]],  # Flight AF007
    ),
    Booking(
        booking_reference="BK10003",
        user=user1,
        number_of_passengers=1,
        total_amount=1200.00,
        created_at="2025-11-10T09:15:00Z",
        id=3,
        flights=[flights[2]],  # Flight AA201
    ),
    Booking(
        booking_reference="BK10004",
        user=user3,
        number_of_passengers=3,
        total_amount=2850.00,
        created_at="2025-11-12T20:00:00Z",
        id=4,
        flights=[flights[3]],  # Flight AF888
    ),
    Booking(
        booking_reference="BK10005",
        user=user2,
        number_of_passengers=1,
        total_amount=250.00,
        created_at="2025-11-15T11:00:00Z",
        id=5,
        flights=[flights[4]],  # Flight AA500
    ),
    # Multi-flight booking example (User 1 books a round trip)
    Booking(
        booking_reference="BK10006",
        user=user1,
        number_of_passengers=2,
        total_amount=3941.00,
        created_at="2025-11-18T16:00:00Z",
        id=6,
        flights=[flights[2], flights[3]],  # JFK-HND and HND-CDG (connecting example)
    ),
    Booking(
        booking_reference="BK10007",
        user=user3,
        number_of_passengers=4,
        total_amount=3800.00,
        created_at="2025-11-20T08:00:00Z",
        id=7,
        flights=[flights[0]],
    ),
    Booking(
        booking_reference="BK10008",
        user=user2,
        number_of_passengers=2,
        total_amount=1641.00,
        created_at="2025-11-22T21:00:00Z",
        id=8,
        flights=[flights[1]],
    ),
    Booking(
        booking_reference="BK10009",
        user=user1,
        number_of_passengers=1,
        total_amount=750.00,
        created_at="2025-11-25T07:00:00Z",
        id=9,
        flights=[flights[0]],
    ),
    Booking(
        booking_reference="BK10010",
        user=user3,
        number_of_passengers=1,
        total_amount=1200.00,
        created_at="2025-11-28T13:00:00Z",
        id=10,
        flights=[flights[2]],
    ),
]

for booking in bookings:
    bookings_repo.save(booking)


# Payment Methods
payment_methods_repo = PaymentMethodsRepository(db_manager)
payment_methods_repo.create_table()
credit_card_method = create_payment_method("Credit Card")
paypal_method = create_payment_method("PayPal")
payment_methods_repo.save(credit_card_method)
payment_methods_repo.save(paypal_method)

# Payments
payments_repo = PaymentsRepository(db_manager, bookings_repo, payment_methods_repo)
payments_repo.create_table()
payment1 = create_payment(bookings[0], 1500.00, credit_card_method)
payment2 = create_payment(bookings[1], 820.50, paypal_method)
payments_repo.save(payment1)
payments_repo.save(payment2)

# Reviews
reviews_repo = ReviewsRepository(db_manager, users_repo, flights_repo)
reviews_repo.create_table()
review1 = create_review(user1, flights[0], 4, "Great flight, arrived early!")
review2 = create_review(user2, flights[4], 3, "Service was okay, plane felt old.")
reviews_repo.save(review1)
reviews_repo.save(review2)

# Tickets
tickets_repo = TicketsRepository(db_manager, bookings_repo, flights_repo, users_repo)
tickets_repo.create_table()
ticket1 = create_ticket(
    ticket_number="TKT789012",
    booking=bookings[0],
    flight=flights[0],
    user=user1,
    seat_number="12A",
    ticket_class="economy",
    ticket_status="active",
)

ticket2 = create_ticket(
    ticket_number="TKT789013",
    booking=bookings[0],  # Same booking, second passenger
    flight=flights[0],
    user=user1,  # Assuming user1 made booking for both people for simplicity
    seat_number="12B",
    ticket_class="economy",
    ticket_status="active",
)
tickets_repo.save(ticket1)
tickets_repo.save(ticket2)

# Flights History
flights_history_repo = FlightsStatusHistoryRepository(
    db_manager, flights_repo, flight_statuses_repo
)
flights_history_repo.create_table()
history_f1_1 = create_flight_status_history(
    flight=flights[0],
    old_status=scheduled_status,
    new_status=departed_status,
    notes="Departed slightly late due to baggage loading.",
)

history_f1_2 = create_flight_status_history(
    flight=flights[0],
    old_status=departed_status,
    new_status=arrived_status,
    notes="Arrived ahead of schedule.",
)
flights_history_repo.save(history_f1_1)
flights_history_repo.save(history_f1_2)

# Tickets History
tickets_history_repo = TicketsStatusHistoryRepository(db_manager, tickets_repo)
tickets_history_repo.create_table()
history_t1_1 = create_ticket_status_history(
    ticket=ticket1,
    old_status="active",
    new_status="checked_in",
    notes="Checked in via mobile app.",
)
tickets_history_repo.save(history_t1_1)
