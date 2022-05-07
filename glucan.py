from parse_input import *

# shifts a time range 24h ahead in time; this is useful for handling intervals that contain midnight
def timeshift(range):
	return Range(start = range.start + 24., end = range.end + 24.)

# returns the duration of a range
def duration(range):
	return range.end - range.start

# returns true if range1 contains range2
def contains(range1, range2):
	return range1[0] <= range2[0] and range1[1] >= range2[1]

# returns the size of the overlapping range
def calc_overlap(range1, range2):
	return calc_overlap_nowrap(range1, range2) #\
		# + calc_overlap_nowrap(timeshift(range1), range2) \
		# + calc_overlap_nowrap(range1, timeshift(range2))

def calc_overlap_nowrap(range1, range2):
	# no overlap
	if range1[0] >= range2[1] or range2[0] >= range1[1]:
		return 0

	# one range contains the other
	if contains(range1, range2):
		return range2[1] - range2[0]
	if contains(range2, range1):
		return range1[1] - range1[0]

	# overlap but one doesn't contain the other
	if range1[0] <= range2[0]:
		return range1[1] - range2[0]
	if range2[0] <= range1[0]:
		return range2[1] - range1[0]

	raise Exception("unhandled range overlap type: overlap(" + range1 + ", " + range2 + ")")


# def analyze_sensitivity(event, sensitivity, overlap):
# 	if event["type"] == "independent":
# 		overlapFraction = overlap / 




sensitivities = parseRatios("example_input/sensitivities.csv")
basals = parseRatios("example_input/basals.csv")
events = parseEvents("example_input/events.csv")

sensitivitiesImpacting = {}
basalsImpacting = {}

for i in events:
	event = events[i]

	sensitivitiesImpacting[i] = []
	basalsImpacting[i] = []

	if(event["type"] == "independent"):
		for j in sensitivities:
			sensitivity = sensitivities[j]
			overlap = calc_overlap(sensitivity["range"], event["range"])

			if overlap > 0:
				sensitivitiesImpacting[i].append([j, overlap])

		for j in basals:
			basal = basals[j]
			overlap = calc_overlap(basal["range"], event["range"])

			if overlap > 0:
				basalsImpacting[i].append([j, overlap])


for i in events:
	print("\nevent:")
	print(events[i])
	print("sensitivity overlap:")

	for impact in sensitivitiesImpacting[i]:
		sensitivity = sensitivities[impact[0]]
		print(rangeString(sensitivities[impact[0]]["range"]) + ", overlap " + timeString(impact[1]))

			
			







