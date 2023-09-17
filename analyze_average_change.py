from calculate_contributions import calculate_contributions
from Event import Level
from sum_contributions import *



def analyze_average_change(events, block):


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


		average_change_is_calculatable = True


		# analyzing the block's average carbohydrate-ratio-related change
		if sufficiency_contributions[Level.LOW][block] >= 1.5 and sufficiency_contributions[Level.HIGH][block] >= 1.5:

				if number_of_uncalculatable_negative_changes < number_of_calculatable_negative_changes and average_change < -25:
					print("=> LOW")

				elif number_of_uncalculatable_positive_changes < number_of_calculatable_positive_changes and average_change > 25:
					print("=> HIGH")


		return(average_change_is_calculatable, average_change)


	else:

		average_change_is_calculatable = False

		return(average_change_is_calculatable, -1000)