from collections import UserDict

class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]
class Field:
    def __init__(self, value=None):
        self.value = value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)



class Phone(Field):
    def __init__(self, value):
        if value is not None and not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        super().__init__(value)

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []

    def add_phone(self, phone):
        if Phone.validate_phone(phone):
            self.phones.append(Phone(phone))
        else:
            raise ValueError("Invalid phone number format")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]





    def edit_phone(self, phone, new_phone):
        if Phone.validate_phone(new_phone):
            found = False

            for i, existing_phone in enumerate(self.phones):

                if existing_phone == phone:
                    self.phones[i] = Phone(new_phone)
                    found = True
                    break

            if not found:
                raise ValueError("There isn't a phone like the one you provided")
        else:
            raise ValueError("Invalid phone number format")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p


class AddressBook:
    def __init__(self):
        self.data = {}

    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]


def handle_command(address_book, command):
    action, *args = command.lower().split()

    if action == "add":
        if len(args) < 2:
            return "Invalid format for 'add' command. Please provide a name and at least one phone number."
        name, *phones = args
        record = Record(name)
        for phone in phones:
            record.add_phone(phone)
        address_book.add_record(record)
        phones_str = ', '.join([p.value for p in record.phones])
        return f"Contact {name} added with phones: {phones_str}"

    elif action == "change":
        if len(args) < 2:
            return "Invalid format for 'change' command. Please provide a name and a new phone number."
        name, phone = args
        record = address_book.find(name)
        if record:
            record.edit_phone(phone, phone)
            return f"Contact {name} phone number changed to {phone}"
        else:
            return f"Contact {name} not found"

    elif action == "phone":
        if len(args) < 1:
            return "Invalid format for 'phone' command. Please provide a name."
        name = args[0]
        record = address_book.find(name)
        if record:
            phones_str = ', '.join([p.value for p in record.phones])
            return f"Phone number for {name}: {phones_str}"
        else:
            return f"Contact {name} not found"

    elif action == "show" and args[0] == "all":
        if not address_book.data:
            return "No contacts found"
        else:
            contacts = [f"{name}: {', '.join([p.value for p in record.phones])}" for name, record in
                        address_book.data.items()]
            return "\n".join(contacts)

    elif action == "hello":
        return "How can I help you?"

    elif action in ["goodbye", "close", "exit"]:
        return "Good bye!"

    else:
        return "Unknown command"


def main():
    print("Welcome to ContactBot!")
    address_book = AddressBook()

    while True:
        command = input("Enter a command: ").strip()

        if command.lower() in ["goodbye", "close", "exit"]:
            print("Good bye!")
            break

        response = handle_command(address_book, command)
        print(response)


if __name__ == "__main__":
    main()
