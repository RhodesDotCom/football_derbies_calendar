fixtures = {}
fixtures['teams'] = '  Oxford United vs. Swindon Town'
match = [' v ', ' vs ', ' vs. ']

for fixture in fixtures['teams']:
    print(fixture)
    for chr in match:
        if chr in fixture:
            teams = fixture.split(chr)
            print(teams)