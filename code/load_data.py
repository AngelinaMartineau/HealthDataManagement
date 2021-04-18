import csv
import psycopg2
import psycopg2.extras
from psycopg2 import sql
from xml.dom import minidom


# ***************** HELPER FUNCTIONS *****************
def splitAge(age): 
	'''
	Function to take an age range (e.g. 15-24 years) and split it 
	into an upper and lower bound. Returns a tuple formatted as: 
	(lowerbound, upperbound)
	NOTE: Using  150 as the max age (for phrases like "75+ years")
	'''
	upperbound = 150
	lowerbound = 0 

	# Case where two numbers are separated by a dash (15-24)
	if age[0].isdigit() and age[1].isdigit() and age[2] == '-':
		lowerbound = int(age[0] + age[1])
		upperbound = int(age[3] + age[4])
	# Case where one number is followed by a plus size (65+)
	if age[0].isdigit() and age[1].isdigit() and age[2] == '+':
		lowerbound = int(age[0] + age[1])
	# Case where a number is preceeded by "less than" (Less than 15)
	if age[:9] == "Less than": 
		if age[10].isdigit() and age[11].isdigit(): 
			upperbound = int(age[10] + age[11])
		elif age[10]: 
			upperbound = int(age[10])

	return (lowerbound, upperbound)


# ***************** FILENAMES *****************
# These CSV files need to be in the same directory as this load_data.py file
drug_poisoning_file = "datasets/NCHS_-_Drug_Poisoning_Mortality_by_State__United_States.csv"
leading_causes_of_death_file = "datasets/NCHS_-_Leading_Causes_of_Death__United_States.csv"
nutrition_file = "datasets/Nutrition__Physical_Activity__and_Obesity_-_Behavioral_Risk_Factor_Surveillance_System.csv"
chronic_disease_indicators_file = "datasets/U.S._Chronic_Disease_Indicators__CDI_.csv"


# ***************** General Set Up *****************
connection_string = "host='localhost' dbname='dbms_final_project' user='dbms_project_user' password='dbms_password'"
conn = psycopg2.connect(connection_string)
cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


# ***************** Use the schema file to set up the database *****************
cursor.execute(open("schema.sql", "r").read())


# ***************** LOAD DATA FROM LEADING_CAUSES_OF_DEATH FILE *****************
count = 0 
insert_query = ""
with open(leading_causes_of_death_file) as leading_causes_of_death: 
	leading_causes_of_death_reader = csv.reader(leading_causes_of_death, delimiter=",")
	for row in leading_causes_of_death_reader: 
		if count > 0: 

			#Add values to Cause table: 
			insert_query = "INSERT INTO Cause(CauseName, CauseNameExpanded) VALUES (%s, %s) ON CONFLICT DO NOTHING"	
			cursor.execute(insert_query, (row[2], row[1]))

			#Add values to LeadingCauseOfDeath table: 
			insert_query = """INSERT INTO LeadingCauseOfDeath(Year, CauseName, State, Deaths, AgeAdjustedDeathRate) 
						VALUES (%s, %s, %s, %s, %s) ON CONFLICT DO NOTHING"""	
			cursor.execute(insert_query, (int(row[0]), row[2], row[3], int(row[4]), float(row[5])))

		count += 1	
print("Leading Causes of Death: ", count)


# ***************** LOAD DATA FROM NUTRITION FILE *****************
count = 0 
insert_query = ""
with open(nutrition_file) as nutrition: 
	nutrition_reader = csv.reader(nutrition, delimiter=",")
	for row in nutrition_reader: 
		if count > 0: 

			#Add values to Location table: 
			insert_query = "INSERT INTO Location(LocationID, LocationAbbr, LocationDesc) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING" 
			cursor.execute(insert_query, (row[28], row[2], row[3]))
				
			#Add values to TopicInformation table: 
			insert_query = "INSERT INTO TopicInformation(TopicID, Topic) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[25], row[6]))

			#Add values to QuestionInformation table: 
			insert_query = "INSERT INTO QuestionInformation(QuestionId, Question) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[26], row[7]))

			#Add values to ClassInformation table: 
			insert_query = "INSERT INTO ClassInformation(ClassID, Class) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[24], row[5]))

			#Add values to DataValueTypeInformation table:
			insert_query = "INSERT INTO DataValueTypeInformation(DataValueTypeID, DataValueType) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[27], row[9]))

			#Add values to StratificationInformation table: 
			insert_query = """INSERT INTO StratificationInformation(StratificationID1, StratificationCategoryID1,
								 Stratification1, StratificationCategory1) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"""
			cursor.execute(insert_query, (row[32], row[31], row[30], row[29]))

			# Check for null values for float and int values
			if row[0] == "":
				row[0] = 0 
			if row[1] == "":
				row[1] = 0 
			if row[14] == "": 
				row[14] = -1
			if row[10] == "":
				row[10] = -1
			if row[15] == "":
				row[15] = -1
			if row[16] == "":
				row[16] = 0 
			if row[28] == "":
				row[28] = 0 

			# Insert the main row data into the Nutrition table
			insert_query = """INSERT INTO Nutrition(YearStart, YearEnd, DataSource, DataValueUnit, DataValue, DataValueFootnoteSymbol, 
			DataValueFootnote, LowConfidenceLimit, HighConfidenceLimit, SampleSize, GeoLocation, ClassID, TopicID, DataValueTypeID, 
			StratificationID1, QuestionID, LocationID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
			ON CONFLICT DO NOTHING"""
			cursor.execute(insert_query, (int(row[0]), int(row[1]), row[4], row[8], float(row[10]), row[12], row[13], float(row[14]), 
				float(row[15]), int(row[16]), row[23], row[24], row[25], row[27], row[32], row[26], int(row[28])))

		count += 1
