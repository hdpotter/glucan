from dataclasses import dataclass
from Range import Range

@dataclass
class RatioBlock:
	range: Range
	ratio: float

