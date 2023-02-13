import Classes
import datetime
import time
import sched
import schedule
import requests
import pprintpp
import threading
import telebot

from pytz import timezone
from Lists import process_command
# from Server import keep_alive
from ProjectEuler import get_problem

# Get the current day's classes from the classes module
todays_classes = Classes.get_todays_classes()

# Set up the scheduler
s = sched.scheduler(time.time, time.sleep)

# Set up the bot
bot = telebot.TeleBot('5926046732:AAG0s6FfvbZxmiqoh2o071AqhSxCmJ2FaAw')
chat_id = '5214053901'

# Dictionary of scheduled messages
# Key is the scheduled time in the format 'HH:MM AM/PM'
# Value is the message to be sent
scheduled_messages = {
    "06:00": "Wake up and have breakfast",
    "06:30": "Review your to-do list for the week and plan out your tasks for the day",
    "07:00": ("Work on programming tasks", lambda: (
        send_message(process_command('programming?'))
    )),

    "8:00": "Get ready for school",
    "13:48": "helllo",
    "15:30": "Return home and take a short break",
    "16:28": (f"Review notes for {todays_classes['1']}", lambda: (
        send_message(process_command('homework?'))
    )),

    "16:25": "Take a 5-minute break",
    "16:30": f"Review notes for {todays_classes['2']}",
    "16:55": "Take a 5-minute break",
    "17:00": f"Review notes for {todays_classes['3']}",
    "17:25": "Take a 5-minute break",
    "17:30": f"Review notes for {todays_classes['4']}",
    "17:55": "Take a 5-minute break",
    "18:00": f"Review notes for {todays_classes['5']}",
    "18:25": "Take a 5-minute break",
    "18:30": "Work on assessment tasks",
    "18:55": "Take a 5-minute break",
    "19:00": "Work on assessment tasks",
    "19:16": "Take a break for dinner",
    "20:44": ("Programming / Free time", lambda: (
        send_message(process_command('programming?'))
    )),

    "21:30": "Get ready for bed and wind down for sleep"
}

# Initialize the scheduler
s = sched.scheduler(time.time, time.sleep)

tz = timezone('Australia/Brisbane')
day_tick_time = "1:0"

def run_scheduler():
    global s
    s.run()
    print('scheduler ran')

def event_loop():
    global current_time, tz, day_tick_time
    while True:
        schedule.run_pending()
        current_time = convert_date(str(datetime.datetime.now(tz).hour) + ':' + str(datetime.datetime.now(tz).minute))
        if str(current_time.hour) == str(day_tick_time.split(':')[0]) and str(current_time.minute == day_tick_time.split(':')[1]):
            day_tick()

        time.sleep(30)


# Initialize the server
# keep_alive()

# Function to send the scheduled message
def send_message(message):
    global bot
    print(message)
    bot.send_message(chat_id=chat_id, text=message)

def scheduled_event(event):
    if not isinstance(event, tuple):
        send_message(event)
    else:
        send_message(event[0])
        event[1]()

def convert_date(time: str):
    today = datetime.datetime.now()
    return datetime.datetime(today.year, today.month, today.day, int(time.split(':')[0]), int(time.split(':')[1]))

def day_tick():
    print('new day?')
    if datetime.datetime.today().weekday() in range(0, 5):
        # Loop through the scheduled messages dictionary
        for time, message in scheduled_messages.items():
            # Schedule the message for each task at the specified time
            today = datetime.datetime.now()
            if (convert_date(time) > today):
                s.enterabs(convert_date(time).timestamp(), 1, scheduled_event, argument=(message,))

    else: print('weekend')


# schedule.every().day.at("18:18").do(day_tick)

# s.enterabs(convert_date('12:30').timestamp(), 1, day_tick)


t = threading.Thread(target=run_scheduler)
t.start()

# t2 = threading.Thread(target=event_loop)
# t2.start()
send_message('Online')

@bot.message_handler()
def on_list_interaction(message):
    print('Message Recieved')
    message.text = message.text.lower()
    try:
        result = process_command(message.text)
        if (result != None):
            send_message(result)
        pass
    except Exception as e:
        print('Not interacting with list', e)
        if (message.text.startswith('project euler:')):
            try:
                problem = get_problem(int(message.text.split(':')[1]))
                send_message(problem)
            except ValueError:
                send_message('Invalid Number')
        return

try:
    bot.polling()
except requests.exceptions.ReadTimeout:
    print('Wait...')
    time.ttime.sleep(100)
    bot.polling()



