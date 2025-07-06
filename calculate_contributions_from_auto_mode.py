from Event import EventType, Level, Source
from RatioBlock import RatioType


def calculate_contributions_from_auto_mode(event, block, inclusive):


	if event.type == EventType.BOLUS and block.type == RatioType.CARB_RATIO and \
	   block.range.contains_time(event.adjustment_time, inclusive) and \
	   event.start_level == Level.IN_RANGE:


			fraction = 1./2.

			if event.end_level_source != Source.TEST:
				fraction *= 1./3.


			if event.end_level_source == Source.TEST:
				sufficiency_for_changing_carb_ratios = 1/2
			else:
				sufficiency_for_changing_carb_ratios = 0


	else:

		fraction = 0
		sufficiency_for_changing_carb_ratios = 0


	return (fraction, sufficiency_for_changing_carb_ratios)