import Database

# ****** HELPER FUNCTIONS ******

def prettyPrintResults(results, headings): 
	'''
		Function to print the results of a query in a readable format.
		Inputs: results - list of rows (lists), headings - list of strings
	'''
	# Check if there is data 
	if len(results) == 0: 
		print("\tSorry, there is no data available for those parameters.")
		return 

	#Get the max length for each column
	max_length_for_columns = []
	for heading in headings: 
		max_length_for_columns.append(len(heading))
	for result in results: 
		for i in range(len(result)): 
			if len(str(result[i])) > max_length_for_columns[i]: 
				max_length_for_columns[i] = len(str(result[i]))

	#Print the headings
	print()
	header = ""
	for i in range(len(headings)): 
		header += "\t{1:<{0}}".format(max_length_for_columns[i], headings[i])
	print(header)
	print("\t", "-"*(len(header) + (len(headings)-1)*4), sep="")

	#print the results
	for result in results:
		for i in range(len(result)): 
			print("\t{1:<{0}}".format(max_length_for_columns[i], str(result[i])), end="", sep="")
		print()

def printQueryOptions(): 
	'''
		Function to print the query options.
	'''
	print("\n\tThe following discovery options are available: \n")
	print("\t\t1. Get the leading cause of death for each state during a given year.")
	print("\t\t2. Get percent of people with no physical activity for states where \n\t\t   30%% of the population and overweight for a given year.")
	print("\t\t3. Get the percent of people with no physical activity for states \n\t\t   where heart disease is the leading cause of death for a given year.")
	print("\t\t4. Explore Chronic Disease Indicators by year, state, and topic.")
	print("\t\t5. Explore Nutrition dataset by year, state, and topic.")
	print("\t\t6. Get the leading causes of deaths (and their rates) for states where\n\t\t   more than 30%% of people have no physical activity.")
	print("\t\t7. Get drug poisoning statistics for a given year and state.")

def getYearFromUser(year_range): 
	'''
		Function to get a valid year through user input. 
		Input: year_range tuple
		Output: Year chosen by user
	'''
	year_input_invalid = True
	while year_input_invalid: 
		user_year_input = input("\tEnter a year value in the range {}-{}: ".format(year_range[0], year_range[1])).strip()
		if not user_year_input.isdigit() or int(user_year_input) < year_range[0] or int(user_year_input) > year_range[1]: 
			print("\tInvalid year. Try Again.")
		else: 
			user_year_input = int(user_year_input)
			year_input_invalid = False
	return user_year_input

def getStateFromUser(list_of_states): 
	'''
		Funtion to get a valid state through user input. 
		Input: list of states 
		Output: state chosen by user
	'''
	state_input_invalid = True
	while state_input_invalid:
		user_state_input = input("\n\tEnter a state (full name): ").strip()
		if not user_state_input.title() in list_of_states: 
			print("\tInvalid State. Try Again.") 
		else: 
			state_input_invalid = False
	return user_state_input

def getTopicIDFromUser(available_topics_dict, topics_list): 
	'''
		Funciton to get a valid TopicID from the user. 
		Input: available_topics_dict - dictionary with topics as keys and topicIDs as values
			   topics_list - list of topic names (these are the keys in the above dictionary)
		Output: The topicID for the topic the user chose. 
	'''
	for i in range(len(topics_list)): 
		print("\t{}. {}".format(i, topics_list[i]))
	user_topic_invalid = True
	while user_topic_invalid: 
		user_topic_input = input("\n\tChoose one of the topics above, and enter the corresponding number: ").strip()
		if not user_topic_input.isdigit() or not (int(user_topic_input) > -1 and int(user_topic_input) < len(topics_list)): 
			print("\tInvalid choice. Try Again.") 
		else: 
			user_topic_invalid = False
	return available_topics_dict[topics_list[int(user_topic_input)]]

def getQuesionIDFromUser(questions): 
	'''
		Function to get the question and questionID chosen by the user. 
		Input: questions - list of 2 element lists where the first element is the question and 
		       the second element is the questionID.
		Output: a tuple with the chosen question and questionID
	'''
	for i in range(len(questions)): 
		print("\t{}. {}".format(i, questions[i][0]))
	user_question_invalid = True
	while user_question_invalid: 
		user_question_input = input("\n\tChoose one of the questions above, and enter the corresponding number: ").strip()
		if not user_question_input.isdigit() or not (int(user_question_input) > -1 and int(user_question_input) < len(questions)): 
			print("\tInvalid choice. Try Again.")
		else: 
			user_question_invalid = False
	user_questionid = questions[int(user_question_input)][1]
	user_question = questions[int(user_question_input)][0]
	return user_question, user_questionid



