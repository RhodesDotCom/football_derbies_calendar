import os
import csv


def read_fixtures():
    fixtures = []
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'fixtures')
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_path = os.path.join(folder_path, filename)

            with open(csv_path, 'r') as csv_file:
                reader = csv.reader(csv_file, delimiter='\t')
                fixtures.extend(list(reader))
    return fixtures


def find_derbies(derbies, fixtures):
    derby_found = []
    for derby in derbies:
        for fixture in fixtures:
            if derby[0] in fixture and derby[1] in fixture:
                derby_found.append(fixture)
    return derby_found