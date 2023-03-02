from dataclasses import dataclass
from enum import Enum

from Range import Range

class EventType(Enum):
	INDEPENDENT = 0
	BOLUS = 1
	CORRECTION = 2
	UNKNOWN = 3


	@staticmethod
	def parse(string):
		if string == "independent":
			return EventType.INDEPENDENT
		elif string == "bolus":
			return EventType.BOLUS
		elif string == "correction":
			return EventType.CORRECTION
		else:
			return EventType.UNKNOWN



class Level(Enum):
	LOW = 0
	IN_RANGE = 1
	HIGH = 2
	UNKNOWN = 3


	@staticmethod
	def parse(string):
		if string == "low":
			return Level.LOW
		elif string == "in range":
			return Level.IN_RANGE
		elif string == "high":
			return Level.HIGH
		else:
			return Level.UNKNOWN


	def __str__(self):
		if self == Level.LOW:
			return "low"
		if self == Level.IN_RANGE:
			return "in range"
		if self == Level.HIGH:
			return "high"
		if self == Level.UNKNOWN:
			return "unknown"



class Source(Enum):
	SENSOR = 0
	TEST = 1
	UNKNOWN = 2


	@staticmethod
	def parse(string):
		if string == "sensor":
			return Source.SENSOR
		elif string == "test":
			return Source.TEST
		else:
			return Source.UNKNOWN



def parse_int_with_default(string, default):
	try:
		return int(string)
	except:
		return default



@dataclass
class Event:
	uid: int
	type: EventType
	range: Range
	start_level: Level
	start_bg: int
	adjustment_time: float
	end_time_source: Source
	end_level: Level
	end_level_source: Source
	end_bg: int
	printed_alert: bool


	@staticmethod
	def parse(line, uid):

		tokens = line.split(",")

		if(len(tokens) != 10):
			raise Exception("Line " + line + " of events.csv doesn't have ten entries.")

		# ensuring empty columns after the final entry in a line are parsed
		while len(tokens) < 10:
			tokens.append("")


		# parsing entries
		event_type = EventType.parse(tokens[0])
		start_time = Range.parse_time(tokens[1], -1)
		start_level = Level.parse(tokens[2])
		start_bg = parse_int_with_default(tokens[3], -1)
		adjustment_time = Range.parse_time(tokens[4], -1)
		end_time = Range.parse_time(tokens[5], -1)
		end_time_source = Source.parse(tokens[6])
		end_level = Level.parse(tokens[7])
		end_level_source = Source.parse(tokens[8])
		end_bg = parse_int_with_default(tokens[9], -1)
		

		# making range compliant

		if end_time != -1 and end_time < start_time:
			end_time += 24.

		range = Range(start = start_time, end = end_time)


		# making event_string

		event_string = ""

		if adjustment_time != -1:
			event_string = event_string + str(adjustment_time) + " "

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
			event_string = event_string + "at " + str(start_time) + " "	

		event_string = event_string + "and ending with a(n) " + str(end_level) + " blood glucose "		

		if end_bg != -1:
			event_string = event_string + "of " + str(end_bg) + " mg/dL "

		if end_time != -1:
			event_string = event_string + "at " + str(end_time) + " "	


		# printing alerts or raising exceptions in order to get more useful event entries

		printed_alert = False


		if event_type == EventType.UNKNOWN:
			raise Exception("The " + event_string + "has an unknown event type.")

		if start_time == -1: 
			raise Exception("The " + event_string + "has an unknown start time.")

		if start_level == Level.UNKNOWN and event_type == EventType.BOLUS:
			raise Exception("The " + event_string + "has an unknown start Level.")

		if start_bg == -1 and event_type == EventType.BOLUS and start_level == Level.IN_RANGE and end_level_source == Source.TEST:

			print("The " + event_string + "has an unknown start glucose.")
			print("")

			printed_alert = True

		if adjustment_time == -1 and (event_type == EventType.BOLUS or event_type == EventType.CORRECTION):
			raise Exception("The " + event_string + "has an unknown adjustment time.")

		if end_time == -1:
			raise Exception("The " + event_string + "has an unknown end time.")

		if adjustment_time != -1 and not range.contains_time(adjustment_time, True):
			raise Exception("The adjustment time of the " + event_string + "isn't a part of its range.")

		if end_time_source == Source.UNKNOWN:

			print("The " + event_string + "has an unknown end time source.")
			print("")

			printed_alert = True

			end_time_source = Source.TEST

		if end_level == Level.UNKNOWN:
			raise Exception("The " + event_string + "has an unknown end Level.")

		if end_level_source == Source.UNKNOWN:

			print("The " + event_string + "has an unknown end Level source.")
			print("")

			printed_alert = True

			end_level_source = Source.SENSOR

		if end_bg == -1 and \
		   event_type == EventType.BOLUS and start_level == Level.IN_RANGE and end_time - adjustment_time >= 2 and end_level_source == Source.TEST:

			print("The " + event_string + "has an unknown end glucose.")
			print("")

			printed_alert = True


		return Event( \
			uid = uid, \
			type = event_type, \
			start_level = start_level, \
			start_bg = start_bg, \
			adjustment_time = adjustment_time, \
			end_time_source = end_time_source, \
			end_level = end_level, \
			end_level_source = end_level_source, \
			end_bg = end_bg, \
			range = range, \
			printed_alert = printed_alert )



	def __hash__(self):
		return self.uid.__hash__()

	def __eq__(self, other):
		return self.uid.__eq__(other)