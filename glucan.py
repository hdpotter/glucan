from enum import Enum
from pickle import FALSE

from parse_input import *
from RatioBlock import *
from Event import *


def calculate_fraction(event, block):
	overlap = block.range.overlap(event.range)
	fraction = overlap / event.range.length()
	sufficiency_for_changing_basals = 0
	sufficiency_for_changing_carb_ratios = 0
	sufficiency_for_changing_sensitivities = 0

	if event.type == EventType.INDEPENDENT:
		if block.type == RatioType.BASAL:
			if block.range.contains_time(event.range.end, False):
				sufficiency_for_changing_basals = 1/2
		else:
			fraction = 0

	elif event.type == EventType.BOLUS:
		if block.type == RatioType.BASAL:
			fraction *= 1./2.  
		if block.type == RatioType.CARB_RATIO:
			if block.range.contains_time(event.adjustment_time, False):
				if event.start_lnh == LowNormalHigh.NORMAL:
					fraction = 1./2.
					sufficiency_for_changing_carb_ratios = 1/2
				elif (event.start_lnh == LowNormalHigh.OUT_OF_RANGE or \
				      event.start_lnh == LowNormalHigh.LOW or event.start_lnh == LowNormalHigh.HIGH):
					fraction = 1./4.
				else:
					fraction = 0
			else:
				fraction = 0
		if block.type == RatioType.SENSITIVITY:
			if block.range.contains_time(event.adjustment_time, False) and \
			   (event.start_lnh == LowNormalHigh.OUT_OF_RANGE or \
			    event.start_lnh == LowNormalHigh.LOW or event.start_lnh == LowNormalHigh.HIGH):
					fraction = 1./4.
			else:
				fraction = 0
		if block.type != RatioType.BASAL and block.type != RatioType.CARB_RATIO and block.type != RatioType.SENSITIVITY:
			fraction = 0

	elif event.type == EventType.CORRECTION:
		if block.type == RatioType.BASAL:
			fraction *= 1./2.
		elif block.type == RatioType.SENSITIVITY:
			if block.range.contains_time(event.adjustment_time, False):
				fraction = 1./2.
				sufficiency_for_changing_sensitivities = 1/2
			else:
				fraction = 0
		else:
			fraction = 0

	else:
		fraction = 0

	if event.source == Source.SENSOR:
		fraction *= 1./3.
		sufficiency_for_changing_basals = 0
		sufficiency_for_changing_carb_ratios = 0
		sufficiency_for_changing_sensitivities = 0

	return (fraction, sufficiency_for_changing_basals, sufficiency_for_changing_carb_ratios, sufficiency_for_changing_sensitivities)


