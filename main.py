from derbies import get_derbies
from fixtures import read_fixtures, find_derbies
from gen_calendar import generate_calendar, add_to_calendar, export_to_csv

from pprint import pprint as pp


derbies = get_derbies()
fixtures = read_fixtures()
derbies_found = find_derbies(derbies, fixtures)
calendar = generate_calendar(2023, 8, 2024, 6)
calendar = add_to_calendar(calendar, derbies_found)
export_to_csv(calendar, "derbies_2023_2024.csv")