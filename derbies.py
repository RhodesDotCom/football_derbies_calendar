import requests
from bs4 import BeautifulSoup
import sys
from pprint import pprint as pp
import re
import os
import csv
from fuzzywuzzy import fuzz
import itertools


def get_derbies():
    data = get_data("https://en.wikipedia.org/wiki/List_of_association_football_rivalries_in_the_United_Kingdom")
    matches = check_for_teams(data, get_teams())
    derbies = list_of_derbies(matches)
    derbies = unpack_tuples(derbies)
    
    return derbies


def get_data(url):
    try:
        page = requests.get(url)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    try:
        soup = BeautifulSoup(page.text, 'html.parser')
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    content_text = soup.find('div', {'id': 'mw-content-text'}).find('div', {'class': 'mw-parser-output'})
    ul_tags = content_text.find_all('ul')

    content = []
    for ul in ul_tags:
        if "Buchan derby" in ul.get_text():
            break
        else:
            text = search_uls(ul)
            content = content + text

    return content     


def search_uls(ul, text=[]):
    if ul.find_all('li'):
        for li in ul.find_all('li'):
            text = search_lis(li, text)
    else:
        text.append(ul.get_text())
    return text


def search_lis(li, text=[]):
    if li.find_all('ul'):
        for ul in li.find_all('ul'):
            text = search_uls(ul, text)
    else:
        text.append(li.get_text())
    return text
    

def get_fixtures(data):
    fixtures = []
    for body in data.find_all('body'):
            for ul in body.find_all('ul'):
                for li in ul.find_all('li'):
                    fixtures = search_lis(li, fixtures)
    return fixtures


def get_teams():
    teams = []
    folder_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'teams')
    for filename in os.listdir(folder_path):
        if filename.endswith('.csv'):
            csv_path = os.path.join(folder_path, filename)

            with open(csv_path, 'r') as csv_file:
                reader = csv.reader(csv_file)
                for row in reader:
                    teams.append(row[0])
    return teams


def fuzzy_match_elements(all_teams, derbies):
    threshold=90
    
    matches = {}
    regex = r':\s*(.+)'
    for item2 in derbies:
        print('-'*20)
        print(f'Derby: {item2}')

        if ':' in item2:
            match = re.search(regex, item2)
            if match:
                teams_in_derby = match.group(1).split(' vs. ')       
        
        teams_in_derby = teams_in_derby if teams_in_derby else [item2]
        teams = []
        for team1 in teams_in_derby:
            for team2 in all_teams:
                if team1 in team2 or team2 in team1:
                    teams.append(team2)
                elif fuzz.partial_ratio(team1, team2) > 85:
                    teams.append(team2)
        matches[item2] = teams
    pp(matches)
            

def check_for_teams(derbies, all_teams):
    matches = {}
    
    for derby in derbies:
        matched_teams = []
        for team in all_teams:
            if team in derby:
                matched_teams.append(team)
            else:
                for k, v in replacements().items():
                    if k in derby or v in derby:
                        if team.replace(k, v) in derby:
                            matched_teams.append(team)
        matches[derby] = matched_teams
    return matches
        

def list_of_derbies(matches):
    return [list(itertools.combinations(value, 2)) for value in matches.values() if len(value) > 1]
    

def replacements():
    return  {'MK ': 'Milton Keynes ',
            'QPR': 'Queens Park Rangers'
            }


def unpack_tuples(derbies):
    new_list = []
    for l in derbies:
        for k in l:
            new_list.append(k)
    return [list(x) for x in set(new_list)]

