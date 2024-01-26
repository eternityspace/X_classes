from collections import UserDict


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

    def __eq__(self, other):
        return isinstance(other, Phone) and self.value == other.value


class Record:
    def __init__(self, name, phone=None):
        self.name = Name(name)
        if phone == None:
            self.phones = []
        else:
            self.phones = [phone]

    def add_phone(self, phone: str):
        self.phones.append(phone)

    def remove_phone(self, phone):
        self.phones = [p for p in self.phones if p != phone]

    def edit_phone(self, old_phone, new_phone):
        idx = self.phones.index(old_phone)
        self.phones[idx] = new_phone
        # print(new_phone == '4444444444')

    def edit_name(self, new_name):
        self.name = Name(new_name)

    def find_phone(self, search):

        for phone in self.phones:
            if phone == search:
                return Phone(phone)

    def __str__(self):
        return f"Contact name: {self.name.value}, phones: {'; '.join(p for p in self.phones)}"


class AddressBook(UserDict):
    def add_record(self, record):
        self.data[str(record.name)] = record

    def find(self, name):
        return self.data.get(name, None)

    def delete(self, record):
        name = record
        if name in self.data:
            del self.data[name]


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
        # phone = Phone(user_command[2])
        phone = user_command[2]

    if name.value not in book:

        record = Record(name)

        if phone:
            record.add_phone(phone)

        book.add_record(record)

        return f'\n{str(record)}\n'

    else:

        if len(user_command) < 3:

            return '\n  Add phone number (10 digits)\n'

        if phone.value not in [str(p) for p in book[name.value].phones]:

            book[name.value].add_phone(phone)
            return f"\n{book[name.value]}\n"

        else:

            return f"\n{name.value.title()} and {phone} already exist!\n"


@input_error
def edit(user_command):

    if len(user_command) == 3:
        old_name = user_command[1]
        new_name = user_command[2]
        record = book.find(old_name)

        if book.find(new_name):
            return f'\n  The contact with new name already exist\n'

        if record:
            book.delete(record)
            record.edit_name(new_name)
            book.add_record(record)
            return f'\n{record}\n'
        else:
            return '\n  Name not found\n'

    if len(user_command) == 4:
        name = user_command[1]
        old_phone = user_command[2]
        new_phone = user_command[3]

        record = book.find(name)

        if record:
            record.edit_phone(old_phone, new_phone)
            return f'\n{record}\n'
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
                return f'\nUser not found\n'
    else:

        result = book.find(search)
        if not result:
            return f'\n  Name not found\n'
        return f"\n{result}\n"


@input_error
def remove(user_command):

    name = user_command[1]
    record = book.find(name)

    if len(user_command) > 2:
        phone = user_command[2]
        if record.find_phone(phone):
            record.remove_phone(phone)
            print('\n  Phone has been removed\n')
            return f'\n{record}\n'
        else:
            return book.find(name)

    elif record:
        book.delete(record.name)

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
