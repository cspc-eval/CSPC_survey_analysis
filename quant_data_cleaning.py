#This code takes raw survey data csv as an input and splits the quantitative data into three subsets (multiple choice, nominal/rank, and multiple answers)


#import packages
import pandas as pd

#read in exit survey data
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

#read in q_type.csv which has the type of questions for the survey
q_type = pd.read_csv("q_type.csv", encoding = 'utf-8')
   
   
#subsets of quantitative dataset-----------
#the quantitative dataset will be divided up further into three different csvs
        #1) closed, multiple choice answers
        #2) closed, nominal/ranked answers
        #3) closed, multiple answers

    #for subset csv #1 (mc_data.csv)
    #select data with type2 in q_type.csv as 'mc' to select closed, multiple choice answers
mc_q = q_type[q_type['type_2'] == 'mc']
    #select first column to get a list of column names of 'survey_raw' for open-ended questions
mc_q_list = mc_q['question'].tolist()
mc_data = survey_raw[survey_raw.columns.intersection(mc_q_list)]


    #for subset csv #2 (rank_data.csv)
    #select data with type2 in q_type.csv as 'nominal' to select closed, nominal or ranked answers
nominal_q = q_type[q_type['type_2'] == 'nominal']
    #select first column to get a list of column names of 'survey_raw' for open-ended questions
nominal_q_list = nominal_q['question'].tolist()
nominal_data = survey_raw[survey_raw.columns.intersection(nominal_q_list)]

    #for subset csv #3 (multi_answer_data.csv)
    #select data with type2 in q_type.csv as 'multi-answer' to select closed, multi-selection answers
multia_q = q_type[q_type['type_2'] == 'multi-answer']
    #select first column to get a list of column names of 'survey_raw' for open-ended questions
multia_q_list = multia_q['question'].tolist()
multia_data = survey_raw[survey_raw.columns.intersection(multia_q_list)]