print("Nutrition: ", count)


# ***************** LOAD DATA FROM CHRONIC DISEASE INDICATORS FILE *****************
count = 0 
location_dict = dict()
topic_info_dict = dict()
question_info_dict = dict()
data_value_dict = dict()
strat_info_dict = dict()
insert_query = ""
with open(chronic_disease_indicators_file) as chronic_disease_indicators: 
	chronic_disease_indicators_reader = csv.reader(chronic_disease_indicators, delimiter=",")
	for row in chronic_disease_indicators_reader: 
		if count > 0:

			#Add values to Location table: 
			insert_query = "INSERT INTO Location(LocationID, LocationAbbr, LocationDesc) VALUES (%s, %s, %s) ON CONFLICT DO NOTHING" 
			cursor.execute(insert_query, (row[24], row[2], row[3]))

			#Add values to TopicInformation table: 
			insert_query = "INSERT INTO TopicInformation(TopicID, Topic) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[25], row[5]))

			#Add values to QuestionInformation table: 
			insert_query = "INSERT INTO QuestionInformation(QuestionID, Question) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[26], row[6]))

			#Add values to DataValueTypeInformation table: 
			insert_query = "INSERT INTO DataValueTypeInformation(DataValueTypeID, DataValueType) VALUES (%s, %s) ON CONFLICT DO NOTHING"
			cursor.execute(insert_query, (row[27], row[9]))

			#Add values to StratificationInformation table: 
			insert_query = """INSERT INTO StratificationInformation(StratificationID1, StratificationCategoryID1,
								 Stratification1, StratificationCategory1) VALUES (%s, %s, %s, %s) ON CONFLICT DO NOTHING"""
			cursor.execute(insert_query, (row[29], row[28], row[17], row[16]))

			# Check for null values for float and int values
			if row[0] == "":
				row[0] = 0 
			if row[1] == "":
				row[1] = 0 
			if row[14] == "": 
				row[14] = -1
			if row[11] == "":
				row[11] = -1
			if row[15] == "":
				row[15] = -1
			if row[24] == "":
				row[24] = 0 

			# Insert the main row data into the ChronicDiseaseIndicator table
			insert_query = """INSERT INTO ChronicDiseaseIndicator(YearStart, YearEnd, DataSource, DataValueUnit, DataValue, 
			DataValueAlt, DataValueFootnoteSymbol, DataValueFootnote, LowConfidenceLimit, HighConfidenceLimit, GeoLocation, TopicID, 
			StratificationID1, DataValueTypeID, QuestionID, LocationID) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
			ON CONFLICT DO NOTHING"""
			cursor.execute(insert_query, (int(row[0]), int(row[1]), row[4], row[8], row[10], float(row[11]), row[12], row[13], float(row[14]), 
				float(row[15]), row[22], row[25], row[29], row[27], row[26], int(row[24])))
		count += 1
print("Chronic Disease Indicators: ", count)


conn.commit()
# ***************** END OF RELATIONAL DATABASE *****************



# ***************** LOAD DATA FROM DRUG_POISONING FILE *****************
# ************ NON RELATIONAL DATABASE - WRITE AN XML FILE *************
root = minidom.Document()
xml = root.createElement('DrugPoisoning')
root.appendChild(xml)
count = 0 