# ****** MAIN QUERY FUNCTIONS ******

def runQueryOne(): 
	'''
		Function to run the first query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	print("\n\tGet the leading cause of death for each state during a given year.")

	# Get user input for the 'year' parameter
	print('\n\tChoose a year.')
	year_range = Database.getYearRangeForLeadingCauseOfDeath()
	user_year_input = getYearFromUser(year_range)
	
	# Use the user input to run the main query 
	results = Database.queryOne(user_year_input)
	headings = ['Year', 'State', 'Max Cause Of Death', 'Number of Deaths']
	prettyPrintResults(results, headings)

def runQueryTwo(): 
	'''
		Function to run the second query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	print("\n\tGet States and percent of people with no physical activity for states where \n\t30%% of the population and overweight for a given year.")

	# Get user input for the 'year' parameter
	print('\n\tChoose a year.')
	year_range = Database.getYearRangeForNutrition()
	user_year_input = getYearFromUser(year_range)

	# Use the user input to run the main query 
	results = Database.queryTwo(user_year_input)
	headings = ['Year', 'Location', '% People Overweight', '% People w/ No Exercise']
	prettyPrintResults(results, headings)

def runQueryThree(): 
	'''
		Function to run the third query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	print("\n\tGet the percent of people with no physical activity for states \n\twhere heart disease is the leading cause of death for a given year.")

	# Get user input for the 'year' parameter
	print('\n\tChoose a year.')
	year_range_nutrition = Database.getYearRangeForNutrition()
	year_range_lcd = Database.getYearRangeForLeadingCauseOfDeath()
	year_range = (max(year_range_nutrition[0], year_range_lcd[0]), min(year_range_nutrition[1], year_range_lcd[1]))
	user_year_input = getYearFromUser(year_range)

	# Use the user input to run the main query 
	results = Database.queryThree(user_year_input)
	headings = ['Year', 'State', 'Max Cause of Death', '% People w/ No Exercise']
	prettyPrintResults(results, headings)	
	
def runQueryFour(): 
	'''
		Function to run the fourth query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	print('\n\tExplore Chronic Disease Indicators data by year, state, and topic.')

	#Get user input for yearstart and yearend
	year_ranges = Database.getYearStartYearEndRangesCDI()
	print('\n\tChoose a start year.')
	user_start_year_input = getYearFromUser((year_ranges[0], year_ranges[1]))

	print('\n\tChoose an end year.')
	user_end_year_input = getYearFromUser((year_ranges[2], year_ranges[3]))

	# Get User input for a state
	states = Database.getCDIStates()
	list_of_states = []
	for row in states: 
		list_of_states.append(row[0])
	user_state = getStateFromUser(list_of_states)

	# Get the topic from the user 
	print()
	available_topics = Database.getTopicsForCDI()
	available_topics_dict = dict() #Contains the topic and the corresponding TopicID
	topics_list = []	# Contains the topics in a set order (so the user can choose a number as an index)
	for topic in available_topics: 
		available_topics_dict[topic[1]] = topic[0]
		topics_list.append(topic[1])

	user_topic_id = getTopicIDFromUser(available_topics_dict, topics_list)

	# Get questions for the topic chosen
	print()
	questions = Database.getCDIQuestionsForTopicID(user_topic_id)
	user_question, user_questionid = getQuesionIDFromUser(questions)

	# Now run the query with the parameters given by the user and provide question responses for 
	# each demographic. 
	print("\n\tResults for Years: {}-{}, State: {}, \n\tQuestion: {}".format(user_start_year_input, user_end_year_input, user_state, user_question))
	results = Database.queryFour(user_start_year_input, user_end_year_input, user_state, user_questionid)
	headings = ['Stratification Category', 'Stratification', 'Data Value Unit', 'Data Value Type', 'Data Value']
	prettyPrintResults(results, headings)

