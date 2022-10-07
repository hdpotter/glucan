from enum import Enum

from parse_input import *
from RatioBlock import *
from Event import *


def calculate_fraction(event, block):
	overlap = block.range.overlap(event.range)
	fraction = overlap / event.range.length()
	sufficient_basal_data = 0
	sufficient_sensitivity_data = 0
	sufficient_carb_ratio_data = 0

	if event.type == EventType.INDEPENDENT:
		if block.type == RatioType.BASAL:
			if block.range.contains_time(event.range.end, False):
				sufficient_basal_data = 1
		else:
			fraction = 0

	elif event.type == EventType.BOLUS:
		if block.type == RatioType.BASAL:
			fraction *= 1./2.  
		if block.type == RatioType.CARB_RATIO:
			if block.range.contains_time(event.adjustment_time, False):
				if event.start_lnh == LowNormalHigh.NORMAL:
					fraction = 1./2.
					sufficient_carb_ratio_data = 1
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
				sufficient_sensitivity_data = 1
			else:
				fraction = 0
		else:
			fraction = 0

	else:
		fraction = 0

	if event.source == Source.SENSOR:
		fraction *= 1./3.
		sufficient_basal_data = 0
		sufficient_carb_ratio_data = 0
		sufficient_sensitivity_data = 0

	return (fraction, sufficient_basal_data, sufficient_carb_ratio_data, sufficient_sensitivity_data)


def print_and_analyze_block_contributions(block, half_hours, block_is_not_an_element_of_half_hours, events):

	block_has_no_contributions = fraction_contributions[LowNormalHigh.LOW][block] == 0 and \
	                             fraction_contributions[LowNormalHigh.NORMAL][block] == 0 and \
	                             fraction_contributions[LowNormalHigh.HIGH][block] == 0
	if block_has_no_contributions == False:


		if block_is_not_an_element_of_half_hours:
			block_string = "   "
		else:
			block_string = "         "

		block_string = block_string + str(block.range) + ":"

		print(block_string)


		for lnh in LowNormalHigh:
			if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
				continue

			if block_is_not_an_element_of_half_hours:
				contributions_string = "      "
			else:
				contributions_string = "            "

			contributions_string = contributions_string + str(lnh) + ": " + str(fraction_contributions[lnh][block])

			if sufficient_data_contributions[lnh][block] >= 2:
				contributions_string = contributions_string + "   Sufficient Data"

			print(contributions_string)		


		if fraction_contributions[LowNormalHigh.NORMAL][block] <= fraction_contributions[LowNormalHigh.LOW][block] and \
		   fraction_contributions[LowNormalHigh.HIGH][block] < fraction_contributions[LowNormalHigh.LOW][block]:

			if sufficient_data_contributions[LowNormalHigh.LOW][block] >= 2 and \
			   (fraction_contributions[LowNormalHigh.HIGH][block] == 0 or \
			    (fraction_contributions[LowNormalHigh.HIGH][block] > 0 and \
			     fraction_contributions[LowNormalHigh.LOW][block]/fraction_contributions[LowNormalHigh.HIGH][block] >= 3)):
					print("=> LOW")

			if fraction_contributions[LowNormalHigh.HIGH][block] > 0:

				if block_is_not_an_element_of_half_hours:
					fraction_string = "      => -"
				else:
					fraction_string = "            => -"

				fraction_string = fraction_string + \
				                  str(fraction_contributions[LowNormalHigh.LOW][block]/fraction_contributions[LowNormalHigh.HIGH][block])

				print(fraction_string)

		if fraction_contributions[LowNormalHigh.LOW][block] < fraction_contributions[LowNormalHigh.NORMAL][block] and \
		   fraction_contributions[LowNormalHigh.HIGH][block] < fraction_contributions[LowNormalHigh.NORMAL][block]:

			if sufficient_data_contributions[LowNormalHigh.NORMAL][block] >= 2:
					print("=> NORMAL")

		if fraction_contributions[LowNormalHigh.LOW][block] < fraction_contributions[LowNormalHigh.HIGH][block] and \
		   fraction_contributions[LowNormalHigh.NORMAL][block] <= fraction_contributions[LowNormalHigh.HIGH][block]:

			if sufficient_data_contributions[LowNormalHigh.HIGH][block] >= 2 and \
			   (fraction_contributions[LowNormalHigh.LOW][block] == 0 or \
			    (fraction_contributions[LowNormalHigh.LOW][block] > 0 and \
			     fraction_contributions[LowNormalHigh.HIGH][block]/fraction_contributions[LowNormalHigh.LOW][block] >= 3)):
					print("=> HIGH")

			if fraction_contributions[LowNormalHigh.LOW][block] > 0:

				if block_is_not_an_element_of_half_hours:
					fraction_string = "      => +"
				else:
					fraction_string = "            => +"

				fraction_string = fraction_string + \
				                  str(fraction_contributions[LowNormalHigh.HIGH][block]/fraction_contributions[LowNormalHigh.LOW][block])

				print(fraction_string)


		if block_is_not_an_element_of_half_hours:
			print_and_analyze_half_hour_block_contributions(half_hours, block, events)
			print("")


def print_and_analyze_half_hour_block_contributions(half_hours, block, events):

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
sufficient_data_contributions = {}

for lnh in LowNormalHigh:

	fraction_contributions[lnh] = {}
	sufficient_data_contributions[lnh] = {}


	for block in basals:
		fraction_contributions[lnh][block] = 0
		sufficient_data_contributions[lnh][block] = 0

	for block in half_hour_basals:
		fraction_contributions[lnh][block] = 0
		sufficient_data_contributions[lnh][block] = 0


	for block in carb_ratios:
		fraction_contributions[lnh][block] = 0
		sufficient_data_contributions[lnh][block] = 0

	for block in half_hour_carb_ratios:
		fraction_contributions[lnh][block] = 0
		sufficient_data_contributions[lnh][block] = 0


	for block in sensitivities:
		fraction_contributions[lnh][block] = 0
		sufficient_data_contributions[lnh][block] = 0

	for block in half_hour_sensitivities:
		fraction_contributions[lnh][block] = 0
		sufficient_data_contributions[lnh][block] = 0


# calculate contributions
for event in events:


	for block in basals_impacting[event]:
		fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
		sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[1]

	for block in half_hour_basals_impacting[event]:
		fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
		sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[1]


	if(event.type == EventType.BOLUS):

		for block in carb_ratios_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[2]

		for block in half_hour_carb_ratios_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[2]


	if(event.type == EventType.CORRECTION or event.type == EventType.BOLUS):
		for block in sensitivities_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[3]

		for block in half_hour_sensitivities_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[3]

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