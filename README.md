**Scooter Rental Management System**
**Overview**
This is a command-line based Scooter Rental Management System implemented in Python. It simulates a real-world scooter rental service, allowing customers to:

**View available scooters**
Rent scooters (hourly, daily, or weekly)
Return rented scooters and process payments
Generate rental and inventory reports
The system uses object-oriented design with enumerations, classes, and interfaces for extensibility, maintainability, and scalability.

**Features**
Scooter Types: STANDARD and PREMIUM
Rental Periods: Hourly, Daily, Weekly
Maintenance Tracking: Scooters require maintenance after a set number of rides
Payment Simulation: 95% chance of payment success (dummy implementation)
Discounts: 30% discount for renting 3 to 5 scooters
Reports: Summary of inventory, rentals, revenue, and maintenance needs
Error Handling: Checks for scooter availability, active rentals, and payment failures

**Requirements**
Python 3.6 or higher

**How to Run**
Clone or download the repository.
Open a terminal or command prompt.
Navigate to the directory containing scooter_rental_system.py.

**Usage**
View Available Scooters: Lists all scooters that are currently available for rental.
Rent Scooters: Enter customer ID, number of scooters, and rental period (HOURLY, DAILY, WEEKLY) to rent scooters.
Return Scooters: Enter customer ID to return rented scooters and process payment.
Generate Report: Displays summary statistics about scooters, rentals, revenue, and maintenance.
Exit: Closes the program.

**Code Structure**
ScooterType and RentalPeriod: Enumerations for scooter categories and rental durations.
Scooter: Class representing each scooter with state and maintenance tracking.
RentalTransaction: Manages details of a rental transaction, including cost calculation.
PaymentProcessor: Simulates a payment system.
ScooterRental: Main controller managing inventory, rentals, payments, and reports.
main(): Entry point presenting the CLI menu and handling user input.

**Future Improvements**
Implement a GUI or web interface for better user experience.
Integrate with a real payment gateway.
Add user authentication and customer management.
Store data persistently using a database.
Add detailed maintenance scheduling and alerts.
