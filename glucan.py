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

	if event.type == EventType.INDEPENDENT and block.type == RatioType.BASAL and block.range.contains_time(event.range.end, 0):
                sufficient_basal_data = 1.

	if event.type == EventType.CORRECTION:
		if block.type == RatioType.BASAL:
                        fraction *= 1./2.                      	
		if block.type == RatioType.SENSITIVITY:
			if block.range.contains_time(event.adjustment_time, 0):
				fraction = 1./2.
				sufficient_sensitivity_data = 1./2.
			else:
				fraction = 0
		if block.type == RatioType.CARB_RATIO:
                        fraction = 0

	if event.type == EventType.BOLUS:
		if block.type == RatioType.BASAL:
                       fraction *= 1./2.  
		if block.type == RatioType.CARB_RATIO:
			if block.range.contains_time(event.adjustment_time, 0):
				if event.start_lnh == LowNormalHigh.NORMAL:
					fraction = 1./2.
					sufficient_carb_ratio_data = 1./2.
				elif (event.start_lnh == LowNormalHigh.OUT_OF_RANGE or event.start_lnh == LowNormalHigh.LOW or event.start_lnh == LowNormalHigh.HIGH):
					fraction = 1./4.
				else:
					fraction = 0
			else:
				fraction = 0
		if block.type == RatioType.SENSITIVITY:
			if block.range.contains_time(event.adjustment_time, 0) and \
                           (event.start_lnh == LowNormalHigh.OUT_OF_RANGE or event.start_lnh == LowNormalHigh.LOW or event.start_lnh == LowNormalHigh.HIGH):
				fraction = 1./4.
			else:
				fraction = 0

	if event.source == Source.SENSOR:
		fraction *= 1./3.
		sufficient_basal_data = 0
		sufficient_sensitivity_data = 0
		sufficient_carb_ratio_data = 0

	return (fraction, sufficient_basal_data, sufficient_sensitivity_data, sufficient_carb_ratio_data)

def analyze_ratio_block(event, block):
	(fraction, sufficient_basal_data, sufficient_sensitivity_data, sufficient_carb_ratio_data) = calculate_fraction(event, block)
	return str(block.range) + ": " + str(fraction) + " (" + Range.time_string(block.range.overlap(event.range)) + " overlap)"

def print_half_hour_block_contributions(half_hours, block, events):

        for half_hour_block in half_hours:
                if block.range.overlap(half_hour_block.range) > 0:

                        contributions_string = "            " + str(half_hour_block.range) + ": \n"
                        print_worthy = 0.
                                                
                        for lnh in LowNormalHigh:

                                if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
                                        continue
                                
                                fraction = 0.
                                sufficient_basal_data = 0.
                                contribution = 0.
                                
                                for event in events:

                                        if event.end_lnh == lnh and half_hour_block.range.contains_time(event.range.end, 0):
                                                
                                                if event.type == EventType.INDEPENDENT:
                                                        fraction = 1.
                                                        if event.source == Source.TEST:
                                                                sufficient_basal_data += 1.
                                                if event.type == EventType.CORRECTION or event.type == EventType.BOLUS:
                                                        fraction = 1./2.

                                                if event.source == Source.SENSOR:
                                                        fraction *= 1./3.

                                                contribution += fraction

                                if sufficient_basal_data >= 2:
                                        contributions_string += "               " + str(lnh) + ": " + str(contribution) + "\n"
                                else:
                                        contributions_string += "               " + str(lnh) + ": " + str(contribution) + " INSUFFICIENT DATA \n"

                                if contribution > 0:
                                        print_worthy += contribution

                        if print_worthy > 0:
                                contributions_string = contributions_string[:-1]
                                print(contributions_string)

print("****************************************************************************************************")
print("This software is an experimental tool.")
print("The author makes no guarantees about the correctness of its outputs or its suitability for any task.")
print("****************************************************************************************************")
print("")

sensitivities = parse_ratios("data/sensitivities.csv", RatioType.SENSITIVITY)
basals = parse_ratios("data/basals.csv", RatioType.BASAL)

half_hours = []
uid = 0
for hh in range(0, 48):
        half_hours.append(RatioBlock(
                uid = uid, 
                range = Range(start = float(hh)/2., end = float(hh)/2. + 0.5),
		ratio = -1, # EDIT LATER!
                type = RatioType.BASAL))
        uid += 1
	
carb_ratios = parse_ratios("data/carb_ratios.csv", RatioType.CARB_RATIO)

events = parse_events("data/events.csv")

sensitivities_impacting = {}
basals_impacting = {}
half_hours_impacting = {}
carb_ratios_impacting = {}

# calculate all intersections
for event in events:
	sensitivities_impacting[event] = []
	basals_impacting[event] = []
	half_hours_impacting[event] = []
	carb_ratios_impacting[event] = []

	for block in sensitivities:
		if block.range.overlap(event.range) > 0:
			sensitivities_impacting[event].append(block)

	for block in basals:
		if block.range.overlap(event.range) > 0:
			basals_impacting[event].append(block)

	for block in half_hours:
		if block.range.overlap(event.range) > 0:
			half_hours_impacting[event].append(block)

	for block in carb_ratios:
		if block.range.overlap(event.range) > 0:
			carb_ratios_impacting[event].append(block)

