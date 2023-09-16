from calculate_contributions import calculate_contributions
from Event import Level
from sum_contributions import *
from RatioBlock import RatioType



print("****************************************************************************************************")
print("This software is an experimental tool.")
print("The author makes no guarantees about the correctness of its outputs or its suitability for any task.")
print("****************************************************************************************************")
print("")
print("")
print("")



def print_and_analyze_block_contributions(block, block_is_a_ratio_block, events, half_hours):


	block_has_sufficienct_events = sufficiency_contributions[Level.LOW][block] >= 1 or \
	                               sufficiency_contributions[Level.IN_RANGE][block] >= 1 or \
	                               sufficiency_contributions[Level.HIGH][block] >= 1

	block_has_no_contributions = fraction_contributions[Level.LOW][block] == 0 and \
	                             fraction_contributions[Level.IN_RANGE][block] == 0 and \
	                             fraction_contributions[Level.HIGH][block] == 0


	# printing the block's range and ratio

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


	# determining if there is sufficient data to analyze

	if (block_is_a_ratio_block and block_has_sufficienct_events) or \
	   (block_is_a_ratio_block == False and block_has_no_contributions == False):


		# printing the block's contributions

		for level in Level:
			if level == Level.UNKNOWN:
				continue

			if block_is_a_ratio_block:
				contributions_string = "      "
			else:
				contributions_string = "            "

			contributions_string = contributions_string + str(level) + ": " + str(fraction_contributions[level][block])

			# analyzing the block's contributions' sufficiency
			if sufficiency_contributions[level][block] >= 1:
				contributions_string = contributions_string + "   Sufficient Events"
			elif sufficiency_contributions[level][block] == 1/2:
				contributions_string = contributions_string + "   half sufficient event"

			print(contributions_string)		


		if block.type == RatioType.CARB_RATIO:

			# calculating the block's average carbohydrate-ratio-related change

			sum_of_negative_changes = 0
			number_of_calculatable_negative_changes = 0
			number_of_uncalculatable_negative_changes = 0

			number_of_zero_changes = 0

			sum_of_positive_changes = 0
			number_of_calculatable_positive_changes = 0
			number_of_uncalculatable_positive_changes = 0

			for event in events:

				if calculate_contributions(event, block, False)[2] == 1/2:

					if event.start_bg != -1 and event.end_bg != -1:

						change = event.end_bg-event.start_bg

						if change < 0:
							sum_of_negative_changes += change
							number_of_calculatable_negative_changes += 1

						elif change == 0:
							number_of_zero_changes += 1

						elif change > 0:
							sum_of_positive_changes += change
							number_of_calculatable_positive_changes += 1

					else:

						if event.end_level == Level.LOW:
							number_of_uncalculatable_negative_changes += 1

						elif event.end_level == Level.HIGH:
							number_of_uncalculatable_positive_changes += 1

			if number_of_calculatable_negative_changes != 0:
				average_negative_changes = sum_of_negative_changes/number_of_calculatable_negative_changes
			else:
				average_negative_changes = 0
				number_of_uncalculatable_negative_changes = 0

			if number_of_calculatable_positive_changes != 0:
				average_positive_changes = sum_of_positive_changes/number_of_calculatable_positive_changes
			else:
				average_positive_changes = 0
				number_of_uncalculatable_positive_changes = 0
			
			sum_of_changes = sum_of_negative_changes + number_of_uncalculatable_negative_changes*average_negative_changes + \
							 number_of_zero_changes*0 + \
							sum_of_positive_changes + number_of_uncalculatable_positive_changes*average_positive_changes

			number_of_changes = number_of_calculatable_negative_changes + number_of_uncalculatable_negative_changes + \
								number_of_zero_changes + \
								number_of_calculatable_positive_changes + number_of_uncalculatable_positive_changes

			if number_of_changes != 0:

				average_change = sum_of_changes/number_of_changes

				# printing the block's average carbohydrate-ratio-related change

				if block_is_a_ratio_block:
					change_string = "      "
				else:
					change_string = "            "

				change_string = change_string + "=> "

				if average_change > 0:
					change_string = change_string + "+"

				change_string = change_string + str(average_change) + "mg/dL"

				print(change_string)

			
		# analyzing the block's contribu...

		fraction_string_exists = False

		if fraction_contributions[Level.IN_RANGE][block] <= fraction_contributions[Level.LOW][block] and \
		   fraction_contributions[Level.HIGH][block] < fraction_contributions[Level.LOW][block]:

			if sufficiency_contributions[Level.LOW][block] >= 1 and \
			   (fraction_contributions[Level.HIGH][block] == 0 or \
			    (fraction_contributions[Level.HIGH][block] > 0 and \
			     fraction_contributions[Level.LOW][block]/fraction_contributions[Level.HIGH][block] >= 3)):
					print("=> LOW")

			if fraction_contributions[Level.HIGH][block] > 0:

				if block_is_a_ratio_block:
					fraction_string = "      "
				else:
					fraction_string = "            "

				fraction_string = fraction_string + "=> -" +\
				                  str(fraction_contributions[Level.LOW][block]/fraction_contributions[Level.HIGH][block])
				
				fraction_string_exists = True

		if fraction_contributions[Level.LOW][block] < fraction_contributions[Level.IN_RANGE][block] and \
		   fraction_contributions[Level.HIGH][block] < fraction_contributions[Level.IN_RANGE][block]:

			if sufficiency_contributions[Level.IN_RANGE][block] >= 1:
					print("=> IN_RANGE")

		if fraction_contributions[Level.LOW][block] < fraction_contributions[Level.HIGH][block] and \
		   fraction_contributions[Level.IN_RANGE][block] <= fraction_contributions[Level.HIGH][block]:

			if sufficiency_contributions[Level.HIGH][block] >= 1 and \
			   (fraction_contributions[Level.LOW][block] == 0 or \
			    (fraction_contributions[Level.LOW][block] > 0 and \
			     fraction_contributions[Level.HIGH][block]/fraction_contributions[Level.LOW][block] >= 3)):
					print("=> HIGH")

			if fraction_contributions[Level.LOW][block] > 0:

				if block_is_a_ratio_block:
					fraction_string = "      "
				else:
					fraction_string = "            "

				fraction_string = fraction_string + "=> +" + \
				                  str(fraction_contributions[Level.HIGH][block]/fraction_contributions[Level.LOW][block])

				fraction_string_exists = True

		# analyzing the block's average carbohydrate-ratio-related change
		if block.type == RatioType.CARB_RATIO and \
		   (sufficiency_contributions[Level.LOW][block] >= 1.5 and \
		    sufficiency_contributions[Level.HIGH][block] >= 1.5):

				if number_of_uncalculatable_negative_changes < number_of_calculatable_negative_changes and average_change < -25:
					print("=> Low")

				elif number_of_uncalculatable_positive_changes < number_of_calculatable_positive_changes and average_change > 25:
					print("=> High")

		# ...alyzing the block's contributions

		if fraction_string_exists:
			print(fraction_string)


	# printing and analyzing the block's sub-blocks

		if block_is_a_ratio_block:

			print_and_analyze_half_hour_block_contributions(block, half_hours, events)
			print("")

	if block_is_a_ratio_block == False:

		printed_half_hour = False

		for level in Level:

			if level == Level.UNKNOWN:
				continue

			if on_the_half_hour_sufficiency_contributions[level][block] >= 1:
			
				if printed_half_hour == False:
					print("         " + Range.time_str(block.range.end) + ":")
					printed_half_hour = True

				print("            " + str(level) + " -------------------   Sufficient Events")

			elif on_the_half_hour_sufficiency_contributions[level][block] >= 1/2:

				if printed_half_hour == False:
					print("         " + Range.time_str(block.range.end) + ":")
					printed_half_hour = True

				print("            " + str(level) + " -------------------   half sufficient event")


def print_and_analyze_half_hour_block_contributions(block, half_hours, events):

	for half_hour_block in half_hours:

			if block.range.overlap(half_hour_block.range) > 0 and block.range.end - block.range.start > 0.5:
				print_and_analyze_block_contributions(half_hour_block, False, events, half_hours)



# printing and analyzing contributions

print("basals:")
print("")
for block in basals:
	print_and_analyze_block_contributions(block, True, events, half_hour_basals)

print("")
print("")

print("carb ratios:")
print("")
for block in carb_ratios:
	print_and_analyze_block_contributions(block, True, events, half_hour_carb_ratios)

print("")
print("")

print("sensitivities:")
print("")
for block in sensitivities:
	print_and_analyze_block_contributions(block, True, events, half_hour_sensitivities)

print("")
print("")