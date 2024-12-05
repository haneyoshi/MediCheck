import UserRequest
import PipeLineObject

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