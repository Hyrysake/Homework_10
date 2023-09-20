from datetime import datetime

class Field:
    def __init__(self, value=None):
        self.value = value

    def set_value(self, value):
        self.value = value

    def get_value(self):
        return self.value


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def set_value(self, value):
        if value is not None and not self.validate_phone(value):
            raise ValueError("Invalid phone number format")
        self.value = value

    @staticmethod
    def validate_phone(phone):
        return len(phone) == 10 and phone.isdigit()


class Birthday(Field):
    def __init__(self, value=None):
        super().__init__(value)

    def set_value(self, value):
        try:
            datetime.strptime(value, "%d.%m.%y")
        except ValueError:
            raise ValueError("Invalid date format. Please use 'dd.mm.yy' format.")

        self.value = value

    def days_to_birthday(self):
        if self.value is None:
            return None
        birth_date = datetime.strptime(self.value, "%d.%m.%y")
        current_date = datetime.now()
        difference = birth_date - current_date
        days_until_birthday = difference.days

        if days_until_birthday < 0:
            next_birthday_year = current_date.year + 1
            next_birthday_date = datetime(next_birthday_year, birth_date.month, birth_date.day)
            difference = next_birthday_date - current_date
            days_until_birthday = difference.days

        return days_until_birthday


class Record:
    def __init__(self, name, birthday=None):
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone):
        if Phone.validate_phone(phone):
            self.phones.append(Phone(phone))
        else:
            raise ValueError("Invalid phone number format")

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def edit_phone(self, phone, new_phone):
        for p in self.phones:
            if p.value == phone:
                p.set_value(new_phone)
                break
        else:
            raise ValueError("Phone number not found")

    def find_phone(self, phone):
        for p in self.phones:
            if p.value == phone:
                return p


class AddressBook:
    def __init__(self):
        self.data = {}
        self.page_size = 10

    def add_record(self, record):
        self.data[record.name.get_value()] = record

    def find(self, name):
        return self.data.get(name)

    def delete(self, name):
        if name in self.data:
            del self.data[name]

    def iterator(self):
        records = list(self.data.values())
        for i in range(0, len(records), self.page_size):
            yield records[i:i + self.page_size]


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
        phones_str = ', '.join([p.get_value() for p in record.phones])
        return f"Contact {name} added with phones: {phones_str}"

    elif action == "birthday" and args[0]:
        if len(args) < 2:
            return "Invalid format for 'add birthday' command. Please provide a name and a birthday date."
        name = args[0]
        birthday = args[1]
        record = Record(name, birthday)
        address_book.add_record(record)
        response = f"Contact {name} added with birthday: {birthday}"
        days_left = record.birthday.days_to_birthday()
        if days_left is not None:
            response += f"\n{days_left} days left until the next birthday."
        return response

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
            phones_str = ', '.join([p.get_value() for p in record.phones])
            return f"Phone number for {name}: {phones_str}"
        else:
            return f"Contact {name} not found"

    elif action == "show" and args[0] == "all":
        if not address_book.data:
            return "No contacts found"
        else:
            contacts = [f"{name}: {', '.join([p.get_value() for p in record.phones])}" for name, record in
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