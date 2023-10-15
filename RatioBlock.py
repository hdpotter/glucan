from dataclasses import dataclass
from enum import Enum

from Range_of_Time import Range_of_Time


class RatioType(Enum):
	BASAL = 0
	CARB_RATIO = 1
	SENSITIVITY = 2


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