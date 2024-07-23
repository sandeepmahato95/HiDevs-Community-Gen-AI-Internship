import pickle

class PersonData:
    def __init__(self):
        self.data = {}
        self.load_data()

    def load_data(self):
        try:
            with open("problem1_data_file.pickle", "rb") as file:
                self.data = pickle.load(file)
        except (FileNotFoundError, EOFError):
            self.data = {}

    def save_data(self):
        with open("problem1_data_file.pickle", "wb") as file:
            pickle.dump(self.data, file)

    def add_person(self):
        for attempt in range(3):
            try:
                name = input("Enter person's name: ").strip()
                if not name:
                    raise ValueError("Name cannot be empty.")
                dob = input("Enter person's date of birth (dd-mm-yyyy) or 'secret': ").strip()
                if not dob or (dob.lower() != 'secret' and not self.validate_dob(dob)):
                    raise ValueError("Invalid date of birth format.")
                self.data[name] = dob
                self.save_data()
                print("Data saved successfully.")
                return
            except ValueError as e:
                print(f"Error: {e}")
                if attempt == 2:
                    print("Max attempts reached. Exiting the function.")

    def get_dob(self):
        name = input("Enter person's name to retrieve DOB: ").strip()
        dob = self.data.get(name, "Person not found.")
        if dob.lower() == "secret":
            print("DOB is secret.")
        else:
            print(f"{name}'s DOB is {dob}")

    def validate_dob(self, dob):
        from datetime import datetime
        try:
            datetime.strptime(dob, "%d-%m-%Y")
            return True
        except ValueError:
            return False

# Testing the class
person_data = PersonData()

# Adding persons
person_data.add_person()

# Retrieving DOB
person_data.get_dob()
