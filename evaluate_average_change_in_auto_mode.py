from calculate_contributions_from_auto_mode import calculate_contributions_from_auto_mode
from Event import Level



def evaluate_average_change_in_auto_mode(events, block, block_is_a_ratio_block):


	# calculating the block's average carbohydrate-ratio-related change

	number_of_large_negative_changes = 0
	sum_of_negative_changes = 0
	number_of_calculatable_negative_changes = 0
	number_of_uncalculatable_negative_changes = 0

	number_of_zero_changes = 0

	number_of_large_positive_changes = 0
	sum_of_positive_changes = 0
	number_of_calculatable_positive_changes = 0
	number_of_uncalculatable_positive_changes = 0


	for event in events:

		if calculate_contributions_from_auto_mode(event, block, False)[1] == 1/2:

			if event.start_bg != -1 and event.end_bg != -1:

				change = event.end_bg-event.start_bg

				if change < -25:
					number_of_large_negative_changes += 1
				if change < 0:
					sum_of_negative_changes += change
					number_of_calculatable_negative_changes += 1

				if change == 0:
					number_of_zero_changes += 1

				if change > 25:
					number_of_large_positive_changes += 1
				if change > 0:
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

		conclusion_exists = False


		# evaluating the block's average carbohydrate-ratio-related change

		if (number_of_calculatable_negative_changes >= 3 or number_of_large_negative_changes >= 2) and \
		   number_of_uncalculatable_negative_changes < number_of_calculatable_negative_changes and \
		   average_change < -25:

				if block_is_a_ratio_block:
					print("=> LOW b/c")
				else:
					print("     => LOW b/c")

				conclusion_exists = True

		if (number_of_calculatable_positive_changes >= 3 or number_of_large_positive_changes >= 2) and \
		   number_of_uncalculatable_positive_changes < number_of_calculatable_positive_changes and \
		   average_change > 25:

				if block_is_a_ratio_block:
					print("=> HIGH b/c")
				else:
					print("     => HIGH b/c")

				conclusion_exists = True


		if block_is_a_ratio_block:
			average_change_string = "      "
		else:
			average_change_string = "            "

		if conclusion_exists == False:
			average_change_string = average_change_string + "=> "

		if average_change > 0:
			average_change_string = average_change_string + "+"

		average_change_string = average_change_string + str(average_change) + " mg/dL"

		print(average_change_string)