import UserInteract
import PipeLineObject
def main():
    while True:
        user_input = input("Enter patient ID or type 'new' to create a new patient: ").strip()
        
        if user_input.lower() == 'new':
            new_patient = UserInteract.create_new_patient()  # Implement your create_new_patient function
            print(f"New patient created: {new_patient}")
            break

        try:
            patient = PipeLineObject.get_patient_profile(user_input)
            print(f"Patient retrieved: {patient}")
            break
        except ValueError as e:
            print(e)
            print("Please try again or type 'new' to create a new patient.")