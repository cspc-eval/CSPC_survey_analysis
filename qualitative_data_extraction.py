#This code takes raw survey data csv as an input and open-ended survey questions (qualitative data) as a csv output for manual analysis

#import packages
import pandas as pd

#read in exit survey data
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

#read in q_type.csv which has the type of questions for the survey
q_type = pd.read_csv("q_type.csv", encoding = 'utf-8')


#select questions with open-ended questions for qualitative analysis; where q_type['type_1'] == open
qual_q = q_type[q_type['type_1'] == 'open']
#select first column to get a list of column names of 'survey_raw' for open-ended questions
qual_q_list = qual_q['question'].tolist()


#create a subset of data for qualitative data to be analyzed manually
qual_data = survey_raw[survey_raw.columns.intersection(qual_q_list)]

qual_data.to_csv("qualitatitive_data.csv")



