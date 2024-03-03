import os
from datetime import datetime, date

def reg_user(username_password):
    # Add a new user to user.txt
    new_username = input("New Username: ")
    if new_username in username_password:
        print("Username already exists. Please choose a different one.")
        continue
    new_password = input("New Password: ")
    confirm_password = input("Confirm Password: ")

    if new_password == confirm_password:
        print("New user added")
        username_password[new_username] = new_password
        with open("user.txt", "w") as out_file:
            user_file = [f"{k};{v}" for k, v in username_password.items()]
            out_file.write("\n".join(user_file))
    else:
        print("Passwords do not match")

def add_task(tasks):
    # Allow a user to add a new task to tasks.txt
    task_username = input("Name of person assigned to task: ")
    if task_username not in username_password:
        print("User does not exist. Please enter a valid username")
        continue
    task_title = input("Title of Task: ")
    task_description = input("Description of Task: ")
    while True:
        try:
            task_due_date = input("Due date of task (YYYY-MM-DD): ")
            due_date_time = datetime.strptime(task_due_date, DATETIME_STRING_FORMAT)
            break
        except ValueError:
            print("Invalid datetime format. Please use the format specified")

    curr_date = date.today()
    new_task = {
        "username": task_username,
        "title": task_title,
        "description": task_description,
        "due_date": due_date_time,
        "assigned_date": curr_date,
        "completed": False
    }

    tasks.append(new_task)
    with open("tasks.txt", "w") as task_file:
        task_list_to_write = [
            f"{t['username']};{t['title']};{t['description']};{t['due_date'].strftime(DATETIME_STRING_FORMAT)};"
            f"{t['assigned_date'].strftime(DATETIME_STRING_FORMAT)};{'Yes' if t['completed'] else 'No'}"
            for t in tasks
        ]
        task_file.write("\n".join(task_list_to_write))
    print("Task successfully added.")

def view_all(task_list):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling) 
    '''

    for t in task_list:
        disp_str = f"Task: \t\t {t['title']}\n"
        disp_str += f"Assigned to: \t {t['username']}\n"
        disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
        disp_str += f"Task Description: \n {t['description']}\n"
        print(disp_str)

def view_mine(task_list, curr_user):
    '''Reads the task from task.txt file and prints to the console in the 
        format of Output 2 presented in the task pdf (i.e. includes spacing
        and labelling)
    '''
    for t in task_list:
        if t['username'] == curr_user:
            disp_str = f"Task: \t\t {t['title']}\n"
            disp_str += f"Assigned to: \t {t['username']}\n"
            disp_str += f"Date Assigned: \t {t['assigned_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Due Date: \t {t['due_date'].strftime(DATETIME_STRING_FORMAT)}\n"
            disp_str += f"Task Description: \n {t['description']}\n"
            print(disp_str)

def  gen_report(username_password, tasks):
    '''Generates reports about number of users and tasks'''
    print(f"Users: {len(username_password)}")
    print(f"Tasks: {len(tasks)}")


    
# Define the datetime string format as a constant
DATETIME_STRING_FORMAT = "%Y-%m-%d"

# Create tasks.txt if it doesn't exist
if not os.path.exists("tasks.txt"):
    with open("tasks.txt", "w"):
        pass

# Read task data from tasks.txt
with open("tasks.txt", 'r') as task_file:
    task_data = [task.strip() for task in task_file.readlines() if task.strip()]

# Create a list to store task dictionaries
tasks = []

# Populate the list with task dictionaries
for task_str in task_data:
    task_components = task_str.split(";")
    task = {
        'username': task_components[0],
        'title': task_components[1],
        'description': task_components[2],
        'due_date': datetime.strptime(task_components[3], DATETIME_STRING_FORMAT),
        'assigned_date': datetime.strptime(task_components[4], DATETIME_STRING_FORMAT),
        'completed': True if task_components[5] == "Yes" else False
    }
    tasks.append(task)

# Create user.txt if it doesn't exist
if not os.path.exists("user.txt"):
    with open("user.txt", "w") as user_file:
        user_file.write("admin;password")

# Read user data from user.txt
with open("user.txt", 'r') as user_file:
    user_data = [user.strip() for user in user_file.readlines()]

# Convert user data to a dictionary
username_password = {}
for user in user_data:
    username, password = user.split(';')
    username_password[username] = password

# Implement user login
logged_in = False
while not logged_in:
    print("LOGIN")
    curr_user = input("Username: ")
    curr_pass = input("Password: ")
    if curr_user not in username_password:
        print("User does not exist")
    elif username_password[curr_user] != curr_pass:
        print("Wrong password")
    else:
        print("Login Successful!")
        logged_in = True

# Main program loop
while True:
    print()
    menu = input('''Select one of the following Options below:
r - Registering a user
a - Adding a task
va - View all tasks
vm - View my task
gr - Generate reports
ds - Display statistics
e - Exit
: ''').lower()

    if menu == 'r':
        reg_user(username_password)

    elif menu == 'a':
        add_task(tasks)

    elif menu == 'va':
        view_all(tasks)          

    elif menu == 'vm':
        view_mine(tasks, curr_user)
    
    elif menu == 'gr':
        '''If the user is an admin they can generate reports about number of users
            and tasks.'''
        gen_report(username_password, tasks) 
    
    elif menu == 'ds' and curr_user == 'admin': 
        '''If the user is an admin they can display statistics about number of users
            and tasks.'''
        num_users = len(username_password.keys())
        num_tasks = len(task_list)

        print("-----------------------------------")
        print(f"Number of users: \t\t {num_users}")
        print(f"Number of tasks: \t\t {num_tasks}")
        print("-----------------------------------")    

    elif menu == 'e':
        print('Goodbye!!!')
        exit()

    else:
        print("You have made a wrong choice, Please Try again")