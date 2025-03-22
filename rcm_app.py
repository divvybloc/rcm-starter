import time

# Simulated token authentication
def get_auth_token():
    print("🔐 Simulating token retrieval...")
    time.sleep(1)
    return "mock-token-12345"

# Simulated patient data
def fetch_patient_data():
    print("📥 Fetching mock patient data...\n")
    time.sleep(1)
    return [
        {
            "patient_id": "P001",
            "name": "Alice Carter",
            "dob": "1982-04-19",
            "insurance": "Blue Cross",
            "outstanding_claims": 2
        },
        {
            "patient_id": "P002",
            "name": "David Kim",
            "dob": "1975-08-03",
            "insurance": "UnitedHealth",
            "outstanding_claims": 0
        }
    ]

# Simulated claim submission
def submit_mock_claim(patient_id, amount, diagnosis_code):
    print(f"📝 Submitting claim for patient {patient_id}...")
    time.sleep(1)
    return {
        "claim_id": "CLM-987654",
        "status": "Submitted",
        "amount": amount,
        "diagnosis": diagnosis_code
    }

# Simulated claim status check
def fetch_claim_status(claim_id):
    print(f"📊 Checking status for claim {claim_id}...")
    time.sleep(1)
    return {
        "claim_id": claim_id,
        "status": "Pending review",
        "expected_payment_date": "2025-04-15"
    }

# Display menu options
def show_menu():
    print("\n📋 RCM MENU")
    print("1. View Patient List")
    print("2. Submit a Claim")
    print("3. Check Claim Status")
    print("4. Exit")

def main():
    print("🚀 Welcome to the RCM Demo App with Mock Data\n")
    token = get_auth_token()
    patients = fetch_patient_data()
    claim_id = None

    while True:
        show_menu()
        choice = input("\nEnter your choice (1-4): ").strip()

        if choice == "1":
            print("\n👩‍⚕️ Patient List:")
            for p in patients:
                print(f" - {p['name']} ({p['insurance']}) - {p['outstanding_claims']} claim(s)")

        elif choice == "2":
            print("\n🧾 Submit a Claim")
            patient_id = input("Enter patient ID (e.g., P001): ").strip()
            amount = float(input("Enter claim amount (e.g., 150.00): ").strip())
            diagnosis_code = input("Enter diagnosis code (e.g., J10.1): ").strip()
            response = submit_mock_claim(patient_id, amount, diagnosis_code)
            claim_id = response["claim_id"]
            print("✅ Claim submitted:", response)

        elif choice == "3":
            if not claim_id:
                print("⚠️ No claim submitted yet. Please submit a claim first.")
            else:
                status = fetch_claim_status(claim_id)
                print("📈 Claim Status:", status)

        elif choice == "4":
            print("👋 Exiting the app. Goodbye!")
            break

        else:
            print("❌ Invalid choice. Please enter 1, 2, 3, or 4.")

if __name__ == "__main__":
    main()
