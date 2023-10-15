from dataclasses import dataclass
from enum import Enum

from Range_of_Time import Range_of_Time



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



@dataclass
class Event:
	uid: int
	type: EventType
	range: Range_of_Time
	start_level: Level
	start_bg: int
	adjustment_time: float
	end_time_source: Source
	end_level: Level
	end_level_source: Source
	end_bg: int


	def __hash__(self):
		return self.uid.__hash__()

	def __eq__(self, other):
		return self.uid.__eq__(other)