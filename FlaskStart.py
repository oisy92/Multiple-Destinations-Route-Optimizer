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
	
@app.route("/error")
def errorfun():
	return render_template('Error.html')

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
	depart_time = str(depart_time[0])
	endP = str(endP[0])
	startP = str(startP[0])
	mode = str(mode[0])
	waypoints = '-'.join(waypoints)
	best_route, best_time = mainfun(startP, endP, waypoints, mode, depart_time)
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
	global waypoints
	global mode
	global depart_time
	global startP
	global endP
	global best_route
	global best_time
	optimizedrouteFINAL = "|".join(optimizedrouteEXTRACTED)
	endP = endP.replace(",","+")
	startP = startP.replace(",","+")
	endP = endP.replace(" ","+")
	startP = startP.replace(" ","+")
	best_routeFORMATED = best_route.replace("+"," ")
	best_routeFINAL = re.findall("'([^']+)'", best_routeFORMATED)
	url = "https://www.google.com/maps/embed/v1/directions?key=INSERT YOUR API&origin="
	url = url+str(startP)+"&destination="+str(endP)+"&waypoints="+str(optimizedrouteFINAL)+"&mode="+str(mode)+"&units=metric&avoid=tolls"
	startP = startP.replace("+"," ")
	endP = endP.replace("+"," ")
	return render_template('Results.html', best_routeFINAL=best_routeFINAL, best_time=best_time, startP=startP, endP=endP, mode=mode, url=url)

if __name__== '__main__':
    app.run(debug=True)