def print_and_analyze_block_contributions(block, half_hours, block_is_a_ratio_block, events):


	block_has_sufficienct_events = sufficiency_contributions[LowNormalHigh.LOW][block] >= 1 or \
	                               sufficiency_contributions[LowNormalHigh.NORMAL][block] >= 1 or \
	                               sufficiency_contributions[LowNormalHigh.HIGH][block] >= 1

	block_has_no_contributions = fraction_contributions[LowNormalHigh.LOW][block] == 0 and \
	                             fraction_contributions[LowNormalHigh.NORMAL][block] == 0 and \
	                             fraction_contributions[LowNormalHigh.HIGH][block] == 0


	if block_is_a_ratio_block:
		block_string = "   "
	else:
		block_string = "         "

	block_string = block_string + str(block.range) 
	
	if block_is_a_ratio_block:

		if (block.type == RatioType.CARB_RATIO and block.ratio >= 10) or block.type == RatioType.SENSITIVITY:
			ratio = int(block.ratio)
		else:
			ratio = block.ratio

		block_string = block_string + " = " + str(ratio)

	block_string = block_string + ":"

	if block_is_a_ratio_block:
		print(block_string)

		if block_has_sufficienct_events == False:
			print("")

	elif block_has_no_contributions == False:
		print(block_string)


	if (block_is_a_ratio_block and block_has_sufficienct_events) or \
	   (block_is_a_ratio_block == False and block_has_no_contributions == False):


		for lnh in LowNormalHigh:
			if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
				continue

			if block_is_a_ratio_block:
				contributions_string = "      "
			else:
				contributions_string = "            "

			contributions_string = contributions_string + str(lnh) + ": " + str(fraction_contributions[lnh][block])

			if sufficiency_contributions[lnh][block] >= 1:
				contributions_string = contributions_string + "   Sufficient Events"
			elif block_is_a_ratio_block == False and sufficiency_contributions[lnh][block] == 1/2:
				contributions_string = contributions_string + "   half sufficient event"

			print(contributions_string)		


		if fraction_contributions[LowNormalHigh.NORMAL][block] <= fraction_contributions[LowNormalHigh.LOW][block] and \
		   fraction_contributions[LowNormalHigh.HIGH][block] < fraction_contributions[LowNormalHigh.LOW][block]:

			if sufficiency_contributions[LowNormalHigh.LOW][block] >= 1 and \
			   (fraction_contributions[LowNormalHigh.HIGH][block] == 0 or \
			    (fraction_contributions[LowNormalHigh.HIGH][block] > 0 and \
			     fraction_contributions[LowNormalHigh.LOW][block]/fraction_contributions[LowNormalHigh.HIGH][block] >= 3)):
					print("=> LOW")

			if fraction_contributions[LowNormalHigh.HIGH][block] > 0:

				if block_is_a_ratio_block:
					fraction_string = "      => -"
				else:
					fraction_string = "            => -"

				fraction_string = fraction_string + \
				                  str(fraction_contributions[LowNormalHigh.LOW][block]/fraction_contributions[LowNormalHigh.HIGH][block])

				print(fraction_string)

		if fraction_contributions[LowNormalHigh.LOW][block] < fraction_contributions[LowNormalHigh.NORMAL][block] and \
		   fraction_contributions[LowNormalHigh.HIGH][block] < fraction_contributions[LowNormalHigh.NORMAL][block]:

			if sufficiency_contributions[LowNormalHigh.NORMAL][block] >= 1:
					print("=> NORMAL")

		if fraction_contributions[LowNormalHigh.LOW][block] < fraction_contributions[LowNormalHigh.HIGH][block] and \
		   fraction_contributions[LowNormalHigh.NORMAL][block] <= fraction_contributions[LowNormalHigh.HIGH][block]:

			if sufficiency_contributions[LowNormalHigh.HIGH][block] >= 1 and \
			   (fraction_contributions[LowNormalHigh.LOW][block] == 0 or \
			    (fraction_contributions[LowNormalHigh.LOW][block] > 0 and \
			     fraction_contributions[LowNormalHigh.HIGH][block]/fraction_contributions[LowNormalHigh.LOW][block] >= 3)):
					print("=> HIGH")

			if fraction_contributions[LowNormalHigh.LOW][block] > 0:

				if block_is_a_ratio_block:
					fraction_string = "      => +"
				else:
					fraction_string = "            => +"

				fraction_string = fraction_string + \
				                  str(fraction_contributions[LowNormalHigh.HIGH][block]/fraction_contributions[LowNormalHigh.LOW][block])

				print(fraction_string)


		if block_is_a_ratio_block:

			print_and_analyze_half_hour_block_contributions(block, half_hours, events)
			print("")

		else:

			printed_half_hour = False

			for lnh in LowNormalHigh:
				if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
					continue

				if on_the_half_hour_sufficiency_contributions[lnh][block.range.end] >= 1:

					if printed_half_hour == False:
						print("         " + Range.time_string(block.range.end) + ":")
						printed_half_hour == True

					print("            " + str(lnh) + " -------------------   Sufficient Events")

				elif on_the_half_hour_sufficiency_contributions[lnh][block.range.end] == 1/2:

					if printed_half_hour == False:
						print("         " + Range.time_string(block.range.end) + ":")
						printed_half_hour == True

					print("            " + str(lnh) + " -------------------   half sufficient event")


def print_and_analyze_half_hour_block_contributions(block, half_hours, events):

	for half_hour_block in half_hours:

			if block.range.overlap(half_hour_block.range) > 0 and block.range.end - block.range.start > 0.5:
				print_and_analyze_block_contributions(half_hour_block, half_hours, False, events)
			

print("****************************************************************************************************")
print("This software is an experimental tool.")
print("The author makes no guarantees about the correctness of its outputs or its suitability for any task.")
print("****************************************************************************************************")
print("")
print("")

# initialize blocks

basals = parse_ratios("data/basals.csv", RatioType.BASAL)

half_hour_basals = []
uid = len(basals) + 1
for hh in range(0, 48):
	half_hour_basals.append(RatioBlock(
		uid = uid, 
		range = Range(start = float(hh)/2., end = float(hh)/2. + 0.5),
	ratio = -1, # EDIT LATER!
		type = RatioType.BASAL))
	uid += 1


carb_ratios = parse_ratios("data/carb_ratios.csv", RatioType.CARB_RATIO)

half_hour_carb_ratios = []
uid = len(carb_ratios) + 1
for hh in range(0, 48):
	half_hour_carb_ratios.append(RatioBlock(
		uid = uid, 
		range = Range(start = float(hh)/2., end = float(hh)/2. + 0.5),
	ratio = -1, # EDIT LATER!
		type = RatioType.CARB_RATIO))
	uid += 1


sensitivities = parse_ratios("data/sensitivities.csv", RatioType.SENSITIVITY)

half_hour_sensitivities = []
uid = len(sensitivities) + 1
for hh in range(0, 48):
	half_hour_sensitivities.append(RatioBlock(
		uid = uid, 
		range = Range(start = float(hh)/2., end = float(hh)/2. + 0.5),
	ratio = -1, # EDIT LATER!
		type = RatioType.SENSITIVITY))
	uid += 1