def runQueryFive(): 
	'''
		Function to run the fifth query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	print("\n\tExplore Nutrition data by year, state, and topic.")

	#Get user input for the year 
	year_range = Database.getYearRangeForNutrition()
	print('\n\tChoose a year.')
	user_year_input = getYearFromUser(year_range)

	#Get user input for a state
	states = Database.getNutritionStates()
	list_of_states = []
	for row in states: 
		list_of_states.append(row[0])
	user_state = getStateFromUser(list_of_states)

	# Get the topic from the user
	print()
	available_topics = Database.getTopicsForNutrition()
	available_topics_dict = dict() #Contains the topic and the corresponding TopicID
	topics_list = []	# Contains the topics in a set order (so the user can choose a number as an index)
	for topic in available_topics: 
		available_topics_dict[topic[1]] = topic[0]
		topics_list.append(topic[1])
	user_topic_id = getTopicIDFromUser(available_topics_dict, topics_list)

	# Get Questions for the topic chosen and have user choose a question
	print()
	questions = Database.getNutritionQuestionsForTopicID(user_topic_id)
	user_question, user_questionid = getQuesionIDFromUser(questions)

	# Now run the query with the parameters given by the user and provide question responses for 
	# each demographic. 
	print("\n\tResults for Year: {}, State: {}, \n\tQuestion: {}".format(user_year_input, user_state, user_question))
	results = Database.queryFive(user_year_input, user_state, user_questionid)
	headings = ['Stratification Category', 'Stratification', 'Data Value Unit', 'Data Value Type', 'Data Value']
	prettyPrintResults(results, headings)

def runQuerySix(): 
	'''
		Function to run the sixth query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	print("\n\tGet the leading causes of deaths (and their rates) for states where\n\t   more than 30%% of people have no physical activity.")

	#Get user input for the year
	print('\n\tChoose a year.')
	year_range_nutrition = Database.getYearRangeForNutrition()
	year_range_lcd = Database.getYearRangeForLeadingCauseOfDeath()
	year_range = (max(year_range_nutrition[0], year_range_lcd[0]), min(year_range_nutrition[1], year_range_lcd[1]))
	user_year_input = getYearFromUser(year_range)

	# Use the user input to run the main query 
	results = Database.querySix(user_year_input)
	headings = ['Year', 'State', '% People w/ No Exercise', 'Leading Causes Of Death', 'Deaths', 'Age Adjusted Death Rate']
	prettyPrintResults(results, headings)	

def runQuerySeven(): 
	'''
		Function to run the seventh query. 
		This function will prompt the user for any extra input needed
		and will call the necessary Database.py functions to run the 
		query. It will also make a call to prettyPrintResults to display 
		the results of the query.
	'''
	#Get year input from the user
	print('\n\tChoose a year.')
	valid_years = Database.getDrugPoisoningYears()
	user_year = getYearFromUser(valid_years)

	#Get state input from the user 
	valid_states = Database.getDrugPoisoningStates()
	user_state = getStateFromUser(valid_states)

	#Run the main query and display the results 
	print("\n\tResults for Year: {}, State: {}".format(user_year, user_state))
	results = Database.querySeven(user_year, user_state)
	results = sorted(results, key = lambda x: (x[0], x[1], x[2]))
	headings = ['Sex', 'Race', 'AgeRange', 'Deaths', 'Population', 'Deaths %% of Population']

	prettyPrintResults(results, headings)




# ****** MAIN PROGRAM ******

# Initial Output
print("\n\n\t**********************************************************************************")
print("\t\tWelcome to the Data Exploration Application for four NCHS datasets!")


# Prompt the user to explore the dataset until they enter "E" to end. 
end_of_program = False
while not end_of_program:

	# Get the user query choice 
	print("\t**********************************************************************************")
	printQueryOptions()
	user_query_choice = input("\n\tPlease enter the number for to the discovery option you would like to run (or enter 'E' to end): ")

	# Get other input from the user based on query choice

	# Check if the user would like to end. 
	if user_query_choice.upper() == 'E': 
		print("\n\tProgram Ended.")
		end_of_program = True
		continue

	# Make sure the input is valid.
	elif not user_query_choice.isdigit() or int(user_query_choice) < 1 or int(user_query_choice) > 7:
		print("\n\t'{}' was not a valid choice.".format(user_query_choice))
		continue

	# Query 1
	elif int(user_query_choice) == 1: 	
		runQueryOne()
	
	# Query 2
	elif int(user_query_choice) == 2: 
		runQueryTwo()

	# Query 3
	elif int(user_query_choice) == 3: 
		runQueryThree()

	# Query 4
	elif int(user_query_choice) == 4: 
		runQueryFour()		

	# Query 5
	elif int(user_query_choice) == 5: 
		runQueryFive()

	# Query 6
	elif int(user_query_choice) == 6: 
		runQuerySix()

	# Query 7
	elif int(user_query_choice) == 7: 
		runQuerySeven()

	# 'Default' case, if all other if statements fail. 
	else: 
		print("\n\t'{}' was not a valid choice.".format(user_query_choice))
		continue

	# Check if the user would like to continue. If not, end the program.
	user_continue_choice = input("\n\tEnter 'E' if you would like to end. (Enter anything else to continue): ")
	print()
	if user_continue_choice.upper() == 'E': 
		print("\n\tProgram Ended.")
		end_of_program = True

print("\t**********************************************************************************")


