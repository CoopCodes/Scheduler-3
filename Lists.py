import os
import random
from sys import platform

lists_path = "Lists/" if platform == "linux" or platform == "linux2" else "Lists\\"

def process_command(command):
    """Processes a command and performs the appropriate action.
    
    Args:
        command (str): The command to be processed.
    """

    # Split the command into the list name and the action
    try:
        list_name, action = command.split()[0], command.split()[1]
        pass
    except IndexError:
        list_name, action = (command[:-1], command[-1])  

    rand_emojies = "💋✌️👻🤡👀😩🤤🫦"

    # Get the list corresponding to the list name
    task_list = get_task_list(list_name)

    return_value = ''
    
    # Perform the appropriate action
    if action == "add:":
        # Add the item to the list
        item = command.split(": ")[1]
        task_list.append(item)
        save_task_list(list_name, task_list)
        return_value = "👍"
    elif action == "delete:":
        # Delete the item from the list
        try: index = int(command.split(": ")[1]) 
        except ValueError: return_value = "Not integer"
        if (index != 0 and isinstance(index, str)):
            del task_list[index]
        save_task_list(list_name, task_list)
        list_as_string = '\n'.join([str(item) if i == 0 else "- " + str(item) for i, item in enumerate(task_list)])
        return_value = (list_as_string, rand_emojies[random.randint(0, len(rand_emojies) - 1)])
    elif action == "clear":
        # Clear the list
        task_list = [task_list[0]]
        save_task_list(list_name, task_list)
        return_value = "👍"
    elif action == "?":
        # Print the list
        list_as_string = '\n'.join([str(item) if i == 0 else "- " + str(item) for i, item in enumerate(task_list)])
        return_value = list_as_string
    else:
        # raise Exception("Incorrect Command")
        return_value = 'Not interacting with list'
    
    if len(task_list) == 1:
        task_list.append('Empty')
    elif len(task_list) > 1 and 'Empty' in task_list:
        task_list.remove('Empty')

    save_task_list(list_name, task_list)

    return return_value

def get_task_list(list_name):
    """Gets the task list corresponding to the given list name.
    
    Args:
        list_name (str): The name of the task list.
    
    Returns:
        list: The task list corresponding to the given list name.
    """
    if list_name == "programming":
        return load_task_list("programming.txt")
    elif list_name == "homework":
        return load_task_list("homework.txt")
    elif list_name == "chores":
        return load_task_list("chores.txt")
    elif list_name == "todo":
        return load_task_list("todo.txt")

def save_task_list(list_name, task_list):
    """Saves the given task list to the specified file.
    
    Args:
        list_name (str): The name of the file to save the task list to.
        task_list (list): The task list to be saved.
    """
    global lists_path
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

def main():
    # Read the command from the user
    command = input("Enter a command: ")
    
    # Process the command
    process_command(command)

if __name__ == "__main__":
    main()

