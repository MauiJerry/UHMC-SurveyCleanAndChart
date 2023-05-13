# UHMC-SurveyCleanAndChart
created for UHMC DataScience class 2023 Final Project
ICS 173 - Intro to Data Science - Univ of Hawaii Maui College
https://www.sis.hawaii.edu/uhdad/bwckctlg.p_disp_course_detail?cat_term_in=202210&inst_in=MAU&subj_code_in=ICS&crse_numb_in=173

Class was cooperating with NASA Harvest program to prototype a food security dashboard for Maui County
https://nasaharvest.org/
https://nasaharvest.org/news/nasa-harvest-expands-food-security-work-maui-county-hi-community-based-partners

Students and community volunteers (High School, etc) visited a selection of farms and used an app created by the HAVEST team to collect data and images. The app data was made available to the class for class use.  A snapshot of this data is in the file 20230423_survey_0.csv

The Final Project for the class was to simply to use some data source to create a graph. Use of the HAVEST data set was strongly recommended.

So here is my python program submission for the final.
surveyDataCleaning.py

It reads the csv into a dataframe
* changes some column names that are rather annoyingly long in the original.
* saves the renamed data to 20230423_survey_NewCol.csv
* extracts the Crop names entered for each survey response
* counts the occurances of the crops
* makes a bar-chart of the crop counts
* identify geographic clusters of rows identified with a FarmID
* save the resulting dataframe

Saving the intermediary files is done for development testing and possible use in follow on development.





