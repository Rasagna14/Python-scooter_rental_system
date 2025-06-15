# scooter_rental_system.py

from abc import ABC, abstractmethod
from enum import Enum
from datetime import datetime, timedelta
import random

class ScooterType(Enum):
    STANDARD = "Standard"
    PREMIUM = "Premium"

class RentalPeriod(Enum):
    HOURLY = "Hourly"
    DAILY = "Daily"
    WEEKLY = "Weekly"

class Scooter:
    def __init__(self, scooter_id, scooter_type):
        self.scooter_id = scooter_id
        self.scooter_type = scooter_type
        self.available = True
        self.maintenance_needed = False
        self.rides_since_maintenance = 0

    def rent(self):
        if self.available and not self.maintenance_needed:
            self.available = False
            self.rides_since_maintenance += 1
            if self.rides_since_maintenance >= 10:
                self.maintenance_needed = True
        else:
            raise Exception("Scooter is not available or needs maintenance")

    def return_scooter(self):
        self.available = True

    def perform_maintenance(self):
        self.rides_since_maintenance = 0
        self.maintenance_needed = False

class IPaymentProcessor(ABC):
    @abstractmethod
    def process_payment(self, amount):
        pass

class PaymentProcessor(IPaymentProcessor):
    def process_payment(self, amount):
        return random.random() < 0.95

class RentalTransaction:
    def __init__(self, customer_id, scooters, rental_period):
        self.customer_id = customer_id
        self.scooters = scooters
        self.rental_period = rental_period
        self.start_time = datetime.now()
        self.end_time = None
        self.cost = 0.0

    def end_rental(self):
        self.end_time = datetime.now()
        self.cost = self.calculate_cost()
        return self.cost

    def calculate_cost(self):
        duration = self.end_time - self.start_time
        count = len(self.scooters)
        cost_per_scooter = {
            RentalPeriod.HOURLY: 5,
            RentalPeriod.DAILY: 20,
            RentalPeriod.WEEKLY: 50
        }[self.rental_period]

        multiplier = {
            RentalPeriod.HOURLY: duration.total_seconds() / 3600,
            RentalPeriod.DAILY: duration.days + 1,
            RentalPeriod.WEEKLY: (duration.days // 7) + 1
        }[self.rental_period]

        total = count * cost_per_scooter * multiplier
        if 3 <= count <= 5:
            total *= 0.7  # 30% discount
        return round(total, 2)

class ScooterRental:
    def __init__(self):
        self.scooters = []
        self.active_rentals = {}
        self.rental_history = []
        self.total_revenue = 0.0
        self.payment_processor = PaymentProcessor()

    def add_scooter(self, scooter_type):
        scooter_id = len(self.scooters) + 1
        scooter = Scooter(scooter_id, scooter_type)
        self.scooters.append(scooter)

    def get_available_scooters(self):
        return [s for s in self.scooters if s.available and not s.maintenance_needed]

    def rent_scooters(self, customer_id, number_of_scooters, rental_period):
        if customer_id in self.active_rentals:
            print("Customer already has an active rental.")
            return
        available = self.get_available_scooters()
        if len(available) < number_of_scooters:
            print("Not enough scooters available.")
            return
        scooters_to_rent = available[:number_of_scooters]
        for scooter in scooters_to_rent:
            scooter.rent()
        transaction = RentalTransaction(customer_id, scooters_to_rent, rental_period)
        self.active_rentals[customer_id] = transaction
        print("Scooters rented successfully.")

    def return_scooters(self, customer_id):
        if customer_id not in self.active_rentals:
            print("No active rental found.")
            return
        transaction = self.active_rentals.pop(customer_id)
        cost = transaction.end_rental()
        if self.payment_processor.process_payment(cost):
            for scooter in transaction.scooters:
                scooter.return_scooter()
            self.rental_history.append(transaction)
            self.total_revenue += cost
            print(f"Payment successful. Total cost: ${cost}")
        else:
            print("Payment failed. Please try again.")

    def generate_report(self):
        total_scooters = len(self.scooters)
        available = len(self.get_available_scooters())
        maintenance = len([s for s in self.scooters if s.maintenance_needed])
        print("----- Report -----")
        print(f"Total Scooters: {total_scooters}")
        print(f"Available Scooters: {available}")
        print(f"In Maintenance: {maintenance}")
        print(f"Total Revenue: ${self.total_revenue}")
        print(f"Total Rentals: {len(self.rental_history)}")

# ----------- Main Program -----------
def main():
    system = ScooterRental()
    for _ in range(20):
        system.add_scooter(ScooterType.STANDARD)
    for _ in range(10):
        system.add_scooter(ScooterType.PREMIUM)

    while True:
        print("\n--- Scooter Rental System ---")
        print("1. View Available Scooters")
        print("2. Rent Scooters")
        print("3. Return Scooters")
        print("4. Generate Report")
        print("5. Exit")

        choice = input("Choose an option: ")

        if choice == '1':
            scooters = system.get_available_scooters()
            for s in scooters:
                print(f"ID: {s.scooter_id}, Type: {s.scooter_type.value}")

        elif choice == '2':
            customer_id = input("Customer ID: ")
            count = int(input("Number of scooters to rent: "))
            print("Rental Period Options: HOURLY, DAILY, WEEKLY")
            period = input("Rental Period: ").upper()
            try:
                system.rent_scooters(customer_id, count, RentalPeriod[period])
            except Exception as e:
                print(f"Error: {e}")

        elif choice == '3':
            customer_id = input("Customer ID: ")
            system.return_scooters(customer_id)

        elif choice == '4':
            system.generate_report()

        elif choice == '5':
            print("Exiting the system.")
            break

        else:
            print("Invalid choice. Try again.")

if __name__ == "__main__":
    main()
