import json
import time as tm
# Opening JSON file
# f = open('assembly_tasks.text', )


"""
    "status":"ready", status can be (ready or started, finished
    "can be done by":"R", can be R for robot or H for human oe HR for both
    "completed": "False", can be false or True
    "completed by": "None", can be Human or Robot
    "start time": "None",
    "completion time": "None" the real time when the task was finished in format HH:MM:SS
"""


def get_data_base():
    f = open('test_file.json')
    # returns JSON object as
    # a dictionary
    data_base = json.load(f)
    f.close()
    return data_base

def update_history(history):
	f = open("History.txt","w")
	f.write(history)
	f.close()

def update_data_base(data):
    """    with open('test_file.json', 'w') as outfile:
        json.dump(data, outfile)"""
    with open('test_file.json', 'w') as f:
        json.dump(data, f, indent=2)
    f.close()
    return


def start_task(task_number, data):
    data[task_number]["start time"] = tm.strftime("%H:%M:%S")
    data[task_number]["status"] = "started"
    return data


def task_complete(task_number, actuator, data):
    data[task_number]["status"] = "finished"
    data[task_number]["completed"] = "True"
    data[task_number]["completed by"] = actuator
    data[task_number]["completion time"] = tm.strftime("%H:%M:%S")
    return data


def current_incomplete_task(data):
    current_task = "no task"
    for task in data:
        if data[task]["status"] == "ready" and data[task]["completed"] == "False":
            current_task = task
            return current_task
    return current_task