with open(drug_poisoning_file, encoding = "utf-8") as drug_poisoning: 
	drug_poisoning_reader = csv.reader(drug_poisoning, delimiter = ",")
	for row in drug_poisoning_reader: 
		if count != 0: 

			#insert -1 for missing data
			for i in range(len(row)): 
				if row[i] == "":
					row[i] = "-1"
			
			# Create the root element
			drugPoisoningStatistic = root.createElement('DrugPoisoningStatistic')

			# Add year to the root element
			year = root.createElement('Year')
			year.appendChild(root.createTextNode(row[0]))
			drugPoisoningStatistic.appendChild(year)

			# Add sex to the root element
			sex = root.createElement('Sex')
			sex.appendChild(root.createTextNode(row[1]))
			drugPoisoningStatistic.appendChild(sex)

			# Create an AgeRange element that will have lowerbound and upperbound 
			# as child elements. Then add AgeRange element to root element. 
			ageRange = root.createElement('AgeRange')
			lowerBound = root.createElement('LowerBound')
			upperBound = root.createElement('UpperBound')
			lower, upper = splitAge(row[2])
			lowerBound.appendChild(root.createTextNode(str(lower)))
			upperBound.appendChild(root.createTextNode(str(upper)))
			ageRange.appendChild(lowerBound)
			ageRange.appendChild(upperBound)
			drugPoisoningStatistic.appendChild(ageRange)

			# Add race to the root element
			race = root.createElement('Race')
			race.appendChild(root.createTextNode(row[3]))
			drugPoisoningStatistic.appendChild(race)

			# Add State to the root element
			state = root.createElement('State')
			state.appendChild(root.createTextNode(row[4]))
			drugPoisoningStatistic.appendChild(state)

			# Add deaths to the root element
			deaths = root.createElement('Deaths')
			deaths.appendChild(root.createTextNode(row[5]))
			drugPoisoningStatistic.appendChild(deaths)

			# Add population to the root element
			population = root.createElement('Population')
			population.appendChild(root.createTextNode(row[6]))
			drugPoisoningStatistic.appendChild(population)

			# Add DeathRate element to root element. The DeathRate
			# contains child elements with information about the 
			# DeathRate.
			deathRate = root.createElement('DeathRate')
			deathRate.appendChild(root.createTextNode(row[7]))
			stderr = root.createElement('Stderr')
			stderr.appendChild(root.createTextNode(row[8]))
			lowConfidenceLimit = root.createElement('LowConfidenceLimit')
			lowConfidenceLimit.appendChild(root.createTextNode(row[9]))
			upperConfidenceLimit = root.createElement('UpperConfidenceLimit')
			upperConfidenceLimit.appendChild(root.createTextNode(row[10]))
			lower,upper = "-1","-1"
			if row[15] != "-1":
				lower,upper = row[15].split('–')
			stateRateLowerBound = root.createElement('StateRateLowerBound')
			stateRateLowerBound.appendChild(root.createTextNode(lower))
			stateRateUpperBound = root.createElement('StateRateUpperBound')
			stateRateUpperBound.appendChild(root.createTextNode(upper))
			usRate = root.createElement('USRate')
			usRate.appendChild(root.createTextNode(row[16]))
			crude = root.createElement("Crude")
			crude.appendChild(deathRate)
			crude.appendChild(stderr)
			crude.appendChild(lowConfidenceLimit)
			crude.appendChild(upperConfidenceLimit)
			crude.appendChild(stateRateLowerBound)
			crude.appendChild(stateRateUpperBound)
			crude.appendChild(usRate)
			drugPoisoningStatistic.appendChild(crude)

			# Add AdjustedRate to the root element. The AdjustedRate 
			# contains child elements with information about the 
			# adjusted rate. 
			adjustedRate = root.createElement('AdjustedRate')
			adjustedRate.appendChild(root.createTextNode(row[11]))
			stderr = root.createElement('Stderr')
			stderr.appendChild(root.createTextNode(row[12]))
			lowConfidenceLimit = root.createElement('LowConfidenceLimit')
			lowConfidenceLimit.appendChild(root.createTextNode(row[13]))
			upperConfidenceLimit = root.createElement('UpperConfidenceLimit')
			upperConfidenceLimit.appendChild(root.createTextNode(row[14]))
			usRate = root.createElement('USRate')
			usRate.appendChild(root.createTextNode(row[17]))
			ageInfo = root.createElement('AgeInfo')
			ageInfo.appendChild(adjustedRate)
			ageInfo.appendChild(stderr)
			ageInfo.appendChild(lowConfidenceLimit)
			ageInfo.appendChild(upperConfidenceLimit)
			ageInfo.appendChild(usRate)
			drugPoisoningStatistic.appendChild(ageInfo)

			#Add the entire 'row' of data to the XML element.
			xml.appendChild(drugPoisoningStatistic)

		count += 1 

print("Drug Poisoning: ", count)

# Write the XML element to an XML file
xml_str = root.toprettyxml(indent="\t", encoding="utf-8")
xml_file = "drug-poisoning-mortality-data.xml"
with open(xml_file, "wb") as out_file: 
	out_file.write(xml_str)