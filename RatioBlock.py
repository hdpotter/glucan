from dataclasses import dataclass
from Range import Range
from enum import Enum

class RatioType(Enum):
	SENSITIVITY = 0
	BASAL = 1
	CARB_RATIO = 2


@dataclass
class RatioBlock:
	uid: int
	range: Range
	ratio: float
	type: RatioType

	def __hash__(self):
		return hash(hash(self.uid) + hash(self.type))

	def __eq__(self, other):
		return self.uid == other.uid and self.type == other.type

