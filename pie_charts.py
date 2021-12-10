#This code graphs pie charts for closed multiple choice type questions

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

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

#mc_data.info()

#Question 1
q1 = mc_data['Question 1'].value_counts(normalize = True) #normalize = True turns the count into percentages
q1 = pd.DataFrame(q1).reset_index() #change to dataframe and reset index
q1.columns = ['answer', 'percent'] #change name of columns
colors = ['#203864', '#4472c4', '#8faadc', '#b4c7e7', '#9dc3e6', '#e3877d', '#c00000', '#a5a5a5']

plt.pie(q1['percent'], labels = q1['answer'], colors = colors)
plt.show()

def pie_chart(df):
    for column in df:
        q = df[column].value_counts(normalize = True) 
        q = pd.DataFrame(q).reset_index()
        q.columns = ['answer', 'percent']
        colors = ['#203864', '#4472c4', '#8faadc', '#b4c7e7', '#9dc3e6', '#e3877d', '#c00000', '#a5a5a5']
        
        plt.pie(q['percent'], labels = q['answer'], colors = colors)
        plt.title(column)
        plt.show()

pie_chart(mc_data)