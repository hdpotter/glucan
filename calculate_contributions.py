from Event import EventType, Level, Source
from RatioBlock import RatioType


def calculate_contributions(event, block, inclusive):


	overlap = block.range.overlap(event.range)
	fraction = overlap / event.range.length()

	sufficiency_for_changing_basals = 0
	sufficiency_for_changing_carb_ratios = 0
	sufficiency_for_changing_sensitivities = 0


	if event.type == EventType.INDEPENDENT:
		if block.type == RatioType.BASAL:

			if block.range.contains_time(event.range.end, inclusive) and \
			   event.end_time_source == Source.SENSOR and event.end_level_source == Source.TEST:
					sufficiency_for_changing_basals = 1/2

		else:
			fraction = 0


	elif event.type == EventType.BOLUS:

		if block.type == RatioType.BASAL:
			fraction *= 1./2.  

		elif block.type == RatioType.CARB_RATIO:
			if block.range.contains_time(event.adjustment_time, inclusive):
				if event.start_level == Level.IN_RANGE:
					fraction = 1./2.

					if event.end_level_source == Source.TEST:
						sufficiency_for_changing_carb_ratios = 1/2

				elif (event.start_level == Level.LOW or event.start_level == Level.HIGH):
					fraction = 1./4.
				else:
					fraction = 0
			else:
				fraction = 0

		elif block.type == RatioType.SENSITIVITY:
			if block.range.contains_time(event.adjustment_time, inclusive) and \
			   (event.start_level == Level.LOW or event.start_level == Level.HIGH):
					fraction = 1./4.
			else:
				fraction = 0

		else:
			fraction = 0


	elif event.type == EventType.CORRECTION:

		if block.type == RatioType.BASAL:
			fraction *= 1./2.

		elif block.type == RatioType.SENSITIVITY:
			if block.range.contains_time(event.adjustment_time, inclusive):
				fraction = 1./2.

				if event.end_level_source == Source.TEST:
					sufficiency_for_changing_sensitivities = 1/2

			else:
				fraction = 0

		else:
			fraction = 0


	else:
		fraction = 0


	if event.end_level_source != Source.TEST:
		fraction *= 1./3.

	return (fraction, sufficiency_for_changing_basals, sufficiency_for_changing_carb_ratios, sufficiency_for_changing_sensitivities)