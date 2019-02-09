import requests
import time
from run import parsejson
from spelling import words
# If you are using a Jupyter notebook, uncomment the following line.
#%matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import simplejson as json
from keyphrase import keyPhrase

def spellcheck(val):
	f = open("output.txt", "w")
	res = words(val)
	s = ' '.join(res)
	return s


def run(filepath, res):
	# Replace <Subscription Key> with your valid subscription key.
	subscription_key = "bdc1312c4a4f4371ad51430be98ae6cc"
	assert subscription_key

	# You must use the same region in your REST call as you used to get your
	# subscription keys. For example, if you got your subscription keys from
	# westus, replace "westcentralus" in the URI below with "westus".
	#
	# Free trial subscription keys are generated in the "westus" region.
	# If you use a free trial subscription key, you shouldn't need to change
	# this region.
	vision_base_url = "https://westcentralus.api.cognitive.microsoft.com/vision/v2.0/"

	text_recognition_url = vision_base_url + "recognizeText"

	# Set image_url to the URL of an image that you want to analyze.

	#image_url = "https://image.slidesharecdn.com/2-160329173523/95/computer-network-notes-handwritten-unit-1-1-638.jpg?cb=1487791184"
	image_path = filepath
	headers = {'Ocp-Apim-Subscription-Key': subscription_key,
			   'Content-Type':'application/octet-stream'}
	# Note: The request parameter changed for APIv2.
	# For APIv1, it is 'handwriting': 'true'.
	params  = {'mode': 'Handwritten'}
	#data    = {'url': image_url}
	data = open(image_path, "rb").read()
	response = requests.post(
	    text_recognition_url, headers=headers, params=params, data=data)
	response.raise_for_status()


	# Extracting handwritten text requires two API calls: One call to submit the
	# image for processing, the other to retrieve the text found in the image.

	# Holds the URI used to retrieve the recognized text.
	operation_url = response.headers["Operation-Location"]

	# The recognized text isn't immediately available, so poll to wait for completion.
	analysis = {}
	poll = True
	while (poll):
	    response_final = requests.get(
	        response.headers["Operation-Location"], headers=headers)
	    analysis = response_final.json()
	    time.sleep(1)
	    if ("recognitionResult" in analysis):
	        poll= False 
	    if ("status" in analysis and analysis['status'] == 'Failed'):
	        poll= False

	f = open("output.txt", "w")
	f.write(json.dumps(analysis))
	f.close()
	val = parsejson("output.txt")
	val = spellcheck(val)
	keyPhr = keyPhrase(val)
	length = len(keyPhr)
	max = length/10

	polygons=[]
	length = len(keyPhr)
	length = length//10
	flag = True
	num = 0

	temp = keyPhr
	keyPhr = list(keyPhr)[0:length]

	if ("recognitionResult" in analysis):
		# Extract the recognized text, with bounding boxes.
		polygons = [(line["boundingBox"], line["text"])
			for line in analysis["recognitionResult"]["lines"]]

	# Display the image and overlay it with the extracted text.
	plt.figure(figsize=(15, 15))
	image = Image.open(BytesIO(data))
	ax = plt.imshow(image)
	
	for polygon in polygons:
		vertices = [(polygon[0][i], polygon[0][i+1])
			for i in range(0, len(polygon[0]), 2)]
		text     = polygon[1]
		col = 'w'
		for phrase in keyPhr:
			if phrase in text:
					# print(phrase+"\n")
					# print(num+"\n")
					# print(length+"\n")
				col = 'r'
					# num+=1
					# if(num == length):
					# 	flag = False
					# 	break
				# if(flag == False):
				# 	break
		patch    = Polygon(vertices, closed=True, fill=False, linewidth=2, color=col)
		ax.axes.add_patch(patch)
		#plt.text(vertices[0][0], vertices[0][1], text, fontsize=20, va="top")
	_ = plt.axis("off")
	plt.savefig(res)
	return(val, temp)
