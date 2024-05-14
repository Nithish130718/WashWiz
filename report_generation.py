"""
    An attempt to create a report generation feature for admins. Not integrated with the other part of the backend.
"""

import datetime

class LaundryService:
    def __init__(self):
        self.customers = []
        self.transactions = []

    def add_transaction(self, transaction):
        self.transactions.append(transaction)

    def add_customer(self, customer):
        self.customers.append(customer)

    def generate_daily_report(self, date):
        daily_transactions = [t for t in self.transactions if t.date == date]
        self._generate_report(daily_transactions, "Daily Report")

    def generate_weekly_report(self, start_date, end_date):
        weekly_transactions = [
            t for t in self.transactions if start_date <= t.date <= end_date
        ]
        self._generate_report(weekly_transactions, "Weekly Report")

    def generate_monthly_report(self, month, year):
        monthly_transactions = [
            t
            for t in self.transactions
            if t.date.month == month and t.date.year == year
        ]
        self._generate_report(monthly_transactions, "Monthly Report")

    def _generate_report(self, transactions, report_type):
        print(f"\n{report_type}")
        print("==========================================")
        total_revenue = 0

        for transaction in transactions:
            print(f"Transaction ID: {transaction.transaction_id}")
            print(f"Customer ID: {transaction.customer.customer_id}")
            print(f"Date: {transaction.date}")
            print(f"Total Cost: {transaction.total_cost}")
            print()
            print("******************************************")
            total_revenue += transaction.total_cost

        print(f"\nTotal Revenue: {total_revenue}")
        print("===================================")


class Customer:
    def __init__(self, customer_id, name, contact):
        self.customer_id = customer_id
        self.name = name
        self.contact = contact


class Transaction:
    transaction_counter = 1

    def __init__(self, customer, date, total_cost):
        self.transaction_id = Transaction.transaction_counter
        self.customer = customer
        self.date = date
        self.total_cost = total_cost
        Transaction.transaction_counter += 1


# Example Usage:

# Create LaundryService instance
laundry_service = LaundryService()

# Add customers
customer1 = Customer(1, "John Doe", "123-456-7890")
customer2 = Customer(2, "Jane Smith", "987-654-3210")
laundry_service.add_customer(customer1)
laundry_service.add_customer(customer2)

# Make transactions
transaction1 = Transaction(customer1, datetime.date(2023, 11, 1), 20)
transaction2 = Transaction(customer2, datetime.date(2023, 11, 1), 30)
transaction3 = Transaction(customer1, datetime.date(2023, 11, 2), 15)
laundry_service.add_transaction(transaction1)
laundry_service.add_transaction(transaction2)
laundry_service.add_transaction(transaction3)

# Generate reports
laundry_service.generate_daily_report(datetime.date(2023, 11, 1))
laundry_service.generate_weekly_report(
    datetime.date(2023, 11, 1), datetime.date(2023, 11, 7)
)
laundry_service.generate_monthly_report(11, 2023)
