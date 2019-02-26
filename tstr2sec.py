
def fun_tstr2sec(time):
	if "days" in time or "day" in time:
		time = time.replace("days",":")
		time = time.replace("hours"," ")
		time = time.replace("day",":")
		time = time.replace("hour"," ")
		d,h = time.split(":")
		duration = int(d)*24*60*60 + int(h)*60*60
		return duration
	
	elif "hours" in time or "hour" in time:
		time = time.replace("hours",":")
		time = time.replace("hour",":")
		time = time.replace("mins"," ")
		time = time.replace("min"," ")
		h,m = time.split(":")
		duration = int(h)*60*60 + int(m)*60
		return duration

	elif "mins" in time or "min" in time:
		time = time.replace("mins","")
		time = time.replace("min","")
		# m = time.split(":")
		# print(time)
		duration = int(time)*60
		return duration
