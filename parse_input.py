from Event import Event, EventType, Level, Source
from Range_of_Time import Range_of_Time
from RatioBlock import RatioBlock



def parse_time(time_string, default):

	if time_string == "":

		return default


	else:

		time = time_string.split(":")

		if len(time) != 2:
			raise Exception("The time " + time_string + " was not entered as a military time hh:mm.")

		hours = int( time[0] )
		minutes = int( time[1] )

		return float(hours) + float(minutes)/60.



def parse_integer(string, default):
	try:
		return int(string)
	except:
		return default



def parse_events(file):


	lines = []

	for line in open(file):
		lines.append( line[ :-1] )


	first_line_tokens = lines[0].split(",")

	if len(first_line_tokens) != 10:
		raise Exception \
("Each line of glucan/" + file + " should have the ten columns, \
independent_bolus_or_correction, \
start_time, \
start_ low_in_range_or_high, \
start_ blood_glucose, \
adjustment_time, \
end_time, end_time_ sensor_or_test, \
end_ low_in_range_or_high, end_level_ test_or_sensor, and \
end_ blood_glucose, \
and no more.")

	if ( first_line_tokens[0] != "independent_bolus_or_correction" or
	     first_line_tokens[1] != "start_time" or
	     first_line_tokens[2] != "start_ low_in_range_or_high" or
	     first_line_tokens[3] != "start_ blood_glucose" or
	     first_line_tokens[4] != "adjustment_time" or
	     first_line_tokens[5] != "end_time" or
	     first_line_tokens[6] != "end_time_ sensor_or_test" or		
	     first_line_tokens[7] != "end_ low_in_range_or_high" or
	     first_line_tokens[8] != "end_level_ test_or_sensor" or
	     first_line_tokens[9] != "end_ blood_glucose"
		):
		raise Exception \
