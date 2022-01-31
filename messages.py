import time as tm


def current_time():
    return tm.strftime("%H:%M:%S")


def message_task(text):
    message = "[" + current_time() + "]" + text + "\n"
    return message


text_1 = " Welcome to the engine Assembly please \n"+\
         50*" "+"Press Start to activate UI\n"+50*" "+"Press Quit to close UI"
text_2 = " UI activated you can start assembly proses"
text_3 = " UI Disabled \n\
                              Press Start to activate UI)\n\
                              Press Quit to close UI"
text_4 = " is ready to go"
text_5 = " All tasks are completed"
text_6 = " Worker started "
text_7 = " Robot started "
text_8 = "\n" \
         + " "*18+"please press task finished button\n" \
         + " "*18+"when task is completed"
text_9 = " is done"
text_10 = "\n\
                              Press Start to activate UI)\n\
                              Press Quit to close UI"
text_11 = "\n" \
         + " "*18+"please wait while robot is working"
text_12 = " Worker Reset "
text_13 = " is Paused"
text_14 = " is continued"

"""text_6 = "Task can be done by\n" \
         "  Human or Robot"
text_7 = "Task can be done by\n" \
         "      Human"
text_8 = "Task can be done by\n" \
         "      Robot"
         """
