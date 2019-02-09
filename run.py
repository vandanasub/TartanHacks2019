import json
import re

def parsejson(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        textstring = ""
        for obj in data['recognitionResult']['lines']:
            textstring += obj['text'] + '\n'

        # post-processing
        textstring = re.sub("_", "", textstring)
        textstring = re.sub("`", "", textstring)
        textstring = re.sub("\|", "", textstring)
        textstring = re.sub("\^", "", textstring)
        textstring = re.sub("\\\\", "", textstring)
        return textstring
