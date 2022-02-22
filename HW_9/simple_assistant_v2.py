import functools

ADDRESS_BOOK = {}

def input_error(func):
    @functools.wraps(func)
    def check_error(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError as err_key:
            return err_key
        except ValueError:
            return "Please enter the valid contact's phone number"
        except IndexError as err_idx:
            return err_idx
        except TypeError:
            return "Please enter the contact's name"
    return check_error

def hello_handler():
    return "How can I help you?"

@input_error
def add_handler(input_str):
    name, phone = input_str.split()
    ADDRESS_BOOK[name.strip().capitalize()] = int(phone.strip())
    return f"Address Book has been updated. Contact {name.capitalize()} with a phone number: {int(phone)} has been added."

@input_error
def change_handler(input_str):
    name, phone = input_str.split()
    if name.capitalize() not in ADDRESS_BOOK:
        return f"The contact name {name.capitalize()} is not in the Address Book. To add it please use the command 'add'."
    if name.capitalize() in ADDRESS_BOOK:
        ADDRESS_BOOK[name.strip().capitalize()] = int(phone.strip())
        return f"Address Book has been updated. The new phone number of {name.capitalize()} is: {int(phone)}"

@input_error
def phone_handler(input_str):
    name = input_str.capitalize()
    phone_search = ADDRESS_BOOK.get(name)
    if phone_search:
        return f"{name.capitalize()}'s phone number: {phone_search}"
    else:
        return f"There is no entry named {name.capitalize()} in the Address Book."

def show_all_handler():
    if len(ADDRESS_BOOK) == 0:
        return "Address Book is empty"
    else:
        return "\n".join(f"{k}: {v}" for k, v in ADDRESS_BOOK.items())

def good_bye_handler():
    return "Good bye!"

def main():
    while True:
        try:
            user_input = input("Input command: ")
            parced_msg=user_input.split()
            for word in (action_commands+exit_commands):
                if word.find(parced_msg[0]) == 0:
                    cmd_words = word.split()
                    user_cmd_len = len(cmd_words)
                    if user_cmd_len == 2:
                        word = ' '.join(parced_msg[:2])
                    else:
                        word = parced_msg[0]
                    if word in exit_commands:
                        print(good_bye_handler())
                        quit()
                    elif word in action_commands:
                        if user_cmd_len == 1:
                            func_arg = parced_msg[1:]
                            if len(func_arg) == 0:
                                print(commands_func[word]())
                            else:
                                func_arg = ' '.join(func_arg)
                                print(commands_func[word](func_arg))
                        elif user_cmd_len == 2:
                            func_arg = parced_msg[2:]
                            if len(func_arg) == 0:
                                print(commands_func[word]())
                            else:
                                func_arg = ' '.join(func_arg)
                                print(commands_func[word](func_arg))
                        else:
                            print("Assistant does not recognize your command. Please input your request.")
        except Exception:
            print("Please enter a valid command")


if __name__ == "__main__":
    action_commands = ['hello','add','change','phone','show all']
    action_func_list = [hello_handler, add_handler, change_handler, phone_handler, show_all_handler]
    commands_func = {cmd: func for cmd, func in zip(action_commands, action_func_list)}
    exit_commands = ['good bye', 'close', 'exit']
    main()