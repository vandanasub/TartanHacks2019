import json

def parsejson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        for obj in data['recognitionResult']['lines']:
            print(obj['text'])
