from dataclasses import dataclass
from enum import Enum

from Range_of_Time import Range_of_Time


class RatioType(Enum):
	ACTIVE_INSULIN_TIME = 0
	BASAL = 1
	CARB_RATIO = 2
	SENSITIVITY = 3


@dataclass
class RatioBlock:
	uid: int
	range: Range_of_Time
	ratio: float
	type: RatioType

	def __hash__(self):
		return hash(hash(self.uid) + hash(self.type))

	def __eq__(self, other):
		return self.uid == other.uid and self.type == other.type