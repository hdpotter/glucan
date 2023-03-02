from Event import Event
from Range import Range
from RatioBlock import RatioBlock



def parse_ratio_blocks(file, ratio_type):


	lines = []

	for line in open(file):
		lines.append( line[ :-1] )


	first_line_tokens = lines[0].split(",")

	if len(first_line_tokens) != 2:
			raise Exception("Each line of glucan/" + file + " should have exactly two entries, a start_time and a ratio entry." )

	if first_line_tokens[0] != "start_time" or first_line_tokens[1] != "ratio" :
		raise Exception("The first line of glucan/" + file + " should be | start_time | ratio |.")


	if(Range.parse_time(lines[1].split(",")[0], -1) != 0):
		raise Exception("The first start_time in glucan/" + file + " should be 00:00.")


	start_times_and_ratios = []

	for line in lines[1: ]:


		tokens = line.split(",")


		start_time = Range.parse_time(tokens[0], -1)

		if start_time == -1:
			raise Exception("Line " + line + " of glucan/" + file + " should have a start_time entry.")

		ratio = float( tokens[1] )


		start_times_and_ratios.append( [start_time, ratio] )


	ratio_blocks = []
	uid = 0

	for i in range(len(start_times_and_ratios)):   # Why?

		start_time = start_times_and_ratios[i][0]

		if i < len(start_times_and_ratios) - 1:
			end_time = start_times_and_ratios[i+1][0]
		else:
			end_time = 24.
		
		ratio = start_times_and_ratios[i][1]


		ratio_blocks.append(RatioBlock(
			uid = uid,
			range = Range(start = start_time, end = end_time),   # Why?
			ratio = ratio,
			type = ratio_type))
		
		
		uid += 1

	return ratio_blocks



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
("The first line of glucan/data/events.csv should be \
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