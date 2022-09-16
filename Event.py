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
	OUT_OF_RANGE = 4

	@staticmethod
	def parse(string):
		if string == "in range":
			return LowNormalHigh.NORMAL
		if string == "out of range":
			return LowNormalHigh.OUT_OF_RANGE
		if string == "low":
			return LowNormalHigh.LOW
		if string == "high":
			return LowNormalHigh.HIGH
		if string == "unknown" or string == "":
			return LowNormalHigh.UNKNOWN
		raise Exception("unrecognized LowNormalHigh " + string)

	def __str__(self):
		if self == LowNormalHigh.OUT_OF_RANGE:
			return "out of range"
		if self == LowNormalHigh.LOW:
			return "low"
		if self == LowNormalHigh.NORMAL:
			return "normal"
		if self == LowNormalHigh.HIGH:
			return "high"
		if self == LowNormalHigh.UNKNOWN:
			return "unknown"

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


def parse_float_with_default(string, default):
	try:
		return float(string)
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
	start_glucose: float
	adjustment_time: float
	end_lnh: LowNormalHigh
	end_glucose: float
	source: Source
	
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
		start_glucose = parse_float_with_default(tokens[3], -1)
		adjustment_time = parse_time_with_default(tokens[4], -1)
		end_time = Range.parse_time(tokens[5])
		end_lnh = LowNormalHigh.parse(tokens[6])
		end_glucose = parse_float_with_default(tokens[7], -1)
		source = Source.parse(tokens[8])
	
		# make range compliant
		if(end_time < start_time):
			print("adding 24h to time because range contains midnight")
			end_time += 24.

		range = Range(start = start_time, end = end_time)
		
		if adjustment_time >= 0 and not range.contains_time(adjustment_time, True):
			raise Exception("adjustment time is not within time range")

		return Event( \
			uid = uid, \
			type = event_type, \
			start_lnh = start_lnh, \
			start_glucose = start_glucose, \
			adjustment_time = adjustment_time, \
			end_lnh = end_lnh, \
			end_glucose = end_glucose, \
			source = source, \
			range = range
			)

	def __hash__(self):
		return self.uid.__hash__()

	def __eq__(self, other):
		return self.uid.__eq__(other)