# initialize contributions
fraction_contributions = {}
for lnh in LowNormalHigh:
	fraction_contributions[lnh] = {}
	for block in sensitivities:
		fraction_contributions[lnh][block] = 0
	for block in basals:
		fraction_contributions[lnh][block] = 0
	for block in half_hours:
		fraction_contributions[lnh][block] = 0
	for block in carb_ratios:
		fraction_contributions[lnh][block] = 0

sufficient_data_contributions = {}
for lnh in LowNormalHigh:
	sufficient_data_contributions[lnh] = {}
	for block in sensitivities:
		sufficient_data_contributions[lnh][block] = 0
	for block in basals:
		sufficient_data_contributions[lnh][block] = 0
	for block in half_hours:
		sufficient_data_contributions[lnh][block] = 0
	for block in carb_ratios:
		sufficient_data_contributions[lnh][block] = 0

# print intersections and tally contributions
for event in events:
	# print("\nevent:")
	# print(event)

	# print("  basal overlap:")
	for block in basals_impacting[event]:
                fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
                # print("    " + analyze_ratio_block(event, block))
                sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[1]

	if(event.type == EventType.CORRECTION or event.type == EventType.BOLUS):
		# print("  sensitivity overlap:")
		for block in sensitivities_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			# print("    " + analyze_ratio_block(event, block))
			sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[2]

	if(event.type == EventType.BOLUS):
		# print("  carb ratio overlap:")
		for block in carb_ratios_impacting[event]:
			fraction_contributions[event.end_lnh][block] += calculate_fraction(event, block)[0]
			# print("    " + analyze_ratio_block(event, block))
			sufficient_data_contributions[event.end_lnh][block] += calculate_fraction(event, block)[3]

# print contributions
print("\n")


print("basals:")
for block in basals:
	
	print("   " + str(block.range) + ": ")	
	for lnh in LowNormalHigh:
		if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
			continue

		print("      " + str(lnh) + ": " + str(fraction_contributions[lnh][block]))

		if fraction_contributions[LowNormalHigh.NORMAL][block] < fraction_contributions[LowNormalHigh.LOW][block] and \
		   fraction_contributions[LowNormalHigh.HIGH][block] < fraction_contributions[LowNormalHigh.LOW][block]:

			print(lnh)
			print(sufficient_data_contributions[lnh][block])
			if sufficient_data_contributions[lnh][block] >= 2 and \
			   ((fraction_contributions[LowNormalHigh.HIGH][block] == 0 and \
			     fraction_contributions[LowNormalHigh.LOW][block] >= 2) or \
			    (fraction_contributions[LowNormalHigh.HIGH][block] > 0 and \
			     fraction_contributions[LowNormalHigh.LOW][block]/fraction_contributions[LowNormalHigh.HIGH][block] >= 3)):
				print("=> LOW")

			else:
				if fraction_contributions[LowNormalHigh.HIGH][block] > 0:
					print("      => -" + str(fraction_contributions[LowNormalHigh.LOW][block]/fraction_contributions[LowNormalHigh.HIGH][block]))
				print_half_hour_block_contributions(half_hours, block, events)

		if fraction_contributions[LowNormalHigh.LOW][block] < fraction_contributions[LowNormalHigh.NORMAL][block] and \
		   fraction_contributions[LowNormalHigh.HIGH][block] < fraction_contributions[LowNormalHigh.NORMAL][block]:

			if sufficient_data_contributions[event.end_lnh][block] >= 2:
				print("=> NORMAL")

			else:
				print_half_hour_block_contributions(half_hours, block, events)

		if fraction_contributions[LowNormalHigh.LOW][block] < fraction_contributions[LowNormalHigh.HIGH][block] and \
		   fraction_contributions[LowNormalHigh.NORMAL][block] < fraction_contributions[LowNormalHigh.HIGH][block]:

			if sufficient_data_contributions[event.end_lnh][block] >= 2 and \
			   ((fraction_contributions[LowNormalHigh.LOW][block] == 0 and \
			     fraction_contributions[LowNormalHigh.HIGH][block] >= 2) or \
			    (fraction_contributions[LowNormalHigh.LOW][block] > 0 and \
			     fraction_contributions[LowNormalHigh.HIGH][block]/fraction_contributions[LowNormalHigh.LOW][block] >= 3)):
				print("=> HIGH")

			else:
				if fraction_contributions[LowNormalHigh.LOW][block] > 0:
					print("      => +" + str(fraction_contributions[LowNormalHigh.HIGH][block]/fraction_contributions[LowNormalHigh.LOW][block]))
				print_half_hour_block_contributions(half_hours, block, events)
					
print("")

print("carb ratios:")
for block in carb_ratios:
	print("   " + str(block.range).rjust(14) + ": ")
	for lnh in LowNormalHigh:                
		if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
			continue

		if sufficient_data_contributions[lnh][block] >= 1:
                        print("      " + str(lnh) + ": " + str(fraction_contributions[lnh][block]))

		else:
			print("      " + str(lnh) + ": " + str(fraction_contributions[lnh][block]) + " INSUFFICIENT DATA")
		
print("")

print("sensitivities:")
for block in sensitivities:
	print("   " + str(block.range).rjust(14) + ": ")
	for lnh in LowNormalHigh:
		if lnh == LowNormalHigh.OUT_OF_RANGE or lnh == LowNormalHigh.UNKNOWN:
			continue
		
		if sufficient_data_contributions[lnh][block] >= 1:
                        print("      " + str(lnh) + ": " + str(fraction_contributions[lnh][block]))

		else:
			print("      " + str(lnh) + ": " + str(fraction_contributions[lnh][block]) + " INSUFFICIENT DATA")
