/* 
	Angelina Martineau
	Final Project Schema 
*/

/**** Tables for Leading Causes of Death Data ****/
CREATE TABLE IF NOT EXISTS Cause(
	CauseName VARCHAR(63) NOT NULL,
	CauseNameExpanded VARCHAR(127), 
	PRIMARY KEY (CauseName)
);

CREATE TABLE IF NOT EXISTS LeadingCauseOfDeath(
	Year SMALLINT NOT NULL,
	CauseName VARCHAR(63) NOT NULL,
	State VARCHAR(63) NOT NULL,
	Deaths INT,
	AgeAdjustedDeathRate NUMERIC(7,1), 
	PRIMARY KEY (Year, State, CauseName),
	FOREIGN KEY (CauseName) REFERENCES Cause(CauseName)
);

/**** Tables shared by Chronic Disease Indicators Data and Nutrition Data ****/
CREATE TABLE IF NOT EXISTS Location(
	LocationID INT,
	LocationAbbr CHAR(2), 
	LocationDesc VARCHAR(31),
	PRIMARY KEY (LocationID)
);

CREATE TABLE IF NOT EXISTS TopicInformation(
	TopicID VARCHAR(31),
	Topic VARCHAR(63),
	PRIMARY KEY(TopicID)
);

CREATE TABLE IF NOT EXISTS QuestionInformation(
	QuestionID VARCHAR(31), 
	Question VARCHAR(255), 
	PRIMARY KEY(QuestionID)
);

CREATE TABLE IF NOT EXISTS DataValueTypeInformation(
	DataValueTypeID VARCHAR(31), 
	DataValueType VARCHAR(127), 
	PRIMARY KEY(DataValueTypeID)
);

CREATE TABLE IF NOT EXISTS StratificationInformation(
	StratificationID1 VARCHAR(31),
	StratificationCategoryID1 VARCHAR(31),
	Stratification1 VARCHAR(63),
	StratificationCategory1 VARCHAR(31),
	PRIMARY KEY(StratificationID1)
);


/**** Tables for Chronic Disease Indicators Data ****/
CREATE TABLE IF NOT EXISTS ChronicDiseaseIndicator(
	YearStart SMALLINT, 
	YearEnd SMALLINT, 
	DataSource VARCHAR(63), 
	DataValueUnit VARCHAR(31), 
	DataValue VARCHAR(127),  /*Value can be numeric or string*/
	DataValueAlt NUMERIC(8,1), 
	DataValueFootnoteSymbol VARCHAR(31), 
	DataValueFootnote TEXT,  
	LowConfidenceLimit NUMERIC(8,1), 
	HighConfidenceLimit NUMERIC(8,1), 
	GeoLocation VARCHAR(63),
	TopicID VARCHAR(31) REFERENCES TopicInformation(TopicID), 
	StratificationID1 VARCHAR(31) REFERENCES StratificationInformation(StratificationID1), 
	DataValueTypeID VARCHAR(31) REFERENCES DataValueTypeInformation(DataValueTypeID), 
	QuestionID VARCHAR(31) REFERENCES QuestionInformation(QuestionID),
	LocationID INT,
	PRIMARY KEY(YearStart, YearEnd, LocationID, QuestionID, StratificationID1),
	FOREIGN KEY(TopicID) REFERENCES TopicInformation(TopicID), 
	FOREIGN KEY(LocationID) REFERENCES Location(LocationID), 
	FOREIGN KEY(QuestionID) REFERENCES QuestionInformation(QuestionID),
	FOREIGN KEY(StratificationID1) REFERENCES StratificationInformation(StratificationID1)
);


/**** Tables for Nutrition Data ****/
CREATE TABLE IF NOT EXISTS ClassInformation(
	ClassID VARCHAR(31), 
	Class VARCHAR(31), 
	PRIMARY KEY(ClassID) 
);

CREATE TABLE IF NOT EXISTS Nutrition(
	YearStart SMALLINT, 
	YearEnd SMALLINT, 
	DataSource VARCHAR(63), 
	DataValueUnit VARCHAR(31),
	DataValue NUMERIC(7,1), 
	DataValueFootnoteSymbol VARCHAR(31), 
	DataValueFootnote TEXT, 
	LowConfidenceLimit NUMERIC(7,1), 
	HighConfidenceLimit NUMERIC(7,1), 
	SampleSize INT, 
	GeoLocation VARCHAR(63), 
	ClassID VARCHAR(31) REFERENCES ClassInformation(ClassID), 
	TopicID VARCHAR(31)  REFERENCES TopicInformation(TopicID), 
	DataValueTypeID VARCHAR(31) REFERENCES DataValueTypeInformation(DataValueTypeID), 
	StratificationID1 VARCHAR(31) REFERENCES StratificationInformation(StratificationID1), 
	QuestionID VARCHAR(31) REFERENCES QuestionInformation(QuestionID),
	LocationID INT,
	PRIMARY KEY(YearStart, YearEnd, LocationID, QuestionID, StratificationID1),
	FOREIGN KEY(LocationID) REFERENCES Location(LocationID), 
	FOREIGN KEY(QuestionID) REFERENCES QuestionInformation(QuestionID)
);

/**** Tables for Drug Poisioning Mortality Data ****/
/* NOTE: This table is no longer needed, as the data is in an XML file */
-- CREATE TABLE DrugPoisioningMortality(
-- 	Year SMALLINT,
-- 	Sex VARCHAR(15), 
-- 	LowerBoundAge INT,
-- 	UpperBoundAge INT, 
-- 	RaceHispanicOrigin VARCHAR(31), 
-- 	State VARCHAR(31), 
-- 	Deaths INT,
-- 	Population INT, 
-- 	CrudeDeathRate NUMERIC(4,1),
-- 	StderrCrudeRate NUMERIC(4,1),
-- 	LowConfidenceLimitCrude NUMERIC(4,1),
-- 	UpperConfidenceLimitCrude NUMERIC(4,1),
-- 	AgeAdjustedRate NUMERIC(4,1),
-- 	StderrAgeAdjustedRate NUMERIC(4,1),
-- 	LowConfidenceLimitAge NUMERIC(4,1),
-- 	UpperConfidenceLimitAge NUMERIC(4,1),
-- 	StateCrudeRateInRangeLowerBound NUMERIC(4,1),
-- 	StateCrudeRateInRangeUpperBound NUMERIC(4,1),
-- 	USCrudeRate NUMERIC(4,1),
-- 	USAgeAdjustedRate NUMERIC(4,1),
-- 	PRIMARY KEY(Year, Sex, LowerBoundAge, UpperBoundAge, RaceHispanicOrigin, State)
-- );