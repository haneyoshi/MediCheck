import UserRequest
"""
**UI is under developing
**introduction about this program is in README.md

some sample input for testing
patient id: Z567890123
symptoms: cough, fever
diagnose: common cold
"""

def main():
    print("Medicheck Symtem Starts")
    UserRequest.program_start()
    while True:
        print("\nOptions:")
        print("1. Check in a patient (type 'check in')")
        print("2. Take the next patient (type 'next')")
        print("3. Exit the system (type 'exit')")
        
        user_request = input("Enter your command: ").strip().lower()

        if user_request == "check in":
            UserRequest.patient_check_in()
        elif user_request == "next":
            UserRequest.take_next_patient()
        elif user_request == "exit":
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid command. Please try again.")

# This ensures the script runs when executed directly
if __name__ == "__main__":
    main()