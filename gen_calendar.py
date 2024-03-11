import calendar
import csv


def generate_calendar(year_start, month_start, year_end, month_end):
    months = {}
    
    current_month, current_year = month_start, year_start
    while (current_year, current_month) <= (year_end, month_end):
        month_data = {}
        cal = calendar.monthcalendar(current_year, current_month)
        for week in cal:
            for day in week:
                if day != 0:
                    month_data[day] = {"date": f"{current_year}-{current_month:02d}-{day:02d}", "note": []}
        months[calendar.month_name[current_month]] = month_data

        # Move to next month/year
        if current_month == 12:
            current_month = 1
            current_year += 1
        else:
            current_month += 1

    return months


def add_to_calendar(calendar, fixtures):
    for month, days in calendar.items():
        for day, data in days.items():
            for fixture in fixtures:
                if fixture[1] == data['date']:
                    fixture_str = f'{fixture[2]} vs. {fixture[3]}'
                    data['note'].append(fixture_str)
    return calendar


def export_to_csv(data, filename):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Date", "Fixture"])
        for month_name, month_data in data.items():
            for day, day_data in month_data.items():
                writer.writerow([day_data['date'], day_data["note"] if day_data["note"] else ''])





