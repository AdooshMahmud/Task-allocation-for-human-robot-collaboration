import time
from tkinter import *
from tkinter import scrolledtext
import threading
import get_data
import messages
#*******************************************************
import rospy
from std_msgs.msg import String
rospy.init_node('GUI',anonymous=True)
pub = rospy.Publisher("/robot_start_task", String, queue_size=10)
r = rospy.Rate(2)
pub_pause_continue = rospy.Publisher("/pause_continue", String, queue_size=10)
pub_reset = rospy.Publisher("/reset_task", String, queue_size=10)
#******************************************************
pause_task_flag = False
reset_task_flag = False
task_options = []
engine_data_base = {}
UI_status = False
click_counter = 0
history = messages.message_task(messages.text_1)
current_task = "Task number"
robot_status = "Idle"
worker_status = "Idle"
on_going_task = False
finished_task=""

def lisining_to_robot(data):
	global finished_task
	finished_task = data.data

class GUI:

    def __init__(self):
        # Main Labels
        global task_options
        self.__main_window = Tk(className='HRC user interface')
        self.__main_window.geometry("1200x1000")

        self.__task_number = Label(self.__main_window, text="task number", font=("Times New Roman", 19), borderwidth=2,
                                   relief=GROOVE, height=5, width=21, background="white")
        self.__task_number.place(x=10, y=10)

        self.__task_status = Label(self.__main_window, text="task status", font=("Times New Roman", 19), borderwidth=2,
                                   relief=GROOVE, height=5, width=21, background="white")
        self.__task_status.place(x=304, y=10)

        self.__task_executor = Label(self.__main_window, text="task executor", font=("Times New Roman", 19),
                                     borderwidth=2, relief=GROOVE, height=5, width=44, background="white")
        self.__task_executor.place(x=10, y=170)

        self.__robot_status = Label(self.__main_window, text="robot status", font=("Times New Roman", 19),
                                    borderwidth=2, relief=GROOVE, height=5, width=21, background="white")
        self.__robot_status.place(x=10, y=330)

        self.__worker_status = Label(self.__main_window, text="worker status", font=("Times New Roman", 19),
                                     borderwidth=2, relief=GROOVE, height=5, width=21, background="white")
        self.__worker_status.place(x=304, y=330)
        # *************************************************************************************************
        # Buttons Worker and Robot
        self.__robot_do_task = Button(self.__main_window, text="Robot\nstart task", font=("Times New Roman", 18),
                                      borderwidth=2, relief=GROOVE, height=5, width=21, background="red",
                                      state='disabled')
        self.__robot_do_task.place(x=10, y=492)
        self.__robot_do_task.bind("<ButtonPress>", self.on_press_robot)
        self.__robot_do_task.bind("<ButtonRelease>", self.on_release_robot)

        self.__worker_do_task = Button(self.__main_window, text="Human\nstart task", font=("Times New Roman", 18),
                                       borderwidth=2, relief=GROOVE, height=5, width=21, background="red",
                                       state='disabled', command=self.worker_start_task)
        self.__worker_do_task.place(x=304, y=492)
        # ************************************************************************************************
        # Buttons Pause and Reset
        self.__pause = Button(self.__main_window, text="Pause", font=("Times New Roman", 18),
                              borderwidth=2, relief=GROOVE, height=4, width=21, background="red",
                              state='disabled', command=self.pause_task)
        self.__pause.place(x=10, y=650)

        self.__reset = Button(self.__main_window, text="Reset Task", font=("Times New Roman", 18),
                              borderwidth=2, relief=GROOVE, height=4, width=21, background="red",
                              state='disabled', command=self.reset_task)
        self.__reset.place(x=304, y=650)
        # ************************************************************************************************
        # Buttons Assembly and quit
        self.__start_assembly = Button(self.__main_window, text="Start", font=("Times New Roman", 18),
                                       borderwidth=2, relief=GROOVE, height=5, width=21, background="red",
                                       command=self.change_assembly_state)
        self.__start_assembly.place(x=1185, y=10)

        self.__Quit = Button(self.__main_window, text="Quit", font=("Times New Roman", 18),
                             borderwidth=2, relief=GROOVE, height=5, width=21, background="red",
                             command=self.quit)
        self.__Quit.place(x=1185, y=170)

        # ************************************************************************************************
        # ******************************************************
        self.__OPTIONS = task_options
        self.__selected_task = StringVar()
        self.__selected_task.set(self.__OPTIONS[0])  # default value
        self.__selector = OptionMenu(self.__main_window, self.__selected_task, *self.__OPTIONS)
        self.__selector.place(x=1394, y=330)  # x=1185, y=170

        self.__select_task = Label(self.__main_window, text="select task", font=("Times New Roman",),
                                   borderwidth=2, relief=GROOVE, width=18, background="white")
        self.__select_task.place(x=1185, y=335)

        self.__note = scrolledtext.ScrolledText(self.__main_window, wrap=WORD, width=35, height=15,
                                                font=("Times New Roman", 12), state='normal')
        self.__note.place(x=1185, y=370)

        self.submit_note = Button(self.__main_window, text="submit note", font=("Times New Roman", 18),
                                  borderwidth=2, relief=GROOVE, height=3, width=21, background="red",
                                  command=self.submit_task_note)
        self.submit_note.place(x=1185, y=665)
        # ******************************************************
        # ************************************************************************************************

        # History Label
        self.__History = scrolledtext.ScrolledText(self.__main_window, wrap=WORD, width=70, height=32,
                                                   font=("Times New Roman", 12), state='normal')
        # self.__History.configure(state='normal')
        self.__History.insert(INSERT, messages.message_task(messages.text_1))
        self.__History.configure(state='disabled')
        self.__History.place(x=600, y=170)

        self.__history_header = Label(self.__main_window, text="History", font=("Times New Roman", 19), borderwidth=2,
                                      relief=GROOVE, height=5, width=44, background="white")
        self.__history_header.place(x=600, y=10)

        self.__main_window.mainloop()
        # ***************************************************************************************
        # attributes

    def quit(self):
        global engine_data_base
        get_data.update_data_base(engine_data_base)
        self.__main_window.destroy()
        
    
    def submit_task_note(self):
        global engine_data_base
        engine_data_base[self.__selected_task.get()]["worker note"] = self.__note.get("1.0", END)
        get_data.update_data_base(engine_data_base)
        self.__note.delete('0.0', END)
        # ************************************************
        # update history by telling that the worker submitted notification for task()
        # ************************************************

    def update_history_label(self, message):
        global history, engine_data_base
        history = message + history
        self.__History.configure(state='normal')
        self.__History.delete('0.0', END)
        self.__History.insert(INSERT, history)
        self.__History.configure(state='disabled')
        return

    def change_assembly_state(self):
        """Activate or disable assembly UI"""
        global UI_status, history, engine_data_base, current_task, worker_status, robot_status, task_options
        # print_message = ""
        if not UI_status:
            print_message = messages.message_task(messages.text_2)
            self.update_history_label(print_message)
            self.__Quit.configure(state='disable')
            self.__start_assembly.configure(background="green", text="Stop")
            engine_data_base = get_data.get_data_base()
            # print(engine_data_base)
            current_task = get_data.current_incomplete_task(engine_data_base)
            UI_status = True
            if current_task == "no task":
                print_message = messages.message_task(messages.text_5)
                UI_status = False
                self.__Quit.configure(state='normal')
            else:
                print_message = messages.message_task(" " + current_task + messages.text_4)
                self.update_ui_labels(engine_data_base, current_task)

        else:
            get_data.update_data_base(engine_data_base)
            print_message = messages.message_task(messages.text_3)
            UI_status = False
            self.__Quit.configure(state='normal')
            self.__start_assembly.configure(background="red", text="Start")
            self.reset_ui_labels()
        self.update_history_label(print_message)
        get_data.update_history(history)
        self.change_buttons_status(worker_status, robot_status, UI_status, engine_data_base, current_task)

    def update_ui_labels(self, data, task_selected):
        global robot_status, worker_status
        self.__task_number.configure(text=task_selected)
        self.__task_status.configure(text=data[task_selected]["status"])
        self.__robot_status.configure(text=robot_status)
        self.__worker_status.configure(text=worker_status)
        if robot_status == "Busy":
            task_manager = " Robot is doing "
            self.__task_executor.configure(text=task_manager + task_selected)
        elif worker_status == "Busy":
            task_manager = " Worker is doing "
            self.__task_executor.configure(text=task_manager + task_selected)
        else:
            if data[task_selected]["can be done by"] == "Human" or data[task_selected]["can be done by"] == "Robot":
                self.__task_executor.configure(text=task_selected + " can be done by\n" +
                                               data[task_selected]["can be done by"] + " only")
            else:
                self.__task_executor.configure(text=task_selected + " can be done by\n" +
                                               data[task_selected]["can be done by"])

    def reset_ui_labels(self):
        global robot_status, worker_status
        self.__task_number.configure(text="task number")
        self.__task_status.configure(text="task status")
        self.__task_executor.configure(text="task executor")
        self.__robot_status.configure(text="robot status")
        self.__worker_status.configure(text="worker status")

    def change_buttons_status(self, w_status, r_status, ui_status, data, task):
        self.__start_assembly.configure(state='normal')
        if task in data:
        	if (data[task]["can be done by"] == "Human" or data[task]["can be done by"] == "Human or Robot") \
        	and w_status == "Idle" and ui_status and data[task]["status"] == "ready":
        		self.__worker_do_task.configure(state='normal', text='Human', background='red')
        	else:
        		self.__worker_do_task.configure(state='disable')
        	if (data[task]["can be done by"] == "Robot" or data[task]["can be done by"] == "Human or Robot") \
        	and r_status == "Idle" and ui_status and data[task]["status"] == "ready":
        		self.__robot_do_task.configure(state='normal', text='Robot', background='red')
        	else:
        		self.__robot_do_task.configure(state='disable')
        else:
        	self.__worker_do_task.configure(state='disable')
        	self.__robot_do_task.configure(state='disable')
        	self.__start_assembly.configure(state='disable')
        	self.__start_assembly.configure(background="red")
        	self.__Quit.configure(state='normal')
        	self.__Quit.configure(background="green")
        	

    def on_press_robot(self, event):
        global current_task, engine_data_base, on_going_task, history, worker_status, robot_status, UI_status
        if not on_going_task:
            on_going_task = True
            robot_status = "Busy"
            engine_data_base[current_task]["start time"] = messages.current_time()
            engine_data_base[current_task]["status"] = "started"
            self.__robot_do_task.configure(background="green", text="Robot is working", state='disable')
            print_message = messages.message_task(messages.text_7 + current_task + messages.text_11)
            self.update_history_label(print_message)
            get_data.update_history(history)
            self.update_ui_labels(engine_data_base, current_task)
            self.__Quit.configure(state='disable')
            self.__worker_do_task.configure(state='disable')
            self.__start_assembly.configure(state='disable')
            self.__pause.configure(state='normal')
            self.__reset.configure(state='normal')

    def on_release_robot(self, event):
        global current_task
        pub.publish(current_task)
        threading.Thread(target=self.pause_function_thread).start()
        threading.Thread(target=self.reset_function_thread).start()
        threading.Thread(target=self.robot_reply_thread).start()
        #***********************************************
        

    def robot_reply_thread(self):
    	global finished_task, current_task, engine_data_base, on_going_task, history, worker_status, robot_status, UI_status
    	sub = rospy.Subscriber ('/Robot_finnished', String, lisining_to_robot)
    	
    	while current_task != finished_task:
    		time.sleep(1)
    	print(finished_task, "finnished")
    	on_going_task = False
    	robot_status = "Idle"
    	self.__pause.configure(state="disable")
    	self.__reset.configure(state="disable")
    	engine_data_base[current_task]["status"] = "finished"
    	engine_data_base[current_task]["completed"] = "True"
    	engine_data_base[current_task]["completion time"] = messages.current_time()
    	engine_data_base[current_task]["completed by"] = "Robot"
    	get_data.update_data_base(engine_data_base)
    	self.__robot_do_task.configure(background="red", text="Robot\nstart task")
    	self.__start_assembly.configure(state='normal')
    	print_message = messages.message_task((" " + current_task + messages.text_9))
    	self.update_history_label(print_message)
    	get_data.update_history(history)
    	current_task = get_data.current_incomplete_task(engine_data_base)
    	if current_task == "no task":
    		print_message = " Congratulations engine is assembled \n"
    		self.reset_ui_labels()
    		self.update_history_label(print_message)
    		get_data.update_history(history)
    	else:
    		print_message = messages.message_task((" " + current_task + messages.text_4))
    		self.update_history_label(print_message)
    		get_data.update_history(history)
    		self.update_ui_labels(engine_data_base, current_task)
    	self.change_buttons_status(worker_status, robot_status, UI_status, engine_data_base, current_task)
    	return
    	
    
    def reset_function_thread(self):
        global reset_task_flag, robot_status
        counter = 50
        while counter > 0:
            counter -= 1
            if reset_task_flag:
                self.__pause.configure(text='Pause', background="red", state='disable')
                pub_reset.publish("reset")
                reset_task_flag = False
                return
            time.sleep(0.1)
        self.__reset.configure(state='disable')

    def pause_function_thread(self):
        global pause_task_flag, reset_task_flag
        while True:
            if pause_task_flag and robot_status == "Busy":
                self.__pause.configure(text='continue', background="green")
                return
            elif reset_task_flag:
                return
            time.sleep(0.1)

    def pause_task(self):
        global pause_task_flag
        if not pause_task_flag:
            self.__pause.configure(text='continue', background="green")
            pub_pause_continue.publish("pause")
            pause_task_flag = True
            print_message = messages.message_task(current_task + messages.text_13)
            self.__task_status.configure(text="temporary stop")
            self.update_history_label(print_message)
        else:
            pause_task_flag = False
            self.__pause.configure(text='Pause', background="red")
            pub_pause_continue.publish("continue")
            self.__task_status.configure(text="started")
            print_message = messages.message_task(current_task + messages.text_14)
            self.update_history_label(print_message)

    def reset_task(self):
        global reset_task_flag, pause_task_flag, reset_task_flag, current_task, engine_data_base,\
            on_going_task, history, worker_status, robot_status, UI_status
        reset_task_flag = True
        
        time.sleep(0.1)
        pause_task_flag = False
        reset_task_flag = False
        on_going_task = False
        engine_data_base[current_task]["status"] = "ready"
        engine_data_base[current_task]["start time"] = "None"
        print_message = messages.message_task(messages.text_12 + current_task)
        self.update_history_label(print_message)
        get_data.update_history(history)
        robot_status = "Idle"
        worker_status = "Idle"
        self.update_ui_labels(engine_data_base, current_task)
        print_message = messages.message_task(" " + current_task + messages.text_4)
        self.update_history_label(print_message)
        get_data.update_history(history)
        self.__pause.configure(text='Pause', background="red", state='disable')
        self.__reset.configure(state='disable')
        self.change_buttons_status(worker_status, robot_status, UI_status, engine_data_base, current_task)

    def worker_start_task(self):
        global current_task, engine_data_base, on_going_task, history, worker_status, robot_status, UI_status
        if not on_going_task:
            on_going_task = True
            ###################################################################################################
            self.__pause.configure(state="disable")
            self.__reset.configure(state="normal")
            #self.reset_task()
            ###################################################################################################
            worker_status = "Busy"
            engine_data_base[current_task]["start time"] = messages.current_time()
            engine_data_base[current_task]["status"] = "started"
            self.__worker_do_task.configure(background="green", text="Task Finished")
            print_message = messages.message_task(messages.text_6 + current_task + messages.text_8)
            self.update_history_label(print_message)
            get_data.update_history(history)
            self.update_ui_labels(engine_data_base, current_task)
            self.__Quit.configure(state='disable')
            self.__robot_do_task.configure(state='disable')
            self.__start_assembly.configure(state='disable')

        else:
            on_going_task = False
            worker_status = "Idle"
            self.__pause.configure(state="disable")
            self.__reset.configure(state="disable")
            engine_data_base[current_task]["status"] = "finished"
            engine_data_base[current_task]["completed"] = "True"
            engine_data_base[current_task]["completion time"] = messages.current_time()
            engine_data_base[current_task]["completed by"] = "Human"
            get_data.update_data_base(engine_data_base)
            self.__worker_do_task.configure(background="red", text="Human\nstart task")
            self.__start_assembly.configure(state='normal')
            print_message = messages.message_task((" " + current_task + messages.text_9))
            self.update_history_label(print_message)
            get_data.update_history(history)
            current_task = get_data.current_incomplete_task(engine_data_base)
            if current_task == "no task":
                print_message = " Congratulations engine is assembled \n"
                self.reset_ui_labels()
                self.update_history_label(print_message)
                get_data.update_history(history)
            else:
                print_message = messages.message_task((" " + current_task + messages.text_4))
                self.update_history_label(print_message)
                get_data.update_history(history)
                self.update_ui_labels(engine_data_base, current_task)
            self.change_buttons_status(worker_status, robot_status, UI_status, engine_data_base, current_task)
        return


def main():
    global engine_data_base
    engine_data_base = get_data.get_data_base()
    for task in engine_data_base:
        task_options.append(task)
    GUI()


if __name__ == "__main__":
	main()
