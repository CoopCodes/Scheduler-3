import os
import random
from sys import platform

lists_path = "Lists/" if platform == "linux" or platform == "linux2" else "Lists\\"
lists = []

def process_command(command):
    """Processes a command and performs the appropriate action.

    Args:
        command (str): The command to be processed.
    """
    global lists_path, lists
    if not ':' in command:
        command = command.lower()
    else:
        command = command.split(':')[0].lower() + ':' + command.split(':')[1]

    lists = []
    # Get lists
    for list in os.listdir(lists_path):
        if list.endswith(".txt"):
            lists.append(list[:-4].lower())


    # Split the command into the list name and the action
    try:
        if (e := [substring in command for substring in lists]):
            list_name = lists[e.index(True)]
            action = command.split(lists[e.index(True)])[1].strip().lower()
            if ':' in action: action = action.split(':')[0].strip().lower()
    except ValueError:
        list_name, action = '', ''         
        

    print(list_name, action)

    rand_emojies = "😀😁😂🤣😃😄😅😆😉😊😋😎😍😘🥰😗😙😚☺️🙂🤗🤩🤔🤨😐😑😶🙄😏😣😥😮🤐😯😪😫😴😌😛😜😝🤤😒😓😔😕🙃🤑😲☹️🙁😖😞😟😤😢😭😦😧😨😩🤯😬😰😱😳🤪😵😡😠🤬😷🤒🤕🤢🤮🤧😇🤠🤡🤥🤫🤭🧐🤓😈👿👹👺💀☠️👻👽👾🤖💩😺😸😹😻😼😽🙀😿😾"
    # Get the list corresponding to the list name
    task_list = get_task_list(list_name) if list_name in lists else []

    return_value = ""

    # Perform the appropriate action
    if action == "add" and list_name != "lists":
        # Add the item to the list
        item = command.split(": ")[1]
        if '|' not in command:
            task_list.append(item)
            save_task_list(list_name, task_list)
        
        else:
            items = command.split('|')
            items[0] = items[0].split(': ')[1]
            for item in items:
                item = item[0].strip() + item[1:]
                task_list.append(item)
            save_task_list(list_name, task_list)
        return_value = "👍"
    elif action == "delete":
        # Delete the item from the list
        try: index = int(command.split(": ")[1])
        except ValueError: return_value = "Not integer"
        if (index != 0):
            try:
                del task_list[index]
            except IndexError:
                return
        save_task_list(list_name, task_list)
        list_as_string = '\n'.join([str(item) if i == 0 else "- " + str(item) for i, item in enumerate(task_list)])
        return_value = (list_as_string, rand_emojies[random.randint(0, len(rand_emojies) - 1)])
    elif action == "clear":
        # Clear the list
        task_list = [task_list[0]]
        save_task_list(list_name, task_list)
        return_value = "👍"
    elif action == "?" and list_name != "lists":
        # Print the list
        list_as_string = '\n'.join([str(item) if i == 0 else "- " + str(item) for i, item in enumerate(task_list)])
        return_value = list_as_string

    if command.split(": ")[0] == "lists add":
        create_new_list(command.split(": ")[1])
        return_value = "👍"
    elif command.split(": ")[0] == "delete list":
        file_path = lists_path + command.split(": ")[1] + '.txt'
        try:
            os.remove(file_path)
            return_value = "👍"
        except OSError as e:
            return_value = (f"Error: {file_path} could not be deleted. {e}", "👎")
    elif command.split(": ")[0] == "lists?":
        return_value = "All Lists:\n------------------------------------------\n"
        for list in lists:
            return_value += '\n'.join([str(item) if i == 0 else "- " + str(item) for i, item in enumerate(get_task_list(list))]) + "\n------------------------------------------\n"

    if return_value == "":
        return None

    # if len(task_list) == 1:
    #     task_list.append('Empty')
    # elif len(task_list) > 1 and 'Empty' in task_list:
    #     task_list.remove('Empty')

    save_task_list(list_name, task_list)

    return return_value

def get_task_list(list_name):
    """Gets the task list corresponding to the given list name.

    Args:
        list_name (str): The name of the task list.

    Returns:
        list: The task list corresponding to the given list name.
    """
    global lists
    for list in lists:
        if list == list_name:
            return load_task_list(list_name + '.txt')

def save_task_list(list_name, task_list):
    """Saves the given task list to the specified file.

    Args:
        list_name (str): The name of the file to save the task list to.
        task_list (list): The task list to be saved.
    """
    global lists_path
    if os.path.isfile(lists_path + list_name + '.txt'):
        with open(lists_path + list_name + ".txt", "w") as f:
            for item in task_list:
                f.write(item + "\n")

def load_task_list(list_name):
    """Loads the task list from the specified file.

    Args:
        list_name (str): The name of the file to load the task list from.

    Returns:
        list: The task list loaded from the file.
    """
    global lists_path
    task_list = []
    if os.path.exists(lists_path + list_name):
        with open(lists_path + list_name, "r") as f:
            for line in f:
                task_list.append(line.strip())
    return task_list

def create_new_list(list_name):
    """Creates a new task list with the given name.

    Args:
        list_name (str): The name of the new task list.
    """
    global lists_path, lists
    with open(lists_path + list_name + ".txt", "w") as f:
        f.write(f"{list_name[0].upper() + list_name[1::].lower()}:\n")

    lists.append(list_name)
    print(lists)

def main():
    # Read the command from the user
    command = input("Enter a command: ")

    # Process the command
    print(process_command(command))


if __name__ == "__main__":
    main()

