import psycopg2
import psycopg2.extras
from lxml import etree


# Create a connection with the database
connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

# Set up for XML parsing and querying
xml_file = 'drug-poisoning-mortality-data.xml'
parser = etree.XMLParser(ns_clean=True)
tree = etree.parse(xml_file, parser)

# **** HELPER QUERY FUNCTIONS ****

def getYearRangeForLeadingCauseOfDeath():
	'''
		Function to find the minimum and maximum years present in the 
		LeadingCauseOfDeath table so that the user can be given a range
		of years to pick from. 
	'''
	query_string = "SELECT MAX(year) FROM LeadingCauseOfDeath"
	cursor.execute(query_string)
	max_year = cursor.fetchall()[0][0]

	query_string = "SELECT MIN(year) FROM LeadingCauseOfDeath"
	cursor.execute(query_string)
	min_year = cursor.fetchall()[0][0]

	return (min_year, max_year)

def getYearRangeForNutrition(): 
	'''
		Function to find the minimum and maximum years present in the 
		Nutrition table so that the user can be given a range of years 
		to pick from.
	'''
	query_string = "SELECT MAX(yearstart) FROM Nutrition"
	cursor.execute(query_string)
	max_year = cursor.fetchall()[0][0]

	query_string = "SELECT MIN(yearstart) FROM Nutrition"
	cursor.execute(query_string)
	min_year = cursor.fetchall()[0][0]

	return (min_year, max_year)

def getNutritionStates(): 
	'''
		Function to get the states in the Nutrition table to 
		check for valid user input. 
	'''
	query_string = "SELECT DISTINCT locationdesc FROM Nutrition NATURAL JOIN location"
	cursor.execute(query_string)
	return cursor.fetchall()

def getTopicsForNutrition(): 
	'''
		Function to return the available topics in the 
		Nutrition dataset.
	'''
	query_string = "SELECT DISTINCT topicid, topic FROM Nutrition NATURAL JOIN TopicInformation"
	cursor.execute(query_string)
	return cursor.fetchall()

def getNutritionQuestionsForTopicID(topicid):
	'''
		Function that gets all the questions associated with a topicId 
		for the Nutrition table.
	'''
	query_string = "SELECT DISTINCT question, questionid FROM Nutrition NATURAL JOIN questioninformation WHERE topicid = %s"
	cursor.execute(query_string, (topicid,))
	return cursor.fetchall()

def getYearStartYearEndRangesCDI(): 
	'''
		Function to find the minimum and maximum years present in the 
		CDI table so that the user can pick a valid start year and end 
		year. 
	'''
	query_string = "SELECT MAX(yearstart) FROM ChronicDiseaseIndicator"
	cursor.execute(query_string)
	max_year_start = cursor.fetchall()[0][0]

	query_string = "SELECT MIN(yearstart) FROM ChronicDiseaseIndicator"
	cursor.execute(query_string)
	min_year_start = cursor.fetchall()[0][0]

	query_string = "SELECT MAX(yearend) FROM ChronicDiseaseIndicator"
	cursor.execute(query_string)
	max_year_end = cursor.fetchall()[0][0]

	query_string = "SELECT MIN(yearend) FROM ChronicDiseaseIndicator"
	cursor.execute(query_string)
	min_year_end = cursor.fetchall()[0][0]

	return (min_year_start, max_year_start, min_year_end, max_year_end)

def getCDIStates(): 
	'''
		Function to get the states in the CDI table to 
		check for valid user input. 
	'''
	query_string = "SELECT DISTINCT locationdesc FROM ChronicDiseaseIndicator NATURAL JOIN location"
	cursor.execute(query_string)
	return cursor.fetchall()

def getTopicsForCDI(): 
	'''
		Function to return the available topics in the 
		CDI dataset. 
	'''
	query_string = "SELECT DISTINCT topicid, topic FROM ChronicDiseaseIndicator NATURAL JOIN TopicInformation"
	cursor.execute(query_string)
	return cursor.fetchall()

def getCDIQuestionsForTopicID(topicid): 
	'''
		Function that gets all the questions associated with a topicId 
		for the ChronicDiseaseIndicator table.
	'''
	query_string = "SELECT DISTINCT question, questionid FROM ChronicDiseaseIndicator NATURAL JOIN questioninformation WHERE topicid = %s"
	cursor.execute(query_string, (topicid,))
	return cursor.fetchall()

