import get_data
import time
data = get_data.get_data_base()
print(data["Task 1"])
time.sleep(5)
get_data.start_task("Task 1", data)
print(data["Task 1"])

time.sleep(5)
get_data.task_complete("Task 1", "Human", data)
print(data["Task 1"])

