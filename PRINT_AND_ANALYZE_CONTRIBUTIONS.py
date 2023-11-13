from analyze_average_change import analyze_average_change
from Event import Level
from RatioBlock import RatioType
from sum_contributions import *



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


	# printing the block's range of time and ratio

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


		# analyzing the block's contributions

		conclusion_exists = False
		fraction_exists = False

		if fraction_contributions[Level.IN_RANGE][block] <= fraction_contributions[Level.LOW][block] and \
		   fraction_contributions[Level.HIGH][block] < fraction_contributions[Level.LOW][block]:

			if sufficiency_contributions[Level.LOW][block] >= 1 and \
			   (fraction_contributions[Level.HIGH][block] == 0 or \
			    (fraction_contributions[Level.HIGH][block] > 0 and \
			     fraction_contributions[Level.LOW][block]/fraction_contributions[Level.HIGH][block] >= 3)):

					if block_is_a_ratio_block:
						conclusion_string = ""
					else:
						conclusion_string = "     "

					if block.type == RatioType.CARB_RATIO:
						conclusion_string = conclusion_string + "=> Low"
						conclusion_exists = True
					else:
						conclusion_string = conclusion_string + "=> LOW"
						conclusion_exists = True

			if fraction_contributions[Level.HIGH][block] > 0:

				if block_is_a_ratio_block:
					fraction_string = "      "
				else:
					fraction_string = "            "

				if conclusion_exists:
					conclusion_string = conclusion_string + " b/c"
				else:
					fraction_string = fraction_string + "=> "

				fraction_string = fraction_string + "-" +\
				                  str(fraction_contributions[Level.LOW][block]/fraction_contributions[Level.HIGH][block])
				
				fraction_exists = True

		if fraction_contributions[Level.LOW][block] < fraction_contributions[Level.IN_RANGE][block] and \
		   fraction_contributions[Level.HIGH][block] < fraction_contributions[Level.IN_RANGE][block]:

			if sufficiency_contributions[Level.IN_RANGE][block] >= 1:
				if block_is_a_ratio_block:
					print("=> IN_RANGE")
				else:
					print("     => IN_RANGE")

		if fraction_contributions[Level.LOW][block] < fraction_contributions[Level.HIGH][block] and \
		   fraction_contributions[Level.IN_RANGE][block] <= fraction_contributions[Level.HIGH][block]:

			if sufficiency_contributions[Level.HIGH][block] >= 1 and \
			   (fraction_contributions[Level.LOW][block] == 0 or \
			    (fraction_contributions[Level.LOW][block] > 0 and \
			     fraction_contributions[Level.HIGH][block]/fraction_contributions[Level.LOW][block] >= 3)):

					if block_is_a_ratio_block:
						conclusion_string = ""
					else:
						conclusion_string = "     "

					if block.type == RatioType.CARB_RATIO:
						conclusion_string = conclusion_string + "=> High"
						conclusion_exists = True
					else:
						conclusion_string = conclusion_string + "=> HIGH"
						conclusion_exists = True

			if fraction_contributions[Level.LOW][block] > 0:

				if block_is_a_ratio_block:
					fraction_string = "      "
				else:
					fraction_string = "            "

				if conclusion_exists:
					conclusion_string = conclusion_string + " b/c"
				else:
					fraction_string = fraction_string + "=> "

				fraction_string = fraction_string + "+" + \
				                  str(fraction_contributions[Level.HIGH][block]/fraction_contributions[Level.LOW][block])

				fraction_exists = True


		if block.type == RatioType.CARB_RATIO:
			analyze_average_change(events, block, block_is_a_ratio_block)


		if conclusion_exists:
			print(conclusion_string)

		if fraction_exists:
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
					print("         " + Range_of_Time.time_str(block.range.end) + ":")
					printed_half_hour = True

				print("            " + str(level) + " -------------------   Sufficient Events")

			elif on_the_half_hour_sufficiency_contributions[level][block] >= 1/2:

				if printed_half_hour == False:
					print("         " + Range_of_Time.time_str(block.range.end) + ":")
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