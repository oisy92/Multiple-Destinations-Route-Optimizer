#!/usr/bin/env python
import os
import urllib, json, pdb
import datetime
from itertools import chain, combinations, permutations
import time
from tstr2sec import fun_tstr2sec

#Initialize Time
start_time = time.time()

#Main Function
def mainfun(origins, destinations, waypoints, travel_mode, depart_time):
	#Setting up Google API request
	endpoint = 'https://maps.googleapis.com/maps/api/distancematrix/json?'
	#Converting user input to readable format by the software.
	currentdate = datetime.datetime.today().strftime('%Y-%m-%d')
	if depart_time == "now":
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
	#Creating dictionaries to host user waypoints for the permutations process
	way_num = len(waypoints_names)
	requested_possible_combs = []
	permutation = []
	#Defining initial variables
	#a= first stop, b = second stop, total_time= time from stop a to stop b, itcount = premuation calculation count, first = boolean value to check if first premuation count.
	a = 0
	b = 0
	total_time = 0
	itcount = 0
	first = True
	orig_destinations = destinations
	orig_origin = origins
	#Creating list of all possible routes between all user waypoints. The list contains as many rows as possible routes.
	permutation_raw = list(permutations(waypoints_names, way_num))
	#Because the route will always start from the origin and ends at the destiniation, the below line modifies the raw permutation list to add origin stop at the beginnning of the route, and destiniation at the end of the route
	for n in permutation_raw:
		n = list(n)
		n.append(destinations)
		n.insert(0,origins)
		permutation.append(n)
	return opttimzer(permutation, a, b , first, destinations, origins, departure_time, traffic_mode, travel_mode, api_key, endpoint)
		
#Optimization/Salesman problem algorithm start here. In short, the software sends API request to Google Maps requesting travel time between point A to point B. Then, it recives Json structure containing travelling time between point A to point B. After that, the software stores the received data in a list, and compares them with the next travelling time taken to travel between point A and C, if it's less than A and B; it nominates it as better route.
def opttimzer(permutation, a, b , first, destinations, origins, departure_time, traffic_mode, travel_mode, api_key, endpoint):
	for route in permutation:
		num_routes = len(permutation)
		len_route = len(route)
		duration = 0
		total_time = 0
		count = 0
		itcount = 0
		calculated = {}
		prog = int(itcount)/(num_routes)*100	
		if not first:
			itcount += 1
		while (count < len_route-1):
			a = count
			b = a +1
			count += 1	
			check = str(route[a]+route[b]) in calculated.keys()
			if check:
				duration = calculated.get(route[a]+route[b])
				total_time = int(duration) + int(total_time)
			elif not check:
				calculated[str(route[a]+route[b])] = duration
				nav_request = 'origins={}&destinations={}&departure_time={}&mode={}&traffic_model={}&key={}'.format(route[a],route[b],departure_time,travel_mode,traffic_mode,api_key)
				request = endpoint + nav_request
				response = urllib.urlopen(request).read()
				directions = json.loads(response)
				trip_time = (directions["rows"][0]["elements"][0]["duration"]["text"])
				duration = fun_tstr2sec(trip_time)
				calculated[str(route[a]+route[b])] = duration
				calculated.copy().items()
				total_time = int(duration) + int(total_time)
		if first:
			best_time = total_time
			best_route = route
			calculated[str(route[a]+route[b])] = duration
			first = False
		if not first and total_time < best_time:
			best_time = total_time
			best_route = str(route).replace("+"," ")
	best_time = str(datetime.timedelta(seconds=best_time))
	return best_route, best_time
