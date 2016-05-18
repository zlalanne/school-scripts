import sys
import csv

_, filename = sys.argv

bio_students = []
algebra_students = []

total_students = {}

with open(filename, 'rb') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        if row['EOC'].startswith('Bio'):
            bio_students.append(row['ID'])
        elif row['EOC'].startswith('Alge'):
            algebra_students.append(row['ID'])

        total_students[row['ID']] = '{} {}'.format(row['FIRST NAME'], row['LAST NAME'])


in_algebra_only = [student for student in algebra_students if student not in bio_students]
in_biology_only = [student for student in bio_students if student not in algebra_students]

print('%' * 80)
print("Students only in Algebra, not Biology:")
for student in in_algebra_only:
    print('{}: {}'.format(student, total_students[student]))

print('%' * 80)

print("Students only in Biology, not Algebra:")
for student in in_biology_only:
    print('{}: {}'.format(student, total_students[student]))
