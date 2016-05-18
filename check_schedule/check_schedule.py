import csv
import re
from os.path import join
from os.path import dirname
from os.path import abspath

NAME_COL = 0
ROOM_COL = 1
PERIOD_START_COL = 2

classes = set()

def print_break():
    print('-------------------------------------------------------')

schedule = join(dirname(abspath(__file__)), 'schedule.csv')
print('Opening: {} for review'.format(schedule))

with open(schedule, 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        for i, col in enumerate(row):
            if i >= PERIOD_START_COL:
                cls = re.sub(r'\s+', ' ', col).strip()
                classes.add(cls)

float_rows = []
classrooms = {}
with open(schedule, 'r') as f:
    reader = csv.reader(f, delimiter=',', quotechar='"')
    for row in reader:
        classroom = row[ROOM_COL]
        if classroom.upper().startswith('FLOAT'):
            float_rows.append(row)
        else:
            classrooms[row[ROOM_COL].strip()] = row

print_break()
print('Looking for teachers that float classrooms...')
for row in float_rows:
    teacher_name = row[NAME_COL].split(',')[0].strip()
    print_break()
    print('Teacher {} floats classrooms. Making sure there are no conflicts'.format(teacher_name))
    for i, period in enumerate(row[PERIOD_START_COL:-1]):
        match = re.match(r'.*(?P<classroom>[C|G]\d+)', period)
        if match:
            assigned_room = match.group('classroom')
            teacher_in_room = classrooms[assigned_room]
            room_teacher_name = teacher_in_room[NAME_COL].split(',')[0].strip()
            print('{} teaches in {} during {} period. That is {} classroom. They have {} during that period.'.format(teacher_name, assigned_room, i + 1, room_teacher_name, teacher_in_room[PERIOD_START_COL + i].strip()))
        elif i != 3:
            print('Could not find room for {}'.format(period))