def getDrugPoisoningYears(): 
	'''
		Function to get the valid year range for the drug poisoning 
		data. (Stored in an XML file).
	'''
	min_year = 9999 
	max_year = 0
	for year in tree.xpath('/DrugPoisoning/DrugPoisoningStatistic/Year'):
		year_int = int(year.text)
		if year_int < min_year: 
			min_year = year_int
		if year_int > max_year: 
			max_year = year_int
	return (min_year, max_year)	

def getDrugPoisoningStates(): 
	'''
		Function to get the valid state for the drug poisoning 
		data. (Stored in an XML file).
	'''
	state_list = []
	for state in tree.xpath('/DrugPoisoning/DrugPoisoningStatistic/State'): 
		if state.text not in state_list: 
			state_list.append(state.text)
	return state_list




# **** MAIN QUERY FUNCTIONS ****

def queryOne(year): 
	'''
		Function to run the first query option. 
		Input: year 
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query returns the cause of death that caused the most 
		deaths for each state during a given year. 
	'''
	query_string = """
					SELECT year as Year, state as State, causename as MaxCauseOfDeath, deaths as NumberOfDeaths
					FROM LeadingCauseOfDeath
					NATURAL JOIN 
					(
						SELECT state, MAX(deaths) AS max_deaths 
						FROM LeadingCauseOfDeath
						WHERE causename != 'All causes' and year = %s
						GROUP BY (state, year)
					) AS foo
					WHERE year = %s and deaths = max_deaths and state = foo.state
					ORDER BY state ASC;
					"""
	cursor.execute(query_string, (year, year))
	records = cursor.fetchall()
	return records

def queryTwo(year): 
	'''
		Function to run the second query option. 
		Input: year
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query gets the States and percent of people with no physical activity for states where
		30% of the population is considered overweight.
	'''
	query_string = """
						SELECT yearstart, locationdesc, overweight_value, activity_value
						FROM 
						(
							(
								SELECT yearstart, locationid, ROUND(100*(SUM(samplesize * datavalue/100) / SUM(samplesize)),3) AS activity_value
								FROM Nutrition 
								WHERE QuestionID = 'Q047' AND yearstart = %s AND yearend = %s and samplesize > 0
								GROUP BY (locationid, yearstart, QuestionID)
								ORDER BY locationid ASC
							) AS queryone
							NATURAL JOIN 
							(
								SELECT yearstart, locationid, ROUND(100*(SUM(samplesize * datavalue/100) / SUM(samplesize)),3) AS overweight_value
								FROM Nutrition 
								WHERE QuestionID = 'Q037' AND yearstart = %s AND yearend = %s and samplesize > 0
								GROUP BY (locationid, yearstart, QuestionID)
								ORDER BY locationid ASC
							) AS querythree
						) AS queryfour
						NATURAL JOIN 
						(
							SELECT locationid, locationdesc
							FROM location
						) AS querytwo
						WHERE queryfour.locationid = querytwo.locationid AND overweight_value > 35;
				   """
	cursor.execute(query_string, (year, year, year, year))
	records = cursor.fetchall()
	return records

def queryThree(year): 
	'''
		Function to run the third query option. 
		Input: year
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query gets the percent of people with no physical activity for states 
		where heart disease is the leading cause of death for a given year.
	'''
	query_string = """
						SELECT Year, State, MaxCauseOfDeath, no_activity_perc
						FROM
						(
							SELECT year as Year, state as State, causename as MaxCauseOfDeath
							FROM LeadingCauseOfDeath
							NATURAL JOIN 
							(
								SELECT state, MAX(deaths) AS max_deaths 
								FROM LeadingCauseOfDeath
								WHERE causename != 'All causes' and year = %s
								GROUP BY (state, year)
							) AS subquery
							WHERE year = %s and deaths = max_deaths and state = subquery.state and causename = 'Heart disease'
						) as MainQueryOne
						NATURAL JOIN 
						(
							SELECT yearstart AS Year, locationdesc AS State, no_activity_perc
							FROM
							(
								SELECT yearstart, locationid, ROUND(100*(SUM(samplesize * datavalue/100) / SUM(samplesize)),3) AS no_activity_perc
								FROM Nutrition 
								WHERE QuestionID = 'Q047' AND yearstart = %s AND yearend = %s and samplesize > 0
								GROUP BY (locationid, yearstart, QuestionID)
								ORDER BY locationid ASC
							) AS subqueryone
							NATURAL JOIN 
							(
								SELECT locationid, locationdesc
								FROM location
							) AS subquerytwo
						) AS MainQueryTwo;
				   """
	cursor.execute(query_string, (year, year, year, year))
	records = cursor.fetchall()
	return records

