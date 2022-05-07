from math import modf

from Event import Event
from Range import Range
from RatioBlock import RatioBlock


# will be loading sensitivities, carb ratios, and basals
def parse_ratios(filepath):
	lines = []
	for line in open(filepath):
		lines.append(line[:-1])

	firstTokens = lines[0].split(",")

	if(len(firstTokens) != 2 or firstTokens[0] != "time" or firstTokens[1] != "ratio"):
		raise Exception("first line of ratios must be time | ratio")

	if(Range.parse_time(lines[1].split(",")[0]) != 0):
		raise Exception("first time in ratios must be 00:00")

	ratioPoints = []
	for line in lines[1:]:
		tokens = line.split(",")

		if(len(tokens) != 2):
			raise Exception("wrong number of entries on line " + line + " of " + filepath)

		time = Range.parse_time(tokens[0])
		ratio = float(tokens[1])
		ratioPoints.append([time, ratio])

	ratioBlocks = []
	for i in range(len(ratioPoints)):
		timeStart = ratioPoints[i][0]
		timeEnd = ratioPoints[i+1][0] if i < len(ratioPoints) - 1 else 24.
		ratio = ratioPoints[i][1]

		ratioBlocks.append(RatioBlock(
			range = Range(start = timeStart, end = timeEnd),
			ratio = ratio))

	return ratioBlocks


def parse_events(filepath):
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

	events = []
	uid = 0
	for line in lines[1:]:
		if(line.isspace()):
			continue

		events.append(Event.Parse(line, uid))
		uid += 1

	return events


# events = parse_events("example_input/events.csv")
# for event  in events:
# 	print(event)



