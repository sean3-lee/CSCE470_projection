import json

events_array = []
with open('events_data.json', 'r') as file:
    events_array = json.load(file)

print(len(events_array))