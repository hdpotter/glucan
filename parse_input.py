from Event import Event
from Range import Range
from RatioBlock import RatioBlock


# will be loading sensitivities, carb ratios, and basals
def parse_ratios(filepath, ratio_type):
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
	uid = 0
	for i in range(len(ratioPoints)):
		timeStart = ratioPoints[i][0]
		timeEnd = ratioPoints[i+1][0] if i < len(ratioPoints) - 1 else 24.
		ratio = ratioPoints[i][1]

		ratioBlocks.append(RatioBlock(
			uid = uid,
			range = Range(start = timeStart, end = timeEnd),
			ratio = ratio,
			type = ratio_type))
		uid += 1

	return ratioBlocks


def parse_events(filepath):
	lines = []
	for line in open(filepath):
		lines.append(line[:-1])

	firstTokens = lines[0].split(",")
	if ( len(firstTokens) != 10 or
	     firstTokens[0] != "independent_bolus_or_correction" or
	     firstTokens[1] != "start_time" or
	     firstTokens[2] != "start_ low_in_range_or_high" or
	     firstTokens[3] != "start_ blood_glucose" or
	     firstTokens[4] != "adjustment_time" or
	     firstTokens[5] != "end_time" or
	     firstTokens[6] != "end_time_ sensor_or_test" or		
	     firstTokens[7] != "end_ low_in_range_or_high" or
	     firstTokens[8] != "end_level_ test_or_sensor" or
	     firstTokens[9] != "end_ blood_glucose"
		):
		raise Exception \
("The first line of events.csv should be \
| independent_bolus_or_correction \
| start_time | start_ low_in_range_or_high | start_ blood_glucose \
| adjustment_time \
| end_time | end_time_ sensor_or_test \
| end_ low_in_range_or_high | end_level_ test_or_sensor \
| end_ blood_glucose |.")


	events = []
	uid = 0
	printed_alert = False

	for line in lines[1:]:
		if(line.isspace()):
			continue

		event = Event.parse(line, uid)

		events.append(event)

		if event.printed_alert == True:
			printed_alert = True
	
		uid += 1

	if printed_alert == True:
		print("")
		print("")


	return events


# events = parse_events("example_input/events.csv")
# for event  in events:
# 	print(event)