import requests
import re
import json

def save_file(arr):
    with open('events_data_dict.json', 'w') as file:
        json.dump(arr, file)

def process_text(text):
    text = re.sub(r'<a.*?>.*?</a>', '', text)
    text = text.replace('-', ' ')
    text = re.sub(r'[\n\r]+', ' ', text)
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'[^A-Za-z0-9\s]', '', text)
    text = text.lower()
    return text

'''
    Used to make an api call with try-catch protection

    returns: data from api call as a dictionary
'''
def api_call(url):
    try:
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            return data
        else:
            print(f"Failed to retrieve data: {response.status_code}")
    except requests.RequestException as e:
        print(f"An error occurred: {e}")


'''
    Pull all teams and put them in a dictonary
'''
teams_url = 'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/teams?limit=50'
teams_dict = {}

data = api_call(teams_url)

for i in data['items']:
    d = api_call(i['$ref'])
    teams_dict[d['name']] = d['id']


'''
    Get all events from each team - put in once large array
'''
events_array = []
all_events = {}
stats_url = 'https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event='

def get_boxscore_stats(event_id):
    d = api_call(stats_url+event_id)
    return d['boxscore']['teams']

def get_story(event_id):
    d = api_call(stats_url+event_id)
    return process_text(d.get('article', {}).get('story', ''))
    # return d['article']['story']

for i in teams_dict.values():
    # get events for team
    events_url = f'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/teams/{i}/events?limit=50'
    events = api_call(events_url)
    for j in events['items']:
        event_dict = {}
        d = api_call(j['$ref'])
        event_dict['id'] = d['id']
        event_dict['name'] = d['name']
        event_dict['boxscore'] = get_boxscore_stats(d['id'])
        event_dict['story'] = get_story(d['id'])
        events_array.append(event_dict)
        all_events[d['id']] = event_dict

print(len(all_events))
save_file(events_array)
save_file(all_events)

# data = api_call('https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401326638')
# print(data['article']['story'])