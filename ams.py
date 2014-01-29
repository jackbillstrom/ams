import requests, json, time
from progressbar import *

# Print a fancy ascii-art
print """
  __ _ _ __ ___  ___ 
 / _` | '_ ` _ \/ __|
| (_| | | | | | \__ \\
 \__,_|_| |_| |_|___/
   
"""

def count_pages():
	print "Grabing states"
	# Array with all state ID's
	states = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25]
	# Arrays length
	states_len = len(states)
	# Store the page-count in a dict
	pages = {}
	# Create a progressbar widget
	widgets = [Bar('='), ' ', ETA(), ' ', ReverseBar('=')]
	pbar = ProgressBar(widgets=widgets, maxval=states_len).start()
	#for i in range(1000000):
	for state in range (states_len):
		pbar.update(state)
		endpoint = "http://api.arbetsformedlingen.se/platsannons/matchning?lanid="+str(states[state])
		try:
			headers = {'Accept-Language': 'application/json'}
			r = requests.get(endpoint, headers=headers) 
			data = json.loads(r.content)
			page_count =  str(data['matchningslista']['antal_sidor'])
		except:
			continue
		pages[state+1] = page_count

	pbar.finish()
	# Pass our array so that we could grab all ad id's from the API
	grab_ad_id(pages)

def grab_ad_id(pages):
	# Maybe we should get all ID's, state by state ?
	ad_id = []
	for key, value in pages.iteritems():
		for num in range(int(value)):
			#  str(key) = State
			#  str(num+1) = The states page count
			endpoint = "http://api.arbetsformedlingen.se/platsannons/matchning?lanid="+str(key)+"&sida="+str(num+1)
			# get all of our results, and each individual ID
			try:
				headers = {'Accept-Language': 'application/json'}
				r = requests.get(endpoint, headers=headers) 
				data = json.loads(r.content)
				for i in range(len(data['matchningslista']['matchningdata'])):
					ad_id.append(data['matchningslista']['matchningdata'][i]['annonsid'])
			except:
				continue
		# Save to textfile
		f = open('id.txt', 'w')
		json.dump(ad_id, f)
		f.close()

count_pages()
