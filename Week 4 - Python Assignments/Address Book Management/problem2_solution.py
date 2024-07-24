import pickle

class AddressBook:
    def __init__(self):
        self.addresses = []

    def add_address(self):
        attempt = 0
        while attempt < 3:
            try: 
                fname = input("Enter the first name: ")
                lname = input("Enter the last name: ")
                street = input("Enter the street address: ")
                city = input("Enter the city: ")
                state = input("Enter the state: ")
                country = input("Enter the country: ")
                mobile = input("Enter the mobile number: ")
                email = input("Enter the email address: ")

                if not fname.isalpha() and " " not in fname:
                    raise ValueError("Invalid First Name Format")
                
                if not lname.isalpha() and " " not in lname:
                    raise ValueError("Invalid Last Name Format")
                
                if not city.isalpha() and " " not in city:
                    raise ValueError("Invalid City Name Format")
                
                if not state.isalpha() and " " not in state:
                    raise ValueError("Invalid State Name Format")
                
                if not country.isalpha() and " " not in country:
                    raise ValueError("Invalid Country Name Format")
                
                if not "@" in email or not "." in email:
                    raise ValueError("Invalid Email Format")
                
                if not mobile.isdigit() or len(mobile) != 10:
                    raise ValueError("Invalid Phone Number Format")

                for address in self.addresses:
                 if address['email'] == email or address['mobile'] == mobile:
                    print("Error: Email or mobile number already exists.")
                    return

                 new_address = {
                'fname': fname,
                'lname': lname,
                 'street': street,
                 'city': city,
                 'state': state,
                'country': country,
                'mobile': mobile,
                'email': email
                }
                 
                self.addresses.append(new_address)
                print("Entry added successfully!")
                self.save_to_disk()
                break
            except ValueError as e:
                print(f"Error: {e}")
                attempt += 1
        if attempt == 3:
            print(" Error: Too many incorrect attempts.")


    def save_to_disk(self):
        try:
            with open('problem2_data_file.pickle', 'wb') as f:
                pickle.dump(self.addresses, f)
        except Exception as e:
            print(f"Error saving data to file: {e}")

    def load_from_disk(self):
        try:
            with open('problem2_data_file.pickle', 'rb') as f:
                self.addresses = pickle.load(f)
        except Exception as e:
            print(f"Error loading data from file: {e}")

    def count_first_names(self, fname):
        count = 0
        for address in self.addresses:
            if address['fname'] == fname:
                count += 1
        return count

    def count_last_names(self, lname):
        count = 0
        for address in self.addresses:
            if address['lname'] == lname:
                count += 1
        return count

    def count_streets(self, street):
        count = 0
        for address in self.addresses:
            if address['street'] == street:
                count += 1
        return count
     
    def count_occurrences(self, search_term):
        count = 0
        for address in self.addresses:
            if address['fname'] == search_term or address[
                    'lname'] == search_term or address[
                        'street'] == search_term:
                count += 1
        return count

def main():
    addresses = AddressBook()
    addresses.load_from_disk()
    while True:
        print("\nAddress Book Menu:")
        print("1. Add Entry")
        print("2. Find number of occurrences of a First Name ")
        print("3. Find number of occurrences of a Last Name ")
        print("4. Find number of occurrences of a Street Name ")
        print("5. Find number of occurrences of a First Name, Last Name or Street Name ")
        print("6. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            addresses.add_address()
          
        elif choice == "2":
            fname = input("Enter the term to search First Name: ")
            print(f"Number of Occurrences: {addresses.count_first_names(fname)}")

        elif choice == "3":
            lname = input("Enter the term to search Last Name: ")          
            print(f"Number of Occurrences: {addresses.count_last_names(lname)}")

        elif choice == "4":
            street = input("Enter the term to search (Street Address): ")
            print(f"Number of Occurrences: {addresses.count_streets(street)}")

        elif choice == "5":
            search_term = input("Enter the term to search (First Name, Last Name, or Street Address): ")
            print(f"Number of Occurrences: {addresses.count_occurrences(search_term)}")

        elif choice == "6":
            print("Thank you for using the Address Book.")
            break
        else:
            print("Error: Invalid choice. Please enter a number between 1 and 6.")

if __name__ == "__main__":
    main()
