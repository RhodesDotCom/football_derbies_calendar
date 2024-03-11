from gettext import find
import pandas as pd
import os
import sys
from pprint import pprint as pp
from bs4 import BeautifulSoup
import requests
import re
import fuzzywuzzy


def main():

    fixture_list = {file.split('.')[0]: pd.read_csv(f"fixtures/{file}") for file in os.listdir("fixtures")}
    
    derbies = scrape_url('united_kingdom')
    derbies, errors = clean_data(derbies)

    fixtures = read_fixture_list('premier_league')
    rivals, errors = split_fixtures(derbies, errors)

    # if errors:
    #     pp(f"Error inserting to df: {errors}")

    # pp(rivals)

def get_url(country):
    links = {
    'united_kingdom': 'https://en.wikipedia.org/wiki/List_of_association_football_rivalries_in_the_United_Kingdom',
    'germany': '',
    'spain': 'https://en.wikipedia.org/wiki/Spanish_football_rivalries',
    'italy': '',
    'france': ''
    }

    try:
        return links[country]
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


def search_uls(ul, text=[]):
    if ul.find_all('li'):
        for li in ul.find_all('li'):
            text = search_lis(li, text)
            return text
    else:
        text.append(ul.get_text())
        return text


def search_lis(li, text=[]):
    if li.find_all('ul'):
        for ul in li.find_all('ul'):
            text = search_uls(ul, text)
            return text
    else:
        text.append(li.get_text())
        return text


def scrape_url(country):

    url = get_url(country)
    try:
        page = requests.get(url)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        data = BeautifulSoup(page.content, "lxml")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    fixtures = []
    for body in data.find_all('body'):
            for ul in body.find_all('ul'):
                for li in ul.find_all('li'):
                    fixtures = search_lis(li, fixtures)
    
    regex = r'\[.*?\]'
    fixtures = [re.sub(regex, '', x).replace('\n', '') for x in fixtures if verify_fixture(x)] 
    
    return fixtures


def verify_fixture(fixture):
    keep = [' v ', ' vs ', ' vs. ', ' between ']
    delete = ['defunct', 'list of']

    for chr in delete:
        if chr in fixture.lower():
            return False
    for chr in keep:
        if chr in fixture.lower():
            return True
    return False


def clean_data(fixtures):
    
    regex = r'\[.*?\]'
    fixtures = [re.sub(regex, '', x).replace('\n', '') for x in fixtures if verify_fixture(x)] 

    errors = []
    fixtures_new = []
    for fixture in fixtures:
        name_and_teams = fixture.split(':')
        if len(name_and_teams) == 2:
            fixtures_new.append({'teams':name_and_teams[1], 'derby_name':name_and_teams[0]})
        elif len(name_and_teams) == 1:
            fixtures_new.append({'teams':name_and_teams[0], 'derby_name':'null'})
        else:
            print(fixture)
            errors.append([fixture])
    
    fixtures = pd.DataFrame(fixtures_new, columns=['teams', 'derby_name'])

    return fixtures, errors


def split_fixtures(fixtures, errors):
    rivals = {}
    match = [' v ', ' vs ', ' vs. ']
    for fixture in fixtures['teams']:
        flag = True
        for chr in match:
            if chr in fixture:
                teams = fixture.split(chr)
                teams[1] = teams[1].split('-')[0]
                rivals[teams[0].strip()] = teams[1].strip()
                flag = False
                break
        if flag:
            errors.append(fixture)

    return rivals, errors

def read_fixture_list(league):
    # fixture_list = {file.split('.')[0]: pd.read_csv(f"fixtures/{file}") for file in os.listdir("fixtures")}
    try:
        df = pd.read_csv(f"fixtures/{league}.csv")
    except FileNotFoundError as e:
        print(f"{league} does not match any csvs")
        sys.exit()
    except Exception as e:
        print(e)
        sys.exit()

    fixture_list = df[['Date', 'Home Team', 'Away Team']].copy()
    return fixture_list


main()
