from dataclasses import dataclass
from math import modf

@dataclass
class Range_of_Time:
	start: float
	end: float

	def length(self):
		return self.end - self.start

	def timeshift(self, delta=24.):
		return Range_of_Time(self.start + delta, self.end + delta)

	def contains(self, other):
		return self.start <= other.start and self.end >= other.end

	# returns the size of the overlapping range of time
	def overlap(self, other):
		return Range_of_Time.overlap_no_wrap(self, other) \
			+ Range_of_Time.overlap_no_wrap(self.timeshift(), other) \
			+ Range_of_Time.overlap_no_wrap(self, other.timeshift())

	def touch(self, other):
		return Range_of_Time.overlap(self, other) > 0 or \
		       (Range_of_Time.overlap(self, other) == 0 and (self.start == other.end or other.start == self.end))

	@staticmethod
	def overlap_no_wrap(a, b):
		# no overlap
		if a.start >= b.end or b.start >= a.end:
			return 0

		# one range of time contains the other
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
		raise Exception("unhandled range of time overlap type: overlap(" + a + ", " + b + ")")

	def contains_time(self, time, inclusive):
		return Range_of_Time.contains_time_no_wrap(self, time, inclusive) or \
		       Range_of_Time.contains_time_no_wrap(self, time-24, inclusive) or Range_of_Time.contains_time_no_wrap(self, time+24, inclusive)

	@staticmethod
	def contains_time_no_wrap(range, time, inclusive):
		if inclusive:
			return time >= range.start and time <= range.end
		else:
			return time > range.start and time < range.end

	@staticmethod
	def time_str(time):

		whole_hours = int( modf(time) [1] )

		minutes = modf(time) [0] * 60
		whole_minutes = round( minutes )


		if whole_minutes == 60:
			whole_hours += 1
			whole_minutes = 0


		return str(whole_hours) + ":" + str(whole_minutes).zfill(2)


	def __str__(self):
		return "[" + Range_of_Time.time_str(self.start).rjust(5) + ", " + Range_of_Time.time_str(self.end).rjust(5) + "]"