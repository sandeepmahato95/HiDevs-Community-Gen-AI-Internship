import pickle
import datetime

class PersonalInfo:
    
    def __init__(self, filename="problem1_data_file.pickle"):
        self.filename = filename
        self.data = {}
        try:
            with open(self.filename, "rb") as file:
                self.data = pickle.load(file)
        except FileNotFoundError:
            pass

    def add_info(self):
        for attempt in range(3):
            name = input("Enter the name: ")
            try:
                if not name.isalpha() and " " not in name:
                    raise ValueError("Invalid name format")
            except ValueError as e:
                print(f"Error: {e}. Please try again.")
                continue
            
            dob_input = input("Enter the date of birth (DD-MM-YYYY): ")
            try:
                dob = datetime.datetime.strptime(dob_input, "%d-%m-%Y").date()
            except ValueError:
                print("Error: Invalid date format. Please enter in DD-MM-YYYY format.")
                continue
            
            secret = input("Is this date of birth secret? (yes/no): ").lower()
            if secret == "yes":
                self.data[name] = "secret"
            else:
                self.data[name] = dob
            
            self.save_data()
            print("Information added successfully!")
            break
        else:
            print("Too many incorrect attempts. Try again.")

    def display_info(self):
        name = input("Enter the name to display the date of birth: ")
        if name in self.data:
            if self.data[name] == "secret":
                print("Secret")
            else:
                print(f"Date of Birth: {self.data[name]}")
        else:
            print("Person not found.")

    def save_data(self):
        with open(self.filename, "wb") as file:
            pickle.dump(self.data, file)

def main():
    info = PersonalInfo()

    while True:
        print("\nChoose an option:")
        print("1. Add Personal Information")
        print("2. Display Personal Information")
        print("3. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
           info.add_info()
        elif choice == "2":
           info.display_info()
        elif choice == "3":
           print("Exiting the personal information management system.")
           break
        else:
            print("Error: Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
