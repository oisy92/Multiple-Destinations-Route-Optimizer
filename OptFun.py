#!/usr/bin/env python
import os
import urllib, json, pdb
import datetime
from itertools import chain, combinations, permutations
import time
from tstr2sec import fun_tstr2sec



start_time = time.time()


# global best_route
# global best_time

# origins = '15 Alice St Kedron QLD'
# destinations = '15 Alice St Kedron QLD'
# waypoints = '17 Munro St, AUCHENFLOWER QLD-5 Raymore Ct, CARINDALE QLD-111 Wellington Rd, EAST BRISBANE QLD'
# mode = 'Driving'
# depart_time = '2018-08-31 16:30'


def mainfun(origins, destinations, waypoints, mode, depart_time):
	endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
	api_key = 'AIzaSyAqlGwiISp3_DE6vtShdH9VmANV4GuK_hQ'
	currentdate = datetime.datetime.today().strftime('%Y-%m-%d')
	if str(depart_time) == "now":
		timestamp = time.time()
	else:
		depart_time = str(str(currentdate)+ ' ' + depart_time)
		ts = time.strptime(depart_time, '%Y-%m-%d %H:%M')
		timestamp = time.mktime(ts)
	departure_time = (timestamp)
	departure_time = "{:.0f}".format((departure_time))
	origins = origins.replace(" ","+")
	destinations = destinations.replace(" ","+")
	waypoints_names = waypoints.replace(" ","+")
	waypoints_names = waypoints_names.split('-')
	traffic_mode = 'pessimistic'

	

	way_num = len(waypoints_names)
	requested_possible_combs = []
	total_time = 0
	itcount = 0
	calculated = {}
	permutation = []
	a = 0
	b = 0
	first = 'true'
	orig_destinations = destinations
	orig_origin = origins
	permutation_raw = list(permutations(waypoints_names, way_num))


	for n in permutation_raw:
		n = list(n)
		n.append(destinations)
		n.insert(0,origins)
		permutation.append(n)

	# print(len(permutation))
	for route in permutation:

		num_routes = len(permutation)
		len_route = len(route)
		duration = 0
		total_time = 0
		count = 0
		prog = int(itcount)/(num_routes)*100	
		if first == 'false':
			itcount += 1
			# os.system('cls')

		
		while (count < len_route-1):
			# print(calculated.items())
			a = count
			b = a +1
			count += 1	
			check = str(route[a]+route[b]) in calculated.keys()
			if str(check) == 'True':
				duration = calculated.get(route[a]+route[b])
				# print(CGREEN2+'Saved route', route[a],route[b],(datetime.timedelta(seconds=int(duration))))
				total_time = int(duration) + int(total_time)
				# sleep(1)
				# print (total_time)
			elif str(check) == 'False':
				# print(CRED+'New route')
				calculated[str(route[a]+route[b])] = duration
				# print(calculated)
				nav_request = 'origins={}&destinations={}&departure_time={}&mode={}&traffic_model={}&key={}'.format(route[a],route[b],departure_time,mode,traffic_mode,api_key)
				# print(nav_request)
				# print ("Origin : ", route[a], "Destination : ", route[b])
				request = endpoint + nav_request
				#Sends the request and reads the response.
				response = urllib.urlopen(request).read()
				#Loads response as JSON
				directions = json.loads(response)
				# print(directions)
				trip_time = (directions["rows"][0]["elements"][0]["duration"]["text"])
				duration = fun_tstr2sec(trip_time)

				
				calculated[str(route[a]+route[b])] = duration
				calculated.copy().items()

				total_time = int(duration) + int(total_time)
				
				# sleep(1)
				# print (total_time)

		if first == 'true':
			best_time = total_time
			best_route = route
			calculated[str(route[a]+route[b])] = duration
			# os.system('cls')
			# print (CYELLOW2 + 'Optimized Route Found: ' + CGREEN2 + str(route).replace("+"," ") + CEND)
			# print (CYELLOW2 + 'Total trip duration of:' + CRED2 + str(datetime.timedelta(seconds=best_time)) + CEND + CYELLOW2 + " Progress" + CRED2 + " %d" % (prog) + "%" + CEND)
			# print (CYELLOW2 + "Progress" + CRED2 + " %d" % (prog) + "%" + CEND)
			first = 'false'

		if first == 'false' and total_time < best_time:
			best_time = total_time
			best_route = str(route).replace("+"," ")
			# os.system('cls')
			# print (CYELLOW2 + 'Optimized Route Found: ' + CGREEN2 + str(route).replace("+"," ") + CEND)
			# print (CYELLOW2 + 'Total trip duration of: ' + CRED2 + str(datetime.timedelta(seconds=best_time)) + CEND)
			# print (CYELLOW2 + "Progress: " + CRED2 + " %d" % (prog) + "%" + CEND)
	# best_route = best_route.replace("['"," ")
	# best_route = best_route.replace("']"," ")
	# best_route = best_route.replace("', u'","|")
	# best_route = "|".join(best_route)
	best_time = str(datetime.timedelta(seconds=best_time))
	return best_route, best_time
