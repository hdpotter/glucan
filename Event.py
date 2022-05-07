from dataclasses import dataclass
from enum import Enum

from Range import Range

class EventType(Enum):
	INDEPENDENT = 0
	CORRECTION = 1
	BOLUS = 2

	@staticmethod
	def parse(string):
		if string == "independent":
			return EventType.INDEPENDENT
		if string == "correction":
			return EventType.CORRECTION
		if string == "bolus":
			return EventType.BOLUS
		raise Exception("unrecognized EventType " + string)

class LowNormalHigh(Enum):
	LOW = 0
	NORMAL = 1
	HIGH = 2
	UNKNOWN = 3

	@staticmethod
	def parse(string):
		if string == "low":
			return LowNormalHigh.LOW
		if string == "normal":
			return LowNormalHigh.NORMAL
		if string == "high":
			return LowNormalHigh.HIGH
		if string == "unknown" or string == "":
			return LowNormalHigh.UNKNOWN
		raise Exception("unrecognized LowNormalHigh " + string)


class Source(Enum):
	SENSOR = 0
	TEST = 1

	@staticmethod
	def parse(string):
		if string == "sensor":
			return Source.SENSOR
		if string == "test":
			return Source.TEST
		raise Exception("unrecognized Source " + string)


class Method(Enum):
	BASAL = 0
	SENSITIVITY = 1

	@staticmethod
	def parse(string):
		if string == "basal":
			return Method.BASAL
		if string == "sensitivity":
			return Method.SENSITIVITY
		raise Exception("unrecognized Method " + string)



@dataclass
class Event:
	uid: int
	type: EventType
	range: Range
	start_lnh: LowNormalHigh
	start_glucose: float
	end_lnh: LowNormalHigh
	end_glucose: float
	sensor_or_test: Source
	basal_or_sensitivity: Method

	@staticmethod
	def Parse(line, uid):
		tokens = line.split(",")

		# ensure correct length
		if(len(tokens) > 9):
			raise Exception("too many entries on line " + line + " of events")
		while len(tokens) < 9:
			tokens.append("")

		# parse fields
		event_type = EventType.parse(tokens[0])
		start_time = Range.parse_time(tokens[1])
		start_lnh = LowNormalHigh.parse(tokens[2])
		start_glucose = float(tokens[3])
		end_time = Range.parse_time(tokens[4])
		end_lnh = LowNormalHigh.parse(tokens[5])
		end_glucose = float(tokens[6])
		source = Source.parse(tokens[7])
		method = Method.parse(tokens[8])

		# make range compliant
		if(end_time < start_time):
			print("adding 24h to time because range contains midnight")
			time2 += 24.

		return Event( \
			uid = uid, \
			type = event_type, \
			start_lnh = start_lnh, \
			start_glucose = start_glucose, \
			end_lnh = end_lnh, \
			end_glucose = end_glucose, \
			sensor_or_test = source, \
			basal_or_sensitivity = method, \
			range = Range(start = start_time, end = end_time)
			)

	def __hash__(self):
		return self.uid.__hash__()

	def __eq__(self, other):
		return self.uid.__eq__(other)



