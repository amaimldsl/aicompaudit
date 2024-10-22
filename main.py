import csv
import PyPDF2
from langchain_ollama import ChatOllama
from tqdm import tqdm  # Import tqdm for progress bar

LLM_MISTRAL = "mistral"
LLM_LLAMA31 = "llama3.1"
LLM_PHI3="phi3"
LLM_LLAMA31_70B = "llama3.1:70b"

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
def check_transaction_against_policy(transaction, policy_text,llm):
    # Convert the transaction dictionary to a string format
    transaction_str = ', '.join(f"{key}: {value}" for key, value in transaction.items())
    
    # Format the conversation as a list of messages
    messages = [
        {"role": "system", "content": "You are a policy compliance assistant."},
        {"role": "user", "content": f"Given the following policy:\n\n{policy_text}\n\nDoes the following transaction violate any policy constraints? Transaction: {transaction_str}\nAnswer 'Yes' or 'No' and explain why."}
    ]
    
    # Initialize the ChatOllama model
    


    chat_ollama = ChatOllama(model=llm)
    
    # Get the response from the model
    result = chat_ollama.invoke(messages)
    
    return result

import csv
import time
from tqdm import tqdm

# Main function to check all transactions
def check_transactions(csv_file, pdf_file, output_file):
    transactions = load_transactions(csv_file)
    policy_text = extract_policy_text(pdf_file)
    
    total_time = 0
    transaction_count = len(transactions)

    llm=LLM_LLAMA31

    print(f"Using {llm} LLM...")
    

    # Add a violation column to the transactions
    for transaction in tqdm(transactions, desc="Analyzing Transactions"):  # Adding tqdm for progress
        start_time = time.time()  # Start time for the current transaction
        result = check_transaction_against_policy(transaction, policy_text,llm)
        transaction['violation'] = result.content if "Yes" in result.content else "No violation"
        elapsed_time = time.time() - start_time  # Time taken for this transaction
        total_time += elapsed_time  # Accumulate total time

    # Calculate average time per transaction
    average_time = total_time / transaction_count if transaction_count > 0 else 0

    # Write the updated transactions to a new CSV file
    with open(output_file, mode='w', newline='') as file:
        fieldnames = list(transactions[0].keys())  # Get the field names from the first transaction
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(transactions)

    # Output total and average time
    print(f"Total consumed time: {total_time:.2f} seconds")
    print(f"Average time per transaction: {average_time:.2f} seconds")

    return transactions


# Example usage
if __name__ == "__main__":
    csv_file = './data/transactions.csv'
    pdf_file = './docs/policy.pdf'
    output_file = './output/transactions_with_violations.csv'  # Specify the output CSV file path
    violations = check_transactions(csv_file, pdf_file, output_file)

    # Output violations
    for violation in violations:
        print(f"Transaction: {violation}\nViolation: {violation['violation']}\n")
