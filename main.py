from collections import UserDict


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[record.name.value] = record

    def find(self, name: str):  # -> Record:

        for key, value in self.data.items():
            if name == str(key):
                return value

    def delete(self, name) -> str:
        for person in self.data:
            print('16', type(person), person)
            if str(person.value) == name:
                self.data.pop(person)
                return
            # if person == name:
            #     self.data.pop(person)
            #     return

    def edit_record(self, old_name, new_name: str):
        old_record = self.find(old_name)
        print('22', type(old_record))
        if old_record:
            book.delete(old_name)
            print('26', type(old_record.name.value))
            old_record.edit_name(new_name)
            print('28', type(old_record.name.value))
            print('29', old_record.name.value)
            new_record = old_record
            book.add_record(new_record)
            print('29', type(new_record), new_record)
            # return new_record

        else:
            raise KeyError


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):

        super().__init__(value)


class Phone(Field):
    def __init__(self, value):

        if len(str(value)) == 10:
            int(value)
            super().__init__((value))
        else:
            raise ValueError

    # def __eq__(self, other):
    #     return isinstance(other, Phone) and self.value == other.value


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone == None:
            self.phones = []
        else:
            self.phones = [Phone(phone)]

    def add_phone(self, phone: str):
        self.phones.append(Phone(phone))

    def edit_name(self, new_name):
        print('   78', type(self.name))
        self.name.value = new_name
        print('   80', type(self.name), self.name)

    def edit_phone(self, old_phone, new_phone):
        phone = self.find_phone(old_phone)
        if phone:
            self.remove_phone(phone.value)
            self.add_phone(new_phone)

        else:
            raise ValueError

    def find_phone(self, search):

        for phone in self.phones:
            if str(phone.value) == search:
                return phone

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p.value != phone]

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}"


book = AddressBook()


def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return ('\n  There is no contact with this name!\n')
        except ValueError:
            return ('\n  Check the phone number! Should be 10 digits\n')
        except IndexError:
            return ('\n  Check your input!\n')

    return inner


@input_error
def add(user_command):

    name = Name(user_command[1])
    phone = None

    if len(user_command) > 2:
        phone = user_command[2]
        # phone = Phone(user_command[2])

    record = book.find(name.value)
    if not record:
        record = Record(name)

        if phone:
            record.add_phone(phone)

        book.add_record(record)

        return f'\n{str(record)}\n'

    else:
        if len(user_command) < 3:
            return '\n  Add phone number (10 digits)\n'

        record = book.find(name.value)

        if not record.find_phone(phone):
            record.add_phone(phone)
            return f"\n{book.find(name.value)}\n"

        else:

            return f"\n{name.value.title()} and {phone} already exist!\n"


@input_error
def edit(user_command):

    if len(user_command) == 3:
        old_name = user_command[1]
        new_name = user_command[2]
        record = book.find(old_name)

        if book.find(new_name):
            return f'\n  The contact with new name already exists\n'

        if record:
            book.edit_record(old_name, new_name)
            return f'\n{record}\n'
        else:
            raise KeyError

    if len(user_command) == 4:
        name = user_command[1]
        old_phone = user_command[2]
        new_phone = user_command[3]

        record = book.find(name)
        if record:
            record.edit_phone(old_phone, new_phone)
            return f'\n{record}\n'
        else:
            raise KeyError
    else:
        raise IndexError


def console_input():
    return input('> ').lower()


def main():

    print()

    while True:

        user_input = console_input()

        if not user_input:
            continue

        if user_input == 'hello':
            print(f'\n  How can I help you?\n')
            continue

        elif user_input == 'show all':
            show_all()
            continue

        elif user_input in ('good bye', 'close', 'exit'):
            break

        user_command = user_input.split()

        if user_command != []:
            command = user_command[0]
        else:
            continue

        if command == 'add':

            result = add(user_command)
            if result is not None:
                print(result)

        elif command == 'edit':

            result = edit(user_command)
            print(result)

        elif command == 'remove':

            result = remove(user_command)
            print(result)

        elif command == 'find':

            result = find(user_command)
            print(result)

        else:
            print('\n  Check your input!\n')


@input_error
def find(user_command):

    search = user_command[1]

    if search.isdigit():
        phone = search
        for name, record in book.items():
            if record.find_phone(phone):
                return f'\n{record}\n'
            else:
                raise KeyError
    else:

        result = book.find(search)
        if not result:
            raise KeyError
        return f"\n{result}\n"


@input_error
def remove(user_command):

    name = user_command[1]
    record = book.find(name)

    if len(user_command) > 2:

        phone = user_command[2]
        if record.find_phone(phone):
            record.remove_phone(phone)
            return f'\n{record}\n'

        else:
            return book.find(name)

    elif record:

        book.delete(str(record.name.value))
        return '\n  Contact has been removed\n'

    else:
        return '\n  User not found\n'


def show_all():
    if not book:
        print('\n Phone book is empty\n')

    else:
        for name, record in book.data.items():
            print(f'\n{record}\n')


if __name__ == '__main__':

    TEXT = \
        """
                       Commands list
        
    create new contact   - - - > 'add name' or 'add name phone(10 digits)'
    add phone to contact - - - > 'add name phone(10 digits)'
    find name or phone   - - - > 'find name' or 'find phone'
    edit contact name    - - - > 'edit old_name new_name'
    edit conctact phone  - - - > 'edit name old_phone new_phone(10 digits)'
    remove contact       - - - > 'remove name'
    remove phone         - - - > 'remove name phone'
    show all phone book  - - - > 'show all'
    
    """
    print(TEXT)
    main()
