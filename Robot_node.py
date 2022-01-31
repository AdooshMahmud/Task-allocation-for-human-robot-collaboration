#!/usr/bin/env python3
import rospy
from std_msgs.msg import String
import time
new_task = "task"
pause_command = "continue"
reset_command = "continue"
def recived_task(data):
	global new_task
	new_task = data.data
def recieve_pause(data):
	global pause_command
	pause_command = data.data

def recieve_reset(data):
	global reset_command
	reset_command = data.data

finished_tasks = []
tasks = ["Task 1", "Task 2", "Task 3", "Task 4"]
start = True
rospy.init_node('Robot', anonymous=True)
pub = rospy.Publisher("/Robot_finnished", String, queue_size=10)
sub = rospy.Subscriber ('/robot_start_task', String, recived_task)
r = rospy.Rate(1)
sub_pause_continue = rospy.Subscriber ('/pause_continue', String, recieve_pause)

sub_reset = rospy.Subscriber ('/reset_task', String, recieve_reset)

while start:
	counter = 5
	time.sleep(1)
	if new_task in tasks and new_task not in finished_tasks:
		print("robot start the task")
		while counter > 0:
			counter -= 1
			time.sleep(1)
			
			while pause_command == "pause":
				time.sleep(0.2)
			if reset_command == "reset":
				counter = 0
		print(reset_command)			
		if reset_command != "reset":
			pub.publish(new_task)
			finished_tasks.append(new_task)
			print("task finished robot is waiting for new task")
		reset_command = "continue"
		new_task = "task"
		
