# **MediCheck - Clinic Service Management System**
**project demo** is available on my portfolio: https://haneyoshi.github.io/ **


## Table of Contents
1.Introduction
2.Requirements
3.Setup Instructions
4.Install Required Tools
5.Setup the Python Environment
6.Set Up the Database
7.Running the System
8.Sample Data Population

## 1.Introduction
MediCheck is a clinic service management system designed to streamline medical workflows with features such as real-time symptom suggestions, disease predictions, and medicine recommendations. This guide explains how to set up and run the program, including instructions for installing required tools and creating the necessary database environment.

## 2.Requirements
To run MediCheck, you will need:
Python 3.8 or higher
MySQL Community Server
MySQL Workbench (optional but recommended for database management)
Python libraries:
pandas
mysql-connector-python

## 3.Setup Instructions
### 3-1.Install Required Tools
Follow these steps to install the tools necessary for MediCheck:
Python 3.8+:
Download and install Python from https://www.python.org/downloads/.
Ensure pip (Python's package installer) is included.
MySQL Community Server:
Download and install the MySQL Community Server from https://dev.mysql.com/downloads/mysql/.
During installation, set a root password that will be used later for database setup.
MySQL Workbench (optional):
Download and install MySQL Workbench from https://dev.mysql.com/downloads/workbench/.
This tool is recommended for managing your database visually.
### 3-2.Setup the Python Environment
Install Required Libraries: Open a terminal and run the following commands to install the necessary Python libraries:
pip install pandas
pip install mysql-connector-python
Verify Installation: Ensure the libraries are installed correctly:
python -m pip show pandas mysql-connector-python
### 3-3.Set Up the Database
Step 1: Create a New Database
Open MySQL Workbench or log into your MySQL server using the command line.
Create a new database by running the following command in the MySQL client:
CREATE DATABASE medi_check;
The database name medi_check is predefined in the CreateTable.py script. Ensure the name matches.
Step 2: Run the CreateTable.py Script

Execute the CreateTable.py module to create the necessary tables in the database:
python CreateTable.py
This script uses the predefined database name medi_check and creates all required tables for the system.
Step 3: Populate Sample Data

Run the RandomDataPopulation.py script to insert sample data into the database:
python RandomDataPopulation.py
This will add random data for testing purposes, including:
Sample patient records
Symptom entries
Diseases and associated medicines

## 4.Running the System
Start the main program by executing the Main.py script:
python Main.py
Follow the on-screen instructions to navigate through the system’s features, such as:
Adding new patients
Inputting symptoms and receiving suggestions
Viewing predicted diseases and recommended medications

## 5.Sample Data Population (Optional)
If you want to customize the data:
Edit the RandomDataPopulation.py script to define your custom data for patients, symptoms, diseases, and medicines.
Re-run the script after making changes:
python RandomDataPopulation.py

## 6.Additional Notes
If you encounter database connection issues, ensure the credentials in your Python scripts match your MySQL server's configuration (e.g., username, password, and host details).
The Main.py script will not function without the database and tables being set up correctly. Ensure CreateTable.py and RandomDataPopulation.py are run successfully before starting the system.
