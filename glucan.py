from enum import Enum

from parse_input import *
from RatioBlock import *
from Event import *


def calculate_fraction(event, block):
	overlap = block.range.overlap(event.range)
	fraction = overlap / event.range.length()

	if event.type == EventType.INDEPENDENT:
		if event.source == Source.SENSOR:
			fraction *= 1./3.

	if event.type == EventType.CORRECTION:
			if event.method == Method.BASAL and block.type == RatioType.SENSITIVITY:
				fraction = 0
			
			if event.source == Source.SENSOR:
				fraction *= 1./3.
			fraction *= 1./2.
			if block.range.contains_time(event.range.start) and block.type == RatioType.SENSITIVITY:
				fraction += 1./2.

	if event.type == EventType.BOLUS:
		if block.type == RatioType.CARB_RATIO:
			fraction = 0

		if event.source == Source.SENSOR:
			fraction *= 1./3.
		fraction *= 1./2.

		if block.type == RatioType.SENSITIVITY and block.range.contains_time(event.range.start) and (event.start_lnh == LowNormalHigh.HIGH or event.start_lnh == LowNormalHigh.LOW):
			fraction += 1./4.
		if block.type == RatioType.CARB_RATIO and block.range.contains_time(event.range.start) and event.start_lnh == LowNormalHigh.NORMAL:
			fraction += 1./2.
		if block.type == RatioType.CARB_RATIO and block.range.contains_time(event.range.start) and (event.start_lnh == LowNormalHigh.HIGH or event.start_lnh == LowNormalHigh.LOW):
			fraction += 1./4.

	return fraction

def analyze_ratio_block(event, block):
	fraction = calculate_fraction(event, block)
	return str(block.range) + ": " + str(fraction) + " (" + Range.time_string(block.range.overlap(event.range)) + " overlap)"


print("********************************************************")
print("This software is an experimental tool.  The author makes")
print("no guarantees about the correctness of its outputs or")
print("its suitability for any task.")
print("********************************************************")
print("")

sensitivities = parse_ratios("example_input/sensitivities.csv", RatioType.SENSITIVITY)
basals = parse_ratios("example_input/basals.csv", RatioType.BASAL)
carb_ratios = parse_ratios("example_input/carb_ratios.csv", RatioType.CARB_RATIO)

events = parse_events("example_input/events.csv")

sensitivities_impacting = {}
basals_impacting = {}
carb_ratios_impacting = {}

# calculate all intersections
for event in events:
	sensitivities_impacting[event] = []
	basals_impacting[event] = []
	carb_ratios_impacting[event] = []

	for block in sensitivities:
		if block.range.overlap(event.range) > 0:
			sensitivities_impacting[event].append(block)

	for block in basals:
		if block.range.overlap(event.range) > 0:
			basals_impacting[event].append(block)

	for block in carb_ratios:
		if block.range.overlap(event.range) > 0:
			carb_ratios_impacting[event].append(block)

# initialize contributions
contributions = {}
for lnh in LowNormalHigh:
	contributions[lnh] = {}
	for block in sensitivities:
		contributions[lnh][block] = 0
	for block in basals:
		contributions[lnh][block] = 0
	for block in carb_ratios:
		contributions[lnh][block] = 0

# print intersections and tally contributions
for event in events:
	print("\nevent:")
	print(event)
	
	if(event.method == Method.SENSITIVITY or (event.method == Method.BASAL and event.type == EventType.CORRECTION)):
		print("  sensitivity overlap:")
		for block in sensitivities_impacting[event]:
			contributions[event.start_lnh][block] += calculate_fraction(event, block)
			print("    " + analyze_ratio_block(event, block))

	if(event.method == Method.BASAL):
		print("  basal overlap:")
		for block in basals_impacting[event]:
			contributions[event.start_lnh][block] += calculate_fraction(event, block)
			print("    " + analyze_ratio_block(event, block))

	if(event.type == EventType.BOLUS):
		print("  carb ratio overlap:")
		for block in carb_ratios_impacting[event]:
			contributions[event.start_lnh][block] += calculate_fraction(event, block)
			print("    " + analyze_ratio_block(event, block))

# print contributions
print("\n")
for lnh in LowNormalHigh:
	if lnh == LowNormalHigh.UNKNOWN:
		continue
	print("sensitivities " + str(lnh) + " weight:")
	for block in sensitivities:
		print("  " + str(block.range).rjust(14) + ": " + str(contributions[lnh][block]))

print("")
for lnh in LowNormalHigh:
	if lnh == LowNormalHigh.UNKNOWN:
		continue
	print("basals " + str(lnh) + " weight:")
	for block in basals:
		print("  " + str(block.range).rjust(14) + ": " + str(contributions[lnh][block]))

print("")
for lnh in LowNormalHigh:
	if lnh == LowNormalHigh.UNKNOWN:
		continue
	print("carb ratios " + str(lnh) + " weight:")
	for block in carb_ratios:
		print("  " + str(block.range).rjust(14) + ": " + str(contributions[lnh][block]))
			
			







