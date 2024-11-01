import requests
from youtube_transcript_api import YouTubeTranscriptApi
video_id = 'rv1MzhOMrb8'
# print(YouTubeTranscriptApi.get_transcript(video_id))


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

for i in teams_dict.values():
    # get events for team
    events_url = f'https://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2023/teams/{i}/events?limit=50'
    events = api_call(events_url)
    for j in events['items']:
        d = api_call(j['$ref'])
        print(d)
        break
    break

# data = api_call('https://site.api.espn.com/apis/site/v2/sports/football/nfl/summary?event=401326638')
# print(data['article']['story'])