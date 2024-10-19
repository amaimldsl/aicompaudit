import csv
import PyPDF2
from langchain_ollama import ChatOllama

# Function to load transactions from CSV
def load_transactions(csv_file):
    transactions = []
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            transactions.append(row)
    return transactions

# Function to extract policy text from PDF
def extract_policy_text(pdf_file):
    with open(pdf_file, 'rb') as file:
        reader = PyPDF2.PdfReader(file)
        policy_text = ""
        for page_num in range(len(reader.pages)):
            policy_text += reader.pages[page_num].extract_text()
    return policy_text

# Function to query ChatOllama for transaction analysis
def check_transaction_against_policy(transaction, policy_text):
    # Convert the transaction dictionary to a string format
    transaction_str = ', '.join(f"{key}: {value}" for key, value in transaction.items())
    
    # Format the conversation as a list of messages
    messages = [
        {"role": "system", "content": "You are a policy compliance assistant."},
        {"role": "user", "content": f"Given the following policy:\n\n{policy_text}\n\nDoes the following transaction violate any policy constraints? Transaction: {transaction_str}\nAnswer 'Yes' or 'No' and explain why."}
    ]
    
    # Initialize the ChatOllama model
    chat_ollama = ChatOllama(model="mistral")
    
    # Get the response from the model
    result = chat_ollama.invoke(messages)
    
    return result

# Main function to check all transactions
def check_transactions(csv_file, pdf_file):
    transactions = load_transactions(csv_file)
    policy_text = extract_policy_text(pdf_file)
    
    violations = []
    for transaction in transactions:
        result = check_transaction_against_policy(transaction, policy_text)
        if ("Yes" in result.content):  # Assuming "Yes" indicates a violation
            violations.append({"transaction": transaction, "result": result})
    
    return violations

# Example usage
if __name__ == "__main__":
    csv_file = './data/transactions.csv'
    pdf_file = './docs/policy.pdf'
    violations = check_transactions(csv_file, pdf_file)

    # Output violations
    for violation in violations:
        print(f"Transaction: {violation['transaction']}\nViolation: {violation['result']}\n")
