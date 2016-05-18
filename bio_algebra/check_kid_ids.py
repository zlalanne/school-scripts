#!/usr/bin/env python

import sys
import xlrd
import xlwt
from xlutils.copy import copy

_, algebra_excel, bio_excel, geo_txt, final_algebra_excel = sys.argv

COLS_WITH_ID = [0, 4, 10]
SWITCH_IND = 32

breakline = '%' * 80

algebra_kids = {'morning': [], 'afternoon': [], 'total': []}
final_algebra_kids = {'morning': [], 'afternoon': [], 'total': []}
bio_kids = {'morning': [], 'afternoon': [], 'total': []}
geo_kids = []

with open(geo_txt, 'r') as f:
    for line in f.readlines():
        geo_kids.append(int(line))

print(breakline)
print('Number of geo kids: {}'.format(len(geo_kids)))


def parse_file(subject, filename):
    print(breakline)
    print('Starting to parse: {}'.format(filename))
    workbook = xlrd.open_workbook(filename)
    sheet_names = workbook.sheet_names()

    for sheet_name in sheet_names:
        sheet = workbook.sheet_by_name(sheet_name)

        for row in range(0, sheet.nrows):
            for col in COLS_WITH_ID:
                cell = sheet.cell(row, col)
                cell = '{}'.format(cell)
                cell = cell.strip()
                cell = cell.split(':')[1]
                cell = cell.split('.')[0]

                cell = str(cell).encode('ascii')
                cell = cell.replace("'", '')
                cell = cell.replace("u", '')

                if subject == 'final_algebra':
                    print(cell)

                # Skip this cell if it isn't an ID
                if not cell.isdigit():
                    continue

                student_id = int(cell)

                if subject == 'final_algebra':
                    if row < SWITCH_IND:
                        final_algebra_kids['afternoon'].append(student_id)
                    else:
                        final_algebra_kids['morning'].append(student_id)
                    if student_id not in final_algebra_kids['total']:
                        final_algebra_kids['total'].append(student_id)
                    else:
                        print('ERROR: {} already appeared in Algebra'.format(
                            student_id))
                if subject == 'algebra':
                    if row < SWITCH_IND:
                        algebra_kids['afternoon'].append(student_id)
                    else:
                        algebra_kids['morning'].append(student_id)
                    if student_id not in algebra_kids['total']:
                        algebra_kids['total'].append(student_id)
                    else:
                        print('ERROR: {} already appeared in Algebra'.format(
                            student_id))
                if subject == 'bio':
                    if row < SWITCH_IND:
                        bio_kids['morning'].append(student_id)
                    else:
                        bio_kids['afternoon'].append(student_id)
                    if student_id not in bio_kids['total']:
                        bio_kids['total'].append(student_id)
                    else:
                        print('ERROR: {} already appeared in Biology'.format(
                            student_id))


parse_file('algebra', algebra_excel)
parse_file('bio', bio_excel)
parse_file('final_algebra', final_algebra_excel)

print(breakline)

morning_kids = [kid for kid in algebra_kids['morning'] if kid in bio_kids['morning']]
print('Kids in multiple morning sections:')
print(morning_kids)
print(breakline)
afternoon_kids = [kid for kid in algebra_kids['afternoon'] if kid in bio_kids['afternoon']]
print('Kids in multiple afternoon sections:')
print(afternoon_kids)
print(breakline)

print('Kids in Algebra not in Biology:')
algebra_only_kids = [kid for kid in algebra_kids['total'] if kid not in bio_kids['total']]
for kid in algebra_only_kids:
    print(kid)
print(breakline)

print('Kids in Biology not in Algebra:')
bio_kids_only = [kid for kid in bio_kids['total'] if kid not in algebra_kids['total']]
for kid in bio_kids_only:
    print(kid)
print(breakline)

print('Starting to write new cells')

## Now highlighting cells
workbook = xlrd.open_workbook(bio_excel)
sheet_names = workbook.sheet_names()
new_workbook = copy(workbook)

st1 = xlwt.easyxf('pattern: pattern solid;')
st1.pattern.pattern_back_colour = 53

st2 = xlwt.easyxf('pattern: pattern solid;')
st2.pattern.pattern_back_colour = 2

for i, sheet_name in enumerate(sheet_names):
    sheet = workbook.sheet_by_name(sheet_name)
    for row in range(0, sheet.nrows):
        for col in COLS_WITH_ID:
            cell = sheet.cell(row, col)
            cell_data = '{}'.format(cell)
            cell_data = cell_data.strip()
            cell_data = cell_data.split(':')[1]
            cell_data = cell_data.split('.')[0]

            # Skip this cell if it isn't an ID
            if not cell_data.isdigit():
                continue

            student_id = int(cell_data)
            #print(student_id)
            if student_id in bio_kids_only:
                new_workbook.get_sheet(i).write(row, col, cell_data, st1)

new_workbook.save('output.xls')

## Now highlighting cells
workbook = xlrd.open_workbook(algebra_excel)
sheet_names = workbook.sheet_names()
new_workbook = copy(workbook)

st1 = xlwt.easyxf('pattern: pattern solid;')
st1.pattern.pattern_back_colour = 53

st2 = xlwt.easyxf('pattern: pattern solid;')
st2.pattern.pattern_fore_colour = 12

for i, sheet_name in enumerate(sheet_names):
    sheet = workbook.sheet_by_name(sheet_name)
    for row in range(0, sheet.nrows):
        for col in COLS_WITH_ID:
            cell = sheet.cell(row, col)
            cell_data = '{}'.format(cell)
            cell_data = cell_data.strip()
            cell_data = cell_data.split(':')[1]
            cell_data = cell_data.split('.')[0]

            # Skip this cell if it isn't an ID
            if not cell_data.isdigit():
                continue

            student_id = int(cell_data)
            #print(student_id)
            if student_id in geo_kids:
                new_workbook.get_sheet(i).write(row, col, cell_data, st2)
            if student_id in algebra_only_kids:
                new_workbook.get_sheet(i).write(row, col, cell_data, st1)
            if student_id in algebra_only_kids and student_id in geo_kids:
                print('ERROR: Kid in weird scenario: {}'.format(student_id))

new_workbook.save('new_algebra.xls')

## Were all kids added?
missed_kids = [kid for kid in algebra_only_kids if kid not in final_algebra_kids['total']]
print(breakline)
print('Kids that need to be added')
print(missed_kids)
print(len(missed_kids))

