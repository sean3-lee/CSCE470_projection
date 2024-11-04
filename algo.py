import json

with open('events_data_dict.json', 'r') as file:
    events_dict = json.load(file)

data = {}

# fill out data with title and text
for event in events_dict.values():
    data[event['id']] = {}
    data[event['id']]['title'] = event['name']
    data[event['id']]['text'] = event['text']


# calculate the tf for each event title and text
for event in events_dict.values():
    tf_title = {}
    words = event['name'].split()
    for w in words:
        tf_title[w] = tf_title.get(w, 0) + 1
    data[event['id']]['tf_title'] = tf_title

    tf_text = {}
    words = event['text'].split()
    for w in words:
        tf_text[w] = tf_text.get(w, 0) + 1
    data[event['id']]['tf_text'] = tf_text
    break

