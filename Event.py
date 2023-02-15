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



class LowNormalHigh(Enum):
	LOW = 0
	NORMAL = 1
	HIGH = 2
	UNKNOWN = 3


	@staticmethod
	def parse(string):
		if string == "low":
			return LowNormalHigh.LOW
		elif string == "in range":
			return LowNormalHigh.NORMAL
		elif string == "high":
			return LowNormalHigh.HIGH
		else:
			return LowNormalHigh.UNKNOWN


	def __str__(self):
		if self == LowNormalHigh.LOW:
			return "low"
		if self == LowNormalHigh.NORMAL:
			return "in range"
		if self == LowNormalHigh.HIGH:
			return "high"
		if self == LowNormalHigh.UNKNOWN:
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

def parse_time_with_default(string, default):
	try:
		return Range.parse_time(string)
	except:
		return default



@dataclass
class Event:
	uid: int
	type: EventType
	range: Range
	start_lnh: LowNormalHigh
	start_bg: int
	adjustment_time: float
	end_time_source: Source
	end_lnh: LowNormalHigh
	end_lnh_source: Source
	end_bg: int
	printed_alert: bool


	@staticmethod
	def Parse(line, uid):

		tokens = line.split(",")

		if(len(tokens) != 10):
			raise Exception("Line " + line + " of events.csv doesn't have ten entries.")

		# ensuring empty columns after the final entry in a line are parsed
		while len(tokens) < 10:
			tokens.append("")


		# parsing entries
		event_type = EventType.parse(tokens[0])
		start_time = parse_time_with_default(tokens[1], -1)
		start_lnh = LowNormalHigh.parse(tokens[2])
		start_bg = parse_int_with_default(tokens[3], -1)
		adjustment_time = parse_time_with_default(tokens[4], -1)
		end_time = parse_time_with_default(tokens[5], -1)
		end_time_source = Source.parse(tokens[6])
		end_lnh = LowNormalHigh.parse(tokens[7])
		end_lnh_source = Source.parse(tokens[8])
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

		event_string = event_string + "starting with a(n) " + str(start_lnh) + " blood glucose "

		if start_bg != -1:
			event_string = event_string + "of " + str(start_bg) + " mg/dL "

		if start_time != -1:
			event_string = event_string + "at " + str(start_time) + " "	

		event_string = event_string + "and ending with a(n) " + str(end_lnh) + " blood glucose "		

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

		if start_lnh == LowNormalHigh.UNKNOWN and event_type == EventType.BOLUS:
			raise Exception("The " + event_string + "has an unknown start LowNormalHigh.")

		if start_bg == -1 and event_type == EventType.BOLUS and start_lnh == LowNormalHigh.NORMAL and end_lnh_source == Source.TEST:

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

		if end_lnh == LowNormalHigh.UNKNOWN:
			raise Exception("The " + event_string + "has an unknown end LowNormalHigh.")

		if end_lnh_source == Source.UNKNOWN:

			print("The " + event_string + "has an unknown end LowNormalHigh source.")
			print("")

			printed_alert = True

			end_lnh_source = Source.SENSOR

		if end_bg == -1 and event_type == EventType.BOLUS and start_lnh == LowNormalHigh.NORMAL and end_lnh_source == Source.TEST:

			print("The " + event_string + "has an unknown end glucose.")
			print("")

			printed_alert = True


		return Event( \
			uid = uid, \
			type = event_type, \
			start_lnh = start_lnh, \
			start_bg = start_bg, \
			adjustment_time = adjustment_time, \
			end_time_source = end_time_source, \
			end_lnh = end_lnh, \
			end_lnh_source = end_lnh_source, \
			end_bg = end_bg, \
			range = range, \
			printed_alert = printed_alert )



	def __hash__(self):
		return self.uid.__hash__()

	def __eq__(self, other):
		return self.uid.__eq__(other)