events = parse_events("data/events.csv")


# initialize intersections

basals_impacting = {}
half_hour_basals_impacting = {}

carb_ratios_impacting = {}
half_hour_carb_ratios_impacting = {}

sensitivities_impacting = {}
half_hour_sensitivities_impacting = {}


# calculate intersections
for event in events:

	basals_impacting[event] = []
	half_hour_basals_impacting[event] = []

	carb_ratios_impacting[event] = []
	half_hour_carb_ratios_impacting[event] = []

	sensitivities_impacting[event] = []
	half_hour_sensitivities_impacting[event] = []


	for block in basals:
		if block.range.overlap(event.range) > 0:
			basals_impacting[event].append(block)

	for block in half_hour_basals:
		if block.range.overlap(event.range) > 0:
			half_hour_basals_impacting[event].append(block)


	for block in carb_ratios:
		if block.range.overlap(event.range) > 0:
			carb_ratios_impacting[event].append(block)

	for block in half_hour_carb_ratios:
		if block.range.overlap(event.range) > 0:
			half_hour_carb_ratios_impacting[event].append(block)


	for block in sensitivities:
		if block.range.overlap(event.range) > 0:
			sensitivities_impacting[event].append(block)

	for block in half_hour_sensitivities:
		if block.range.overlap(event.range) > 0:
			half_hour_sensitivities_impacting[event].append(block)


# initialize contributions

fraction_contributions = {}

sufficiency_contributions = {}
on_the_half_hour_sufficiency_contributions = {}


for lnh in LowNormalHigh:

	fraction_contributions[lnh] = {}

	sufficiency_contributions[lnh] = {}
	on_the_half_hour_sufficiency_contributions[lnh] = {}


	for block in basals:
		fraction_contributions[lnh][block] = 0
		sufficiency_contributions[lnh][block] = 0

	for block in half_hour_basals:

		fraction_contributions[lnh][block] = 0

		sufficiency_contributions[lnh][block] = 0
		on_the_half_hour_sufficiency_contributions[lnh][block.range.end] = 0


	for block in carb_ratios:
		fraction_contributions[lnh][block] = 0
		sufficiency_contributions[lnh][block] = 0

	for block in half_hour_carb_ratios:

		fraction_contributions[lnh][block] = 0

		sufficiency_contributions[lnh][block] = 0
		on_the_half_hour_sufficiency_contributions[lnh][block.range.end] = 0


	for block in sensitivities:
		fraction_contributions[lnh][block] = 0
		sufficiency_contributions[lnh][block] = 0

	for block in half_hour_sensitivities:

		fraction_contributions[lnh][block] = 0

		sufficiency_contributions[lnh][block] = 0
		on_the_half_hour_sufficiency_contributions[lnh][block.range.end] = 0


# calculate contributions
for event in events:


	for block in basals_impacting[event]:
		fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
		sufficiency_contributions[event.end_lnh][block] += calculate_fraction(event, block)[1]

	for block in half_hour_basals_impacting[event]:

		fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]

		sufficiency_contributions[event.end_lnh][block] += calculate_fraction(event, block)[1]
		if (block.range.end == event.range.end or block.range.end == event.range.end - 24) and event.source == Source.TEST:
			on_the_half_hour_sufficiency_contributions[event.end_lnh][block.range.end] += 1/2


	if(event.type == EventType.BOLUS):

		for block in carb_ratios_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			sufficiency_contributions[event.end_lnh][block] += calculate_fraction(event, block)[2]

		for block in half_hour_carb_ratios_impacting[event]:

			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]

			sufficiency_contributions[event.end_lnh][block] += calculate_fraction(event, block)[2]
			if (block.range.end == event.range.end or block.range.end == event.range.end - 24) and event.source == Source.TEST:
				on_the_half_hour_sufficiency_contributions[event.end_lnh][block.range.end] += 1/2


	if(event.type == EventType.CORRECTION or event.type == EventType.BOLUS):

		for block in sensitivities_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			sufficiency_contributions[event.end_lnh][block] += calculate_fraction(event, block)[3]

		for block in half_hour_sensitivities_impacting[event]:

			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]

			sufficiency_contributions[event.end_lnh][block] += calculate_fraction(event, block)[3]
			if (block.range.end == event.range.end or block.range.end == event.range.end - 24) and event.source == Source.TEST:
				on_the_half_hour_sufficiency_contributions[event.end_lnh][block.range.end] += 1/2


# print and analyze contributions

print("basals:")
print("")
for block in basals:
	print_and_analyze_block_contributions(block, half_hour_basals, True, events)

print("")
print("")

print("carb ratios:")
print("")
for block in carb_ratios:
	print_and_analyze_block_contributions(block, half_hour_carb_ratios, True, events)

print("")
print("")

print("sensitivities:")
print("")
for block in sensitivities:
	print_and_analyze_block_contributions(block, half_hour_sensitivities, True, events)

print("")
print("")