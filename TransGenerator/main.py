import csv
import random
from datetime import datetime, timedelta

# Generate random dates between two dates
def random_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))

# Function to generate a random transaction
def generate_transaction(transaction_id, start_date, end_date, vendors, policies_violated=False):
    date = random_date(start_date, end_date)
    amount = round(random.uniform(2000, 15000), 2)
    vendor = random.choice(vendors)
    purchase_order_id = f"PO{random.randint(1000, 1999)}"
    transaction_type = random.choice(['Purchase', 'Invoice'])
    discount = round(random.uniform(0, 25), 2)
    tax_paid = random.choice(['Yes', 'No'])
    submitted_date = random_date(date, date + timedelta(days=35))
    authorization = random.choice(['Yes', 'No'])
    item_description = random.choice([
        'Office Computers', 'Laptops', 'Projector', 'Server Maintenance', 'Conference Room Setup', 
        'Printer Supplies', 'Software Subscription', 'Security System Installation', 'Consulting Services',
        'IT Equipment'
    ])

    # Add policy violations in approximately 10% of cases
    if policies_violated:
        violation_type = random.choice(['exceeds_limit', 'missing_authorization', 'no_tax', 'high_discount', 'late_submission', 'duplicate'])
        
        if violation_type == 'exceeds_limit':
            amount = round(random.uniform(10500, 20000), 2)  # Violates maximum purchase limit
        elif violation_type == 'missing_authorization':
            amount = round(random.uniform(6000, 15000), 2)  # Requires authorization but set to 'No'
            authorization = 'No'
        elif violation_type == 'no_tax':
            tax_paid = 'No'  # No tax for a non-exempt vendor
        elif violation_type == 'high_discount':
            discount = round(random.uniform(18, 25), 2)  # Discount above 15% without approval
        elif violation_type == 'late_submission':
            submitted_date = date + timedelta(days=35 + random.randint(1, 10))  # Submitted late
        elif violation_type == 'duplicate':
            purchase_order_id = f"PO1004"  # Duplicate PO ID

    return {
        'Transaction ID': transaction_id,
        'Date': date.strftime('%Y-%m-%d'),
        'Amount': amount,
        'Vendor': vendor,
        'Purchase Order ID': purchase_order_id,
        'Type': transaction_type,
        'Discount': f'{discount}%',
        'Tax Paid': tax_paid,
        'Submitted Date': submitted_date.strftime('%Y-%m-%d'),
        'Authorization': authorization,
        'Item Description': item_description
    }

# Generate 500 transactions, with 10% policy violations
def generate_transactions(num_transactions=500, violation_rate=0.1):
    transactions = []
    vendors = ['Vendor A', 'Vendor B', 'Vendor C', 'Vendor D', 'Vendor E', 
               'Vendor F', 'Vendor G', 'Vendor H', 'Vendor I']
    
    start_date = datetime.strptime('2024-07-01', '%Y-%m-%d')
    end_date = datetime.strptime('2024-10-18', '%Y-%m-%d')
    
    num_violations = int(num_transactions * violation_rate)
    transaction_id = 1
    
    for _ in range(num_transactions):
        policies_violated = transaction_id <= num_violations
        transaction = generate_transaction(f"T{transaction_id:03d}", start_date, end_date, vendors, policies_violated)
        transactions.append(transaction)
        transaction_id += 1
    
    return transactions

# Write transactions to a CSV file
def write_transactions_to_csv(transactions, filename='transactions.csv'):
    fieldnames = ['Transaction ID', 'Date', 'Amount', 'Vendor', 'Purchase Order ID', 'Type', 'Discount', 'Tax Paid', 'Submitted Date', 'Authorization', 'Item Description']
    with open(filename, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

# Main execution
transactions = generate_transactions(500, violation_rate=0.1)
write_transactions_to_csv(transactions)
print(f"{len(transactions)} transactions generated and saved to 'transactions.csv'.")