def queryFour(yearstart, yearend, state, questionid): 
	'''
		Function to run the fourth query option. 
		Input: yearstate, yearend, state, questionId
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query provides the statistics from the CDI data for each 
		stratification for a given question, state, and year range.
	'''
	query_string = """
						SELECT DISTINCT StratificationCategory1, Stratification1, DataValueUnit, DataValueType, DataValue
						FROM  ChronicDiseaseIndicator NATURAL JOIN StratificationInformation NATURAL JOIN DataValueTypeInformation NATURAL JOIN Location
						WHERE YearStart = %s and YearEnd = %s and LocationDesc = %s and questionID = %s and datavalue != '-1';
				   """
	cursor.execute(query_string, (yearstart, yearend, state, questionid))
	return cursor.fetchall()

def queryFive(year, state, questionid): 
	'''
		Function to run the fifth query option. 
		Input: year, state, questionId
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query provides the statistics from the Nutrition data for each 
		stratification for a given question, state, and year range.
	'''
	query_string = """
						SELECT DISTINCT StratificationCategory1, Stratification1, DataValueUnit, DataValueType, DataValue
						FROM  Nutrition NATURAL JOIN StratificationInformation NATURAL JOIN DataValueTypeInformation NATURAL JOIN Location
						WHERE YearStart = %s and LocationDesc = %s and questionID = %s and datavalue > -1;
				   """
	cursor.execute(query_string, (year, state, questionid))
	return cursor.fetchall()

def querySix(year): 
	'''
		Function to run the sixth query option. 
		Input: year
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query returns the states where more than 30% of people get 
		no exercise, along with the leading cause of death statistics for 
		those states (for a given year).
	'''
	query_string = """
						SELECT * FROM 
						(
							SELECT yearstart AS Year, locationdesc AS State, no_activity_perc
							FROM
							(
								SELECT yearstart, locationdesc, ROUND(100*(SUM(samplesize * datavalue/100) / SUM(samplesize)),3) AS no_activity_perc
								FROM Nutrition NATURAL JOIN location
								WHERE QuestionID = 'Q047' AND yearstart = %s AND yearend = %s and samplesize > 0
								GROUP BY (locationdesc, yearstart, QuestionID)
								ORDER BY locationdesc ASC
							) AS subqueryone
							WHERE no_activity_perc > 30
						) AS mainone
						NATURAL JOIN 
						(
							SELECT Year, CauseNameExpanded, State, Deaths, AgeAdjustedDeathRate
							FROM LeadingCauseOfDeath NATURAL JOIN Cause
							WHERE Year = %s
						) AS maintwo
						ORDER BY (State, CauseNameExpanded);
				   """

	cursor.execute(query_string, (year, year, year))
	records = cursor.fetchall()
	return records

def querySeven(user_year, user_state): 
	'''
		Function to run the seventh query option. 
		Input: user_year, user_state
		Output: The results of running the query in the 
		form of a list of rows(lists).

		The query returns drug poisioning statistics for 
		a user provided year and state. 
	'''
	
	#List of rows(lists)
	results = []
	row = []

	for stat in tree.xpath('/DrugPoisoning/DrugPoisoningStatistic'): 
		year = stat.find('Year').text
		state = stat.find('State').text

		if int(year) == int(user_year) and state.lower() == user_state.lower(): 
			upper_age = stat.find('AgeRange').find('UpperBound').text
			lower_age = stat.find('AgeRange').find('LowerBound').text
			sex = stat.find('Sex').text
			Race = stat.find('Race').text
			deaths = stat.find('Deaths').text
			population = stat.find('Population').text
			row = []
			row.append(sex)
			row.append(Race)
			row.append("{}-{}".format(lower_age, upper_age))
			row.append(deaths)
			row.append(population)
			row.append(round(int(deaths)*100/int(population), 8))
			results.append(row)
	return results

