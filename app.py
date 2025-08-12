from datetime import datetime
import json

def currentDateTime():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

#Creating a new task

def createTask(tasks, taskName):
       
    new_task = {}
    new_task["status"] = "todo"
    new_task["createdAt"] = currentDateTime()
    new_task["updatedAt"] = None
    new_task["task"] = taskName[1:len(taskName)-1]
    new_task["description"] = input("Enter description: ")
    new_task["id"] = max(tasks.keys()) + 1 if tasks else 1
    tasks[new_task["id"]] = new_task
    print("Task added Succesfully")
    return tasks

#Updating a task
 
def updateTask(tasks, taskId, taskName):
    print("Updating....")
    print(taskId, taskName)
    task = tasks.get(taskId)
    task["task"] = taskName[1:len(taskName)-1]
    task["updatedAt"] = currentDateTime()
    if input("Press y to update description: ").lower() == 'y':
        task["description"] = input("Enter new Description: ")
    return tasks

#Deleting a task

def deleteTask(tasks, taskId):
    print("Deleting...")
    if taskId in tasks:
        del tasks[taskId]
    return tasks

#Updating Status

def updateStatus(tasks, status, taskId):
    print("Update...")
    print(status ,taskId)
    task = tasks.get(taskId)
    if status == "i":
        task["status"] = "in-progress"
    if status == "d":
        task["status"] = "done"
    task["updatedAt"] = currentDateTime()
    return tasks

#Listing Tasks

def listTask(tasks, list):
    if list == "all":
        for task in tasks.values():
            print("Task: ", task["task"], " Description: ", task["description"], "Status: ", task["status"])
    else: 
        print("Task ", list)
        for task in tasks.values():
            if task["status"] == list:
                print("Task: ", task["task"], " Description: ", task["description"])

try:
    with open('task.json', 'r') as file:
        file_data = json.load(file)
        tasks = {t["id"]: t for t in file_data}
except (FileNotFoundError, json.JSONDecodeError):
    file_data = []

inputTask = input().split()
if inputTask[0] == "task-cli":
    if inputTask[1] == "add":
        taskLine = ' '.join(inputTask[2:])
        if taskLine[0] == '"' and taskLine[-1] == '"': 
            createTask(tasks, taskLine)
        else:
            print("Error Task Name should be in quotes")
    elif inputTask[1] == "update":
        taskLine = ' '.join(inputTask[3:])
        if taskLine[0] == '"' and taskLine[-1] == '"': 
            updateTask(tasks, int(inputTask[2]), ' '.join(inputTask[3:]))
        else:
            print("Error Task Name should be in quotes")
        
    elif inputTask[1] == "delete":
        taskLine = ' '.join(inputTask[3:])
        if taskLine[0] == '"' and taskLine[-1] == '"': 
            deleteTask(tasks, int(inputTask[2]))
        else:
            print("Error Task Name should be in quotes")        
    elif inputTask[1][:4] == "mark":
        updateStatus(tasks, inputTask[1][5], int(inputTask[2]))
    elif inputTask[1] == "list":
        if len(inputTask) == 2:
            listTask(tasks, "all")
        else:
            listTask(tasks, inputTask[2])
    else: 
        print("Wrong Command Please try again!!")
else:
    print("Error: Command should start with task-cli....")
# Write the updated data back to the file
    with open('task.json', 'w') as file:
        json.dump(list(tasks.values()), file, indent=4)