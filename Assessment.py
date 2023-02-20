import csv
from datetime import datetime
import pytz

class Assessment:
    def __init__(self, title, subject, due_date,
                handout_date,
                estimated_hours,
                hours_per_week_to_be_completed):
        self.title = title
        self.subject = subject

        if not(isinstance(due_date, datetime) and isinstance(handout_date, datetime)):
            self.due_date = datetime.strptime(due_date.strip(), "%d/%m/%Y").date()
            self.handout_date = datetime.strptime(handout_date.strip(), "%d/%m/%Y").date()

        else:
            self.due_date = due_date.date()
            self.handout_date = handout_date.date()

        self.estimated_hours = int(estimated_hours)
        self.hours_per_week = \
            abs(round(self.estimated_hours / (int((self.due_date - self.handout_date).days) / 7), 2))
        
        if isinstance(hours_per_week_to_be_completed, int):
            self.hours_per_week_to_be_completed = hours_per_week_to_be_completed
        
        elif isinstance(hours_per_week_to_be_completed, bool):
            self.hours_per_week_to_be_completed = self.hours_per_week
        
        else:
            self.hours_per_week_to_be_completed = self.hours_per_week

        self.days_till_due   = (self.handout_date - datetime.now(pytz.timezone('Australia/Brisbane'))).days




def write_assessments_to_csv(assessments, file_path):
    with open(file_path, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['title', 'subject', 'due_date',
                         'handout_date', 'estimated_hours',
                         'hours_per_week', 'hours_per_week_to_be_completed'])
        for assessment in assessments:
            writer.writerow([assessment.title, assessment.subject,
                             assessment.due_date,
                             assessment.handout_date,
                             assessment.estimated_hours,
                             assessment.hours_per_week,
                             assessment.hours_per_week_to_be_completed])



def read_assessments_csv(file_path):
    assessments = []
    with open(file_path, 'r') as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            print(headers.index('title'))
            title = row[headers.index('title')]
            subject = row[headers.index('subject')]
            due_date = datetime.strptime(row[headers.index('due_date')], "%Y-%m-%d")
            handout_date = datetime.strptime(row[headers.index('handout_date')], "%Y-%m-%d")
            estimated_hours = row[headers.index('estimated_hours')]
            hours_per_week_to_be_completed = row[headers.index('hours_per_week_to_be_completed')]
            assessment = Assessment(title, subject, due_date, handout_date, estimated_hours, hours_per_week_to_be_completed)
            assessments.append(assessment)
    return assessments
