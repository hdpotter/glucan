from calculate_contributions import calculate_contributions
from Event import EventType, Level
from parse_input import parse_events, parse_ratio_blocks
from Range import Range
from RatioBlock import RatioBlock, RatioType



# parsing input

events = parse_events("data/events.csv")

basals = parse_ratio_blocks("data/basals.csv", RatioType.BASAL)

carb_ratios = parse_ratio_blocks("data/carb_ratios.csv", RatioType.CARB_RATIO)

sensitivities = parse_ratio_blocks("data/sensitivities.csv", RatioType.SENSITIVITY)



# making half hour blocks

half_hour_basals = []
uid = len(basals) + 1

for hh in range(0, 48):


	half_hour_range = Range( \
		start = float(hh)/2., \
		end = float(hh)/2. + 0.5 )

	for block in basals:
		if Range.overlap(block.range, half_hour_range) > 0:
			ratio = block.ratio


	half_hour_basals.append( RatioBlock( 
		uid = uid, 
		range = half_hour_range, 
		ratio = ratio, 
		type = RatioType.BASAL ) )


	uid += 1


half_hour_carb_ratios = []
uid = len(carb_ratios) + 1

for hh in range(0, 48):


	half_hour_range = Range( \
		start = float(hh)/2., \
		end = float(hh)/2. + 0.5 )

	for block in basals:
		if Range.overlap(block.range, half_hour_range) > 0:
			ratio = block.ratio


	half_hour_basals.append( RatioBlock( 
		uid = uid, 
		range = half_hour_range, 
		ratio = ratio, 
		type = RatioType.CARB_RATIO ) )


	uid += 1


half_hour_sensitivities = []
uid = len(sensitivities) + 1

for hh in range(0, 48):


	half_hour_range = Range( \
		start = float(hh)/2., \
		end = float(hh)/2. + 0.5 )

	for block in basals:
		if Range.overlap(block.range, half_hour_range) > 0:
			ratio = block.ratio


	half_hour_basals.append( RatioBlock( 
		uid = uid, 
		range = half_hour_range, 
		ratio = ratio, 
		type = RatioType.SENSITIVITY ) )


	uid += 1



# initializing intersections

basals_overlapping = {}

half_hour_basals_overlapping = {}
half_hour_basals_touching = {}


carb_ratios_overlapping = {}

half_hour_carb_ratios_overlapping = {}
half_hour_carb_ratios_touching = {}


sensitivities_overlapping = {}

half_hour_sensitivities_overlapping = {}
half_hour_sensitivities_touching = {}


for event in events:

	basals_overlapping[event] = []

	half_hour_basals_overlapping[event] = []
	half_hour_basals_touching[event] = []


	carb_ratios_overlapping[event] = []

	half_hour_carb_ratios_overlapping[event] = []
	half_hour_carb_ratios_touching[event] = []


	sensitivities_overlapping[event] = []

	half_hour_sensitivities_overlapping[event] = []
	half_hour_sensitivities_touching[event] = []



	# determining intersections

	for block in basals:
		if block.range.overlap(event.range) > 0:
			basals_overlapping[event].append(block)

	for block in half_hour_basals:
		if block.range.overlap(event.range) > 0:
			half_hour_basals_overlapping[event].append(block)
	for block in half_hour_basals:
		if block.range.touch(event.range) == True:
			half_hour_basals_touching[event].append(block)


	for block in carb_ratios:
		if block.range.overlap(event.range) > 0:
			carb_ratios_overlapping[event].append(block)

	for block in half_hour_carb_ratios:
		if block.range.overlap(event.range) > 0:
			half_hour_carb_ratios_overlapping[event].append(block)
	for block in half_hour_carb_ratios:
		if block.range.touch(event.range) == True:
			half_hour_carb_ratios_touching[event].append(block)


	for block in sensitivities:
		if block.range.overlap(event.range) > 0:
			sensitivities_overlapping[event].append(block)

	for block in half_hour_sensitivities:
		if block.range.overlap(event.range) > 0:
			half_hour_sensitivities_overlapping[event].append(block)
	for block in half_hour_sensitivities:
		if block.range.touch(event.range) == True:
			half_hour_sensitivities_touching[event].append(block)



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


	for block in basals:
		fraction_contributions[level][block] = 0
		sufficiency_contributions[level][block] = 0

	for block in half_hour_basals:

		fraction_contributions[level][block] = 0

		sufficiency_contributions[level][block] = 0
		on_the_half_hour_sufficiency_contributions[level][block] = 0


	for block in carb_ratios:
		fraction_contributions[level][block] = 0
		sufficiency_contributions[level][block] = 0

	for block in half_hour_carb_ratios:

		fraction_contributions[level][block] = 0

		sufficiency_contributions[level][block] = 0
		on_the_half_hour_sufficiency_contributions[level][block] = 0


	for block in sensitivities:
		fraction_contributions[level][block] = 0
		sufficiency_contributions[level][block] = 0

	for block in half_hour_sensitivities:

		fraction_contributions[level][block] = 0

		sufficiency_contributions[level][block] = 0
		on_the_half_hour_sufficiency_contributions[level][block] = 0



# making lists of start times

basal_starts = []

for block in basals:
	basal_starts.append(block.range.start)


carb_ratio_starts = []

for block in carb_ratios:
	carb_ratio_starts.append(block.range.start)


sensitivity_starts = []

for block in sensitivities:
	sensitivity_starts.append(block.range.start)



# summing contributions

for event in events:


	for block in basals_overlapping[event]:
		fraction_contributions[event.end_level][block] += calculate_contributions(event, block, False)[0]
		sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, False)[1]

	for block in half_hour_basals_overlapping[event]:

		fraction_contributions[event.end_level][block] += calculate_contributions(event, block, False)[0]

		sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, False)[1]
	for block in half_hour_basals_touching[event]:
		if event.range.end not in basal_starts and \
		   (block.range.end == event.range.end or block.range.end == event.range.end - 24):
				on_the_half_hour_sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, True)[1]


	if(event.type == EventType.BOLUS):

		for block in carb_ratios_overlapping[event]:
			fraction_contributions[event.end_level][block] += calculate_contributions(event, block, False)[0]
			sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, False)[2]

		for block in half_hour_carb_ratios_overlapping[event]:

			fraction_contributions[event.end_level][block] += calculate_contributions(event, block, False)[0]

			sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, False)[2]
		for block in half_hour_carb_ratios_touching[event]:
			if event.adjustment_time not in carb_ratio_starts and \
			   (block.range.end == event.adjustment_time or block.range.end == event.adjustment_time - 24):
					on_the_half_hour_sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, True)[2]


	if(event.type == EventType.CORRECTION or event.type == EventType.BOLUS):

		for block in sensitivities_overlapping[event]:
			fraction_contributions[event.end_level][block] += calculate_contributions(event, block, False)[0]
			sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, False)[3]

		for block in half_hour_sensitivities_overlapping[event]:

			fraction_contributions[event.end_level][block] += calculate_contributions(event, block, False)[0]

			sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, False)[3]
		for block in half_hour_sensitivities_touching[event]:
			if event.adjustment_time not in sensitivity_starts and \
			   (block.range.end == event.adjustment_time or block.range.end == event.adjustment_time - 24):
					on_the_half_hour_sufficiency_contributions[event.end_level][block] += calculate_contributions(event, block, True)[3]