("The first line of glucan/data/events.csv should be \
| independent_bolus_or_correction \
| start_time \
| start_ low_in_range_or_high \
| start_ blood_glucose \
| adjustment_time \
| end_time | end_time_ sensor_or_test \
| end_ low_in_range_or_high | end_level_ test_or_sensor \
| end_ blood_glucose |.")


	events = []
	uid = 0
	printed_alert = False


	for line in lines[1: ]:


		if line.isspace():
			continue


		tokens = line.split(",")

		# ensuring empty columns after the final entry in a line are parsed
		while len(tokens) < 10:
			tokens.append("")


		# parsing entries

		event_type = EventType.parse(tokens[0])

		start_time = parse_time(tokens[1], -1)

		start_level = Level.parse(tokens[2])

		start_bg = parse_integer(tokens[3], -1)

		adjustment_time = parse_time(tokens[4], -1)

		end_time = parse_time(tokens[5], -1)
		end_time_source = Source.parse(tokens[6])

		end_level = Level.parse(tokens[7])
		end_level_source = Source.parse(tokens[8])

		end_bg = parse_integer(tokens[9], -1)
		

		# making range of time compliant

		if end_time != -1 and end_time < start_time:
			end_time += 24.

		range = Range_of_Time(start = start_time, end = end_time)


		# ensuring events with an end_bg have TEST as their end_level_source
		if end_bg != -1:
			end_level_source = Source.TEST


		# making event_string

		event_string = ""

		if adjustment_time != -1:
			event_string = event_string + Range_of_Time.time_str(adjustment_time) + " "

		if event_type == EventType.INDEPENDENT:
			event_string = event_string + "independent event "
		elif event_type == EventType.BOLUS:
			event_string = event_string + "bolus "
		elif event_type == EventType.CORRECTION:
			event_string = event_string + "correction "
		elif event_type == EventType.UNKNOWN:
			event_string = event_string + "event "

		event_string = event_string + "starting with a(n) " + str(start_level) + " blood glucose "

		if start_bg != -1:
			event_string = event_string + "of " + str(start_bg) + " mg/dL "

		if start_time != -1:
			event_string = event_string + "at " + Range_of_Time.time_str(start_time) + " "

		event_string = event_string + "and ending with a(n) " + str(end_level) + " blood glucose "		

		if end_bg != -1:
			event_string = event_string + "of " + str(end_bg) + " mg/dL "

		if end_time != -1:
			event_string = event_string + "at " + Range_of_Time.time_str(end_time) + " "	


		# printing alerts or raising exceptions in order to get more useful event entries

		if event_type == EventType.UNKNOWN:
			raise Exception("The " + event_string + "has an unknown event type.")

		if start_time == -1: 
			raise Exception("The " + event_string + "has an unknown start time.")

		if start_level == Level.UNKNOWN and event_type == EventType.BOLUS:
			raise Exception("The " + event_string + "has an unknown start level.")

		if start_bg == -1 and \
		   event_type == EventType.BOLUS and start_level == Level.IN_RANGE and end_time - adjustment_time >= 2 and end_level_source == Source.TEST:

			if printed_alert == False:
				print("")
				print("")
				print("")
			print("The " + event_string + "has an unknown start glucose.")
			print("")

			printed_alert = True

		if adjustment_time == -1 and (event_type == EventType.BOLUS or event_type == EventType.CORRECTION):
			raise Exception("The " + event_string + "has an unknown adjustment time.")

		if end_time == -1:
			raise Exception("The " + event_string + "has an unknown end time.")
		
		if end_time-start_time + 0.00000000000001 < 4:

			raise Exception("The " + event_string + "has a range of time less than 4 hours.")

		if end_time-start_time + 0.00000000000001 >= 12:

			if printed_alert == False:
				print("")
				print("")
				print("")
			print("The " + event_string + "has a range of time greater than or equal to 12 hours.")
			print("")

			printed_alert = True

		if adjustment_time != -1 and not range.contains_time(adjustment_time, True):
			raise Exception("The " + event_string + "has an adjustment time that isn't a part of its range of time.")

		if end_time_source == Source.UNKNOWN:

			if printed_alert == False:
				print("")
				print("")
				print("")
			print("The " + event_string + "has an unknown end time source.")
			print("")

			printed_alert = True

			end_time_source = Source.TEST

		if end_time_source == Source.SENSOR and \
		   end_time-start_time - 0.00000000000001 > 4:
				raise Exception("The " + event_string + "has a range of time not equal to 4 hours.")

		if end_level == Level.UNKNOWN:
			raise Exception("The " + event_string + "has an unknown end level.")

		if end_level_source == Source.UNKNOWN:

			if printed_alert == False:
				print("")
				print("")
				print("")
			print("The " + event_string + "has an unknown end level source.")
			print("")

			printed_alert = True

			end_level_source = Source.SENSOR

		if end_bg == -1 and \
		   event_type == EventType.BOLUS and start_level == Level.IN_RANGE and end_time - adjustment_time >= 2 and end_level_source == Source.TEST:

			if printed_alert == False:
				print("")
				print("")
				print("")
			print("The " + event_string + "has an unknown end glucose.")
			print("")

			printed_alert = True


		events.append( Event( \
			uid = uid, \
			type = event_type, \
			start_level = start_level, \
			start_bg = start_bg, \
			adjustment_time = adjustment_time, \
			end_time_source = end_time_source, \
			end_level = end_level, \
			end_level_source = end_level_source, \
			end_bg = end_bg, \
			range = range ) )


		uid += 1


	if printed_alert == True:
		print("")
		print("")


	return events



def parse_ratio_blocks(file, ratio_type):


	lines = []

	for line in open(file):
		lines.append( line[ :-1] )


	first_line_tokens = lines[0].split(",")

	if len(first_line_tokens) != 2:
		raise Exception("Each line of glucan/" + file + " should have exactly two entries, a start_time and a ratio entry." )

	if first_line_tokens[0] != "start_time" or first_line_tokens[1] != "ratio" :
		raise Exception("The first line of glucan/" + file + " should be | start_time | ratio |.")


	if(parse_time(lines[1].split(",")[0], -1) != 0):
		raise Exception("The first start_time in glucan/" + file + " should be 00:00.")


	start_times_and_ratios = []

	for line in lines[1: ]:


		tokens = line.split(",")


		start_time = parse_time(tokens[0], -1)

		if start_time == -1:
			raise Exception("Line " + line + " of glucan/" + file + " should have a start_time entry.")

		ratio = float( tokens[1] )


		start_times_and_ratios.append( [start_time, ratio] )


	ratio_blocks = []
	uid = 0

	for i in range(0, len(start_times_and_ratios)):

		start_time = start_times_and_ratios[i][0]

		if i < len(start_times_and_ratios) - 1:
			end_time = start_times_and_ratios[i+1][0]
		else:
			end_time = 24.
		
		ratio = start_times_and_ratios[i][1]


		ratio_blocks.append(RatioBlock(
			uid = uid,
			range = Range_of_Time(start = start_time, end = end_time),
			ratio = ratio,
			type = ratio_type))
		
		
		uid += 1

	return ratio_blocks