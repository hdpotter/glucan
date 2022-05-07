from parse_input import *
from RatioBlock import RatioBlock
from Event import *


# def analyze_sensitivity(event, sensitivity, overlap):
# 	if event["type"] == "independent":
# 		overlapFraction = overlap / 




sensitivities = parse_ratios("example_input/sensitivities.csv")
basals = parse_ratios("example_input/basals.csv")
carb_ratios = parse_ratios("example_input/carb_ratios.csv")

events = parse_events("example_input/events.csv")

sensitivities_impacting = {}
basals_impacting = {}
carb_ratios_impacting = {}

for event in events:
	sensitivities_impacting[event] = []
	basals_impacting[event] = []
	carb_ratios_impacting[event] = []

	if(event.type == EventType.INDEPENDENT):
		for block in sensitivities:
			if block.range.overlap(event.range) > 0:
				sensitivities_impacting[event].append(block)

		for block in basals:
			if block.range.overlap(event.range) > 0:
				basals_impacting[event].append(block)

		for block in carb_ratios:
			if block.range.overlap(event.range) > 0:
				carb_ratios_impacting[event].append(block)


for event in events:
	print("\nevent:")
	print(event)
	
	print("sensitivity overlap:")
	for block in sensitivities_impacting[event]:
		print(str(block.range) + ", overlap " + Range.time_string(block.range.overlap(event.range)))

	print("basal overlap")
	for block in basals_impacting[event]:
		print(str(block.range) + ", overlap " + Range.time_string(block.range.overlap(event.range)))

	print("carb ratio overlap")
	for block in carb_ratios_impacting[event]:
		print(str(block.range) + ", overlap " + Range.time_string(block.range.overlap(event.range)))


			
			







