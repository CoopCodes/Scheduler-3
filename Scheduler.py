import Classes
import Assessment
import datetime
import time as ttime
import sched
import random
import pytz
import csv
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
tz = pytz.timezone('Australia/Brisbane')

# Set up the scheduler
s = sched.scheduler(ttime.time, ttime.sleep)

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


    "15:30": "Return home and take a short break",
    "15:45": "Take a bloody sleep if you feel like it",
    "16:30": "Start Assessment Work",

    # Assessment to be worked on determined on day
    # Start homework (Determined on day)
    str(datetime.datetime.now(tz).hour) + ":" + str(datetime.datetime.now(tz).minute): "test",

    "19:00": ("Chores 💀", lambda: (
        send_message(process_command('chores?'))
    )),

    "19:30": "Take a break for dinner",
    "20:00": ("Programming / Free time", lambda: (
        send_message(process_command('programming?'))
    )),

    "21:30": "Get ready for bed and wind down for sleep"
}

scheduled_messages_status = [ False for _ in scheduled_messages.items() ]

assessments_path = "Lists/assessments.csv"
assessments = Assessment.read_assessments_csv(assessments_path);

assessment_queue = [
    assessment for assessment in assessments
]
todays_assessment = random.choice(assessment_queue)

# print("{:02d}:{:02d}".format(datetime.datetime.now(tz).hour, datetime.datetime.now(tz).minute + 1))

tz = timezone('Australia/Brisbane')

# Initialize the scheduler
s = sched.scheduler(datetime.datetime.now(tz), ttime.sleep)


day_tick_time = "1:0"

def run_scheduler():
    global s
    s.run()
    day_tick()

def event_loop():
    global current_time, tz, day_tick_time
    while True:
        current_time = convert_date("{:02d}:{:02d}".format(datetime.datetime.now(tz).hour, datetime.datetime.now(tz).minute))
        current_time_f = "{:02d}:{:02d}".format(datetime.datetime.now(tz).hour, datetime.datetime.now(tz).minute)
        if str(current_time.hour) == str(day_tick_time.split(':')[0]) and str(current_time.minute == day_tick_time.split(':')[1]):
            day_tick()

        for i, (time, message) in enumerate(scheduled_messages.items()):
            if current_time_f == time and scheduled_messages_status[i] == False:
                scheduled_event(message)
                scheduled_messages_status[i] = True

        ttime.sleep(10)


# Function to send the scheduled message
def send_message(message, html=False):
    global bot
    try:
        print(message)
        if html == False: 
            bot.send_message(chat_id=chat_id, text=message)
        else:
            bot.send_message(chat_id=chat_id, text=message, parse_mode='HTML')

    except telebot.apihelper.ApiTelegramException:
        print('Empty message')
        bot.send_message(chat_id=chat_id, text="Empty message")

def scheduled_event(event):
    if not isinstance(event, tuple):
        send_message(event)
    else:
        send_message(event[0])
        event[1]()

def convert_date(time: str):
    today = datetime.datetime.now(tz)
    return datetime.datetime(today.year, today.month, today.day, int(time.split(':')[0]), int(time.split(':')[1]))

def day_tick():
    global s, assessments, assessment_queue
    if datetime.datetime.today().weekday() in range(0, 7): # Check if the day is a weekday
        schedule()

        todays_assessment = random.choice(assessment_queue)

        for status in scheduled_messages_status:
            status = False

    else: print('weekend')

    assessments = Assessment.read_assessments_csv(assessments_path);

def schedule(random=False):
    global todays_assessment, s, assessments, assessment_queue
    schoolwork_start_time = "16:30"

    if random == True:
        todays_assessment = random.choice(assessment_queue)

    assessment = todays_assessment


    if assessment.hours_per_week > 1.5:
        assessment_queue[assessment_queue.index(assessment)].hours_per_week_completed -= 1.5
        scheduled_messages[schoolwork_start_time] = f'Work on {assessment.title} for 1.5 hours'

        i = convert_date(schoolwork_start_time)
        j = datetime.timedelta(hours=1, minutes=30)
        # j = datetime.timedelta(hours=int(str(assessment.hours_per_week_completed).split('.')[0]), minutes=int(str(assessment.hours_per_week_completed).split('.')[1]))
        homework_start_time = (i + j).strftime("%H:%M")

        scheduled_messages[homework_start_time] = \
                        ("Time for homework", lambda: (
                                send_message(process_command('homework?'))
                        ))


    else: assessment_queue.remove(assessment) 

    scheduled_messages_status = [ False for _ in scheduled_messages.items() ]



t = threading.Thread(target=run_scheduler)
t.start()

t2 = threading.Thread(target=event_loop)
t2.start()

send_message('Online')

@bot.message_handler()
def on_list_interaction(message):
    global todays_assessment
    print('Message Recieved')

    message.text = message.text[0].lower() + message.text[1::]
    try:
        result = process_command(message.text)
        if (result != None):
            send_message(result)
        pass
    except Exception as e:
        global assessments, assessments_path
        print('Not interacting with list')
        if (message.text.startswith('project euler:')):
            try:
                problem = get_problem(int(message.text.split(':')[1]))
                send_message(problem)
            except ValueError:
                send_message('Invalid Number')

        elif (message.text.startswith('assessment:')):
            assessments = Assessment.read_assessments_csv(assessments_path)

            assessment = Assessment.Assessment(
                    message.text.split(',')[0].split(':')[1],
                    message.text.split(',')[1],
                    message.text.split(',')[2],
                    message.text.split(',')[3],
                    message.text.split(',')[4]
            ); assessments.append(assessment)

            Assessment.write_assessments_to_csv(assessments, assessments_path)
            assessments = Assessment.read_assessments_csv(assessments_path)
            send_message(f'Assessment Saved \nhours per week: {assessment.hours_per_week} hours')

            if len(assessments) < 2:
                schedule(True)


        elif (message.text.startswith('assessment?')):
            send_message("Format: title, subject, due_date, assessment_handout_date, estimated_hours")

        elif (message.text.startswith('assessments?')):
            assessments = Assessment.read_assessments_csv(assessments_path)
            assessments_str = "------------------------------------------\n"
            if len(assessments) < 1:
                print('lists not initialized')
                return

            for assessment in assessments:
                assessments_str += f'<b>{assessment.title}</b>:\n     Subject: {assessment.subject}\n     Due Date: {assessment.due_date}\n     Date Handed In: {assessment.assessment_handout_date}\n     Estimated Hours: {assessment.estimated_hours}\n     Hours Per Week: {assessment.hours_per_week}\n------------------------------------------\n'

            send_message(assessments_str, True)



        return

try:
    bot.polling()
except requests.exceptions.ReadTimeout:
    print('Wait...')
    time.ttime.sleep(100)
    bot.polling()



