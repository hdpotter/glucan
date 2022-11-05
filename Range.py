from dataclasses import dataclass
from math import modf

@dataclass
class Range:
	start: float
	end: float

	def length(self):
		return self.end - self.start

	def timeshift(self, delta=24.):
		return Range(self.start + delta, self.end + delta)

	def contains(self, other):
		return self.start <= other.start and self.end >= other.end

	# returns the size of the overlapping range
	def overlap(self, other):
		return Range.overlap_no_wrap(self, other) \
			+ Range.overlap_no_wrap(self.timeshift(), other) \
			+ Range.overlap_no_wrap(self, other.timeshift())

	@staticmethod
	def overlap_no_wrap(a, b):
		# no overlap
		if a.start >= b.end or b.start >= a.end:
			return 0

		# one range contains the other
		if a.contains(b):
			return b.length()
		if b.contains(a):
			return a.length()

		# overlap but one doesn't contain the other
		if a.start <= b.start:
			return a.end - b.start
		if b.start <= a.start:
			return b.end - a.start

		# leave this in here to catch if our logic above was wrong
		raise Exception("unhandled range overlap type: overlap(" + range1 + ", " + range2 + ")")

	def contains_time(self, time, inclusive):
		return Range.contains_time_no_wrap(self, time, inclusive) or Range.contains_time_no_wrap(self, time+24, inclusive)

	@staticmethod
	def contains_time_no_wrap(range, time, inclusive):
                if inclusive:
                        return time >= range.start and time <= range.end
                else:
                        return time > range.start and time < range.end

	
	

	@staticmethod
	def time_string(time):
		hours = modf(time)[1]
		hourFrac = modf(time)[0]

		minutes = modf(hourFrac*60)[1]
		minuteFrac = modf(hourFrac*60)[0]

		seconds = modf(minuteFrac*60)[1]

		# we might get a tiny fraction of a second from floating point error, so ignore it
		if seconds <= 0.01 or seconds >= 59.99:
			return str(int(hours)) + ":" + str(int(minutes)).zfill(2)
		else:
			return str(int(hours)) + ":" + str(int(minutes)).zfill(2) + ":" + str(seconds)

	def __str__(self):
		return "[" + Range.time_string(self.start).rjust(5) + ", " + Range.time_string(self.end).rjust(5) + "]"

	@staticmethod
	def parse_time(timeString):
		tokens = timeString.split(":")

		if len(tokens) != 2:
			raise Exception("time format is hh:mm, 24h time")

		hours = int(tokens[0])
		minutes = int(tokens[1])

		return float(hours) + float(minutes)/60.



# range = Range(0, 1)
# print(range.timeshift())
