from calculate_contributions_from_auto_mode import calculate_contributions_from_auto_mode
from Event import EventType, Level
from parse_input import parse_events, parse_ratio_blocks
from Range_of_Time import Range_of_Time
from RatioBlock import RatioBlock, RatioType



# parsing input

events = parse_events("data/events.csv")

basals = parse_ratio_blocks("data/basals.csv", RatioType.BASAL)

carb_ratios = parse_ratio_blocks("data/carb_ratios.csv", RatioType.CARB_RATIO)



# making half hour blocks

half_hour_carb_ratios = []
uid = len(carb_ratios) + 1

for hh in range(0, 48):


	half_hour_range = Range_of_Time( \
		start = float(hh)/2., \
		end = float(hh)/2. + 0.5 )

	for block in basals:
		if Range_of_Time.overlap(block.range, half_hour_range) > 0:
			ratio = block.ratio


	half_hour_carb_ratios.append( RatioBlock( 
		uid = uid, 
		range = half_hour_range, 
		ratio = ratio, 
		type = RatioType.CARB_RATIO ) )


	uid += 1



# initializing intersections

carb_ratios_overlapping = {}

half_hour_carb_ratios_overlapping = {}
half_hour_carb_ratios_touching = {}


for event in events:

	carb_ratios_overlapping[event] = []

	half_hour_carb_ratios_overlapping[event] = []
	half_hour_carb_ratios_touching[event] = []



	# determining intersections

	for block in carb_ratios:
		if block.range.overlap(event.range) > 0:
			carb_ratios_overlapping[event].append(block)

	for block in half_hour_carb_ratios:
		if block.range.overlap(event.range) > 0:
			half_hour_carb_ratios_overlapping[event].append(block)
	for block in half_hour_carb_ratios:
		if block.range.touch(event.range) == True:
			half_hour_carb_ratios_touching[event].append(block)



# initializing contributions

fraction_contributions = {}

sufficiency_contributions = {}
on_the_half_hour_sufficiency_contributions = {}


for level in Level:
	if level == Level.UNKNOWN:
		continue

	fraction_contributions[level] = {}

	sufficiency_contributions[level] = {}
	on_the_half_hour_sufficiency_contributions[level] = {}


	for block in carb_ratios:
		fraction_contributions[level][block] = 0
		sufficiency_contributions[level][block] = 0

	for block in half_hour_carb_ratios:

		fraction_contributions[level][block] = 0

		sufficiency_contributions[level][block] = 0
		on_the_half_hour_sufficiency_contributions[level][block] = 0



# making lists of start times

carb_ratio_starts = []

for block in carb_ratios:
	carb_ratio_starts.append(block.range.start)



# summing contributions

for event in events:


	if(event.type == EventType.BOLUS):

		for block in carb_ratios_overlapping[event]:
			fraction_contributions[event.end_level][block] += calculate_contributions_from_auto_mode(event, block, False)[0]
			sufficiency_contributions[event.end_level][block] += calculate_contributions_from_auto_mode(event, block, False)[1]

		for block in half_hour_carb_ratios_overlapping[event]:

			fraction_contributions[event.end_level][block] += calculate_contributions_from_auto_mode(event, block, False)[0]

			sufficiency_contributions[event.end_level][block] += calculate_contributions_from_auto_mode(event, block, False)[1]
		for block in half_hour_carb_ratios_touching[event]:
			if event.adjustment_time not in carb_ratio_starts and \
			   (block.range.end == event.adjustment_time or block.range.end == event.adjustment_time - 24):
					on_the_half_hour_sufficiency_contributions[event.end_level][block] += calculate_contributions_from_auto_mode(event, block, True)[1]