# ITWS Database Systems and Applications Final Project: Health Data Management

Author: Angelina Martineau  
Topic: Health Data

## Project Description

This project was completed as a final assignment for my Database Systems and Applications course in the Fall of 2020. The project involved finding data sources, creating a normalized schema for the data, and developing an application that allowed a user to explore the data. 

The assigment requested that at least one dataset be represented by a non-relational database, while the rest were to be stored in a relational database. Therefore, postgreSQL was used to develop a relational database, and XML was used to develop a non-relational database. The breakdown of where data from each data source is stored is shown below: 
- Relational Database (PostgreSQL)
	- Leading Causes of Death Data
	- Nutrition Data
	- Chronic Disease Indicator Data
- Non-Relational Database (XML)
	- Drug Poisoning Data

Python 3.6 was used to access and fill the databases, as well as develop the application. 

## Directory Structure 

The outermost folder contains all the files necessary to run 
this application. The following files and folders are present 
in this folder:  
- retrieve_data.py
- db-setup.sql
- code (folder)

Inside the *code* folder, the following files exist: 
- datasets.txt
- schema.sql
- drug-poisoning-mortality-schema.xsd
- load_data.py
- Application.py
- Database.py

## Setting up the Database 

In order to set up the database, run the following command: 
	
	psql -U postgres postgres < db-setup.sql

This will set up a database with name 'dbms_final_project', user 'dbms_project_user',  and password 'dbms_password'. 

## Loading the data

First, *retrieve_data.py* needs to be run: 

	python retrieve_data.py

This will use the links in *datasets.txt* to retrieve the raw data files, and it will place them in a new folder called *datasets*. If this folder already exists, it will be cleared before the datasets are added. 

Next, *load_data.py* needs to be run: 

	python load_data.py

This will populate the PostgreSQL database with the data from the four CSV files in the *datasets* folder. The *schema.sql* file will be run from *load_data.py*, and it will only create the tables if they don't already exist. The *load_data.py* file will also create and populate an XML file (non-relational database) titled *drug-poisoning-mortality-data.xml* in the code file.

**NOTE:** Running load_data.py will take several minutes due to the size of one of the data files (800,000+ rows).

## Running the Application

To run the application, the file *Application.py* needs to be run from the command-line.

	python Application.py

This will begin the program in the command terminal, and from there the program will prompt for user input.

## Notes about the XML file 

The file *drug-poisoning-mortality-data.xml* will be created by running the *load_data.py* file *load_data.py* will take the data from the drug poisoning CSV file and add it to a newly created *drug-poisoning-mortality-data.xml* file. This file will be stored in the main project folder (i.e., the same location as the *load_data.py* file). The XML Schema File, *drug-poisoning-mortality-schema.xsd*, is also stored in this directory. 

During the development of the project, an XML validator file, written by the course professor, was used to ensure that the XML data file developed fit the XML schema defined. 

The user does not need to take any extra actions to handle the XML file. All work will be done by *load_data.py*.

Query 7 in the main application accesses the data in the XML file. 
