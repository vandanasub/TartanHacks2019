import pprint
subscription_key = "8e4496657d114d88a93dc38582c339dc"
assert subscription_key
import requests
text_analytics_base_url = "https://eastus.api.cognitive.microsoft.com/text/analytics/v2.0/"
key_phrase_api_url = text_analytics_base_url + "keyPhrases"
print(key_phrase_api_url)
f = open("text.txt", "r")
thetext = ""
for line in f:
	thetext += line.rstrip()

documents = {'documents' : [
  {'id': '1', 'language': 'en', 'text': thetext},
]}
headers   = {'Ocp-Apim-Subscription-Key': subscription_key}
response  = requests.post(key_phrase_api_url, headers=headers, json=documents)
key_phrases = response.json()
pprint.pprint(key_phrases)