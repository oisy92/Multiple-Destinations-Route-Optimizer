from flask import Flask, request, render_template, json, redirect, url_for
import logging
import sys
from OptFun import mainfun
import time
import re
logging.basicConfig(level=logging.DEBUG)
checker = 0
waypoints = []
des = 0
ori = 0
mode = 0
depart_time = 0
best_route= 0
best_time = 0
optimizedrouteEXTRACTED = 0

app = Flask(__name__)
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'
@app.route("/")
@app.route("/path")
def index():
	return render_template('Main.html')
	
@app.route("/GUI")
def home():
	return render_template('Software.html')
	
@app.route("/contact")
def contactfun():
	return render_template('Contact.html')

@app.route('/getjson', methods=['POST'])
def getjsonfun():
	global checker
	global waypoints
	global mode
	global depart_time
	global startP
	global endP
	global best_route
	global best_time
	global optimizedrouteEXTRACTED
	
	checker = 0
	waypoints = request.form.getlist('Waypoints[]')
	mode = request.form.getlist('mode')
	depart_time = request.form.getlist('depart_time')
	startP= request.form.getlist('origins')
	endP = request.form.getlist('destinations')
	waypoints = json.dumps(waypoints)
	waypoints = re.findall('"([^"]*)"', waypoints)
	# waypoints = waypoints.replace("[","")
	# waypoints = waypoints.replace("]","")
	# waypoints = waypoints.replace('"','')
	# print(waypoints)
	# print(type(waypoints))
	depart_time = str(depart_time[0])
	endP = str(endP[0])
	startP = str(startP[0])
	mode = str(mode[0])
	waypoints = '-'.join(waypoints)
	print(startP)
	print (endP)
	print (waypoints)
	print(mode)
	print(depart_time)
	best_route, best_time = mainfun(startP, endP, waypoints, mode, depart_time)
	# print(type(best_route))
	if isinstance(best_route, (list,)):
		best_route = str(best_route)
	optimizedrouteEXTRACTED = re.findall("'([^']+)'", best_route)
	del(optimizedrouteEXTRACTED[0])
	del(optimizedrouteEXTRACTED[-1])

	
	
	

	
	return redirect(url_for('resultsfinal'), code=302)

@app.route('/results')
def resultsfinal():
	global checker
	best_route_decoded = []
	checker = checker +1;
	# best_route = session.get('best_route', None)
	# best_time = session.get('best_time', None)
	# destinations = session.get('destinations', None)
	# origins = session.get('origins', None)
	# mode = session.get('mode', None)
	global waypoints
	global mode
	global depart_time
	global startP
	global endP
	global best_route
	global best_time
	optimizedrouteFINAL = "|".join(optimizedrouteEXTRACTED)
	# print ('BBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBBB')
	# print(type(best_route))
	# best_route = best_route.split('",')
	# print(type(best_route))
	# best_routeC = best_route[1:-1]
	# print ('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
	# print(best_routeC)
	# print(type(best_routeC))
	# print ('CCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCCC')
	# best_routeD = '|'.join(best_routeC)
	# print(best_routeD)
	# print ('DDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDDD')
	endP = endP.replace(",","+")
	startP = startP.replace(",","+")
	endP = endP.replace(" ","+")
	startP = startP.replace(" ","+")
	print ('AAAAAAAAAAAA')
	best_routeFORMATED = best_route.replace("+"," ")
	best_routeFINAL = re.findall("'([^']+)'", best_routeFORMATED)
	print(best_routeFINAL)
	print(type(best_routeFINAL))
	

	url = "https://www.google.com/maps/embed/v1/directions?key=AIzaSyAqlGwiISp3_DE6vtShdH9VmANV4GuK_hQ&origin="
	url = url+str(startP)+"&destination="+str(endP)+"&waypoints="+str(optimizedrouteFINAL)+"&mode="+str(mode)+"&units=metric&avoid=tolls"
	# print(url)
	startP = startP.replace("+"," ")
	endP = endP.replace("+"," ")


	return render_template('Results.html', best_routeFINAL=best_routeFINAL, best_time=best_time, startP=startP, endP=endP, mode=mode, url=url)


if __name__== '__main__':
    app.run(debug=True)
