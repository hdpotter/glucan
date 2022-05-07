

from math import modf

def parseTime(timeString):
	tokens = timeString.split(":")

	if len(tokens) != 2:
		raise Exception("time format is hh:mm, 24h time")

	hours = int(tokens[0])
	minutes = int(tokens[1])

	return float(hours) + float(minutes)/60.

def timeString(time):
	hours = modf(time)[1]
	hourFrac = modf(time)[0]

	minutes = modf(hourFrac*60)[1]
	minuteFrac = modf(hourFrac*60)[0]

	seconds = modf(minuteFrac*60)[1]

	# we might get a tiny fraction of a second from floating point error, so ignore it
	if(seconds >= 0.01):
		return str(int(hours)) + ":" + str(int(minutes)).zfill(2) + ":" + str(seconds)
	else:
		return str(int(hours)) + ":" + str(int(minutes)).zfill(2)

def rangeString(range):
	return "[" + timeString(range[0]) + " - " + timeString(range[1]) + "]"
	# return "[" + str(range[0]) + " - " + str(range[1]) + "]"

# will be loading sensitivities, carb ratios, and basals
def parseRatios(filepath):
	lines = []
	for line in open(filepath):
		lines.append(line[:-1])

	firstTokens = lines[0].split(",")

	if(len(firstTokens) != 2 or firstTokens[0] != "time" or firstTokens[1] != "ratio"):
		raise Exception("first line of sensitivities must be time | ratio")

	if(parseTime(lines[1].split(",")[0]) != 0):
		raise Exception("first time in sensitivities must be 00:00")

	sensitivityPoints = []
	for line in lines[1:]:
		tokens = line.split(",")

		if(len(tokens) != 2):
			raise Exception("wrong number of entries on line " + line + " of sensitivities")

		time = parseTime(tokens[0])
		sensitivity = float(tokens[1])
		sensitivityPoints.append([time, sensitivity])

	sensitivityRanges = {}
	uid = 0
	for i in range(len(sensitivityPoints)):
		timeStart = sensitivityPoints[i][0]
		timeEnd = sensitivityPoints[i+1][0] if i < len(sensitivityPoints) - 1 else 24.
		sensitivity = sensitivityPoints[i][1]

		sensitivityRanges[uid] = {"uid": uid, "range": [timeStart, timeEnd], "sensitivity": sensitivity}
		
		uid += 1

	return sensitivityRanges


def parseEvents(filepath):
	lines = []
	for line in open(filepath):
		lines.append(line[:-1])

	firstTokens = lines[0].split(",")
	if(len(firstTokens) != 9 or
		firstTokens[0] != "event_type" or
		firstTokens[1] != "start_time" or
		firstTokens[2] != "low_normal_high" or
		firstTokens[3] != "start_glucose" or
		firstTokens[4] != "end_time" or
		firstTokens[5] != "low_normal_high" or
		firstTokens[6] != "end_glucose" or
		firstTokens[7] != "glucose_type" or
		firstTokens[8] != "basal_or_sensitivity"
		):
		raise Exception("first line of events must be event_type | start_time | low_normal_high | glucose | end_time | low_normal_high | glucose | glucose_type | basal_or_sensitivity")

	events = {}
	uid = 0
	for line in lines[1:]:
		tokens = line.split(",")

		if(len(tokens) > 9):
			raise Exception("too many entries on line " + line + " of events")
		while(len(tokens) < 9):
			tokens.append("")

		if(tokens[0] != "independent" and tokens[0] != "correction" and tokens[0] != "bolus"):
			raise Exception("type on line " + line + " must be independent, correction, or bolus")
		eventType = tokens[0]

		time1 = parseTime(tokens[1])

		range1 = ""
		if(eventType != "correction"):
			if(tokens[2] != "low" and tokens[2] != "high" and tokens[2] != "normal"):
				raise Exception("glucose range on line " + line + " must be low, normal, or high")
			range1 = tokens[2]

		glucose1 = int(tokens[3])

		time2 = parseTime(tokens[4])

		# mandatory field
		range2 = ""
		if(eventType != "independent"):
			if(tokens[5] != "low" and tokens[5] != "high" and tokens[5] != "normal"):
				raise Exception("glucose range on line " + line + " must be low, normal, or high")
			range2 = tokens[5]

		# optional field
		glucose2 = int(tokens[6])

		if(tokens[7] != "sensor" and tokens[7] != "test"):
			raise Exception("source on line " + line + " must be sensor or test")
		source = tokens[7]

		if(tokens[8] != "basal" and tokens[8] != "sensitivity"):
			raise Exception("method on line " + line + " must be basal or sensitivity")
		method = tokens[8]

		# make ranges compliant
		if(time2 < time1):
			print("adding 24h to time because range contains midnight")
			time2 += 24.


		event = {}
		event["uid"] = uid
		event["type"] = eventType
		# event["time1"] = time1
		event["range1"] = range1
		event["glucose1"] = glucose1
		# event["time2"] = time2
		event["range2"] = range2
		event["glucose2"] = glucose2
		event["source"] = source
		event["method"] = method

		event["range"] = [time1, time2]

		events[uid] = event
		uid += 1

	return events


# events = parseEvents("events.csv")
# for event  in events:
# 	print(event)



