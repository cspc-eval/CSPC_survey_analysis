#This code graphs pie charts for closed multiple choice type questions

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import os

### Define helper functions 

def convert_percent(survey_raw, question):
    """
    This function will take the raw data and create a dataframe with a summary of data showing the percentages of each answer.
    The function will return a pandas dataframe.
    """
    df = survey_raw[question].value_counts(normalize = True) 
    df = pd.DataFrame(df).reset_index()
    df.columns = ['answer', 'percent']
    print('Current Question: {}'.format(question))
    df1 = survey_raw[question].value_counts()
    df1 = pd.DataFrame(df1).reset_index()
    df1.columns = ['answer', 'values']    
    print('Total responses (N): {}'.format(df1['values'].sum()))
    df['percent'] = df['percent']*100
    return df

def convert_values(survey_raw, question):
    """
    This function will take the raw data and create a dataframe with a summary of data showing the values of each answer.
    The function will return a pandas dataframe.
    """
    df = survey_raw[question].value_counts() 
    df = pd.DataFrame(df).reset_index()
    df.columns = ['answer', 'values']
    print('Current Question: {}'.format(question))
    print('Total responses (N): {}'.format(df['values'].sum()))
    return df    


def convert_values_per_capita(survey_raw, question):
    """
    This function will take the raw data and create a dataframe with a summary of data showing the values of each answer.
    The function will return a pandas dataframe.
    """
    df = survey_raw[question].value_counts() 
    df = pd.DataFrame(df).reset_index()
    df.columns = ['answer', 'values']
    print('Current Question: {}'.format(question))
    print('Total responses (N): {}'.format(df['values'].sum()))
    df = df.drop(2) #Drop value outside Canada
    pop =[23546417, 7031370, 2480826, 5249635, 128199] # population of Central Canada (ON, QC),  Prairie Provinces (AB, SK, MB),  
    #Atlantic Canada (NB, NL, NS, PE), West Coast (BC), Northern Territories (NT, NU, YT)   (Source Q42021: https://www150.statcan.gc.ca/t1/tbl1/en/tv.action?pid=1710000901)
    df['percent']=(df['values']/pop)
    return df   


def pie_chart(df, question):
    """
    This function creates pie charts from dataframes (df), and question number as an input  
    """
    
    colors = ['#203864', '#4472c4','#a5a5a5','#e3877d', '#8faadc', '#b4c7e7',  '#9dc3e6','#c00000']
    fig = plt.figure(figsize = [6,10])
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])    
    patches, texts, pcts = ax.pie(df['percent'], colors = colors, autopct='%1.0f%%',startangle=90, pctdistance=1.1)
    plt.legend(df['answer'], loc="center left", bbox_to_anchor=(1,0.5), fontsize=14) 
    plt.setp(pcts, fontweight='bold')
#    plt.show()
    name = question + '.png'
    fig.savefig(name, format='png', dpi=300, bbox_inches="tight")


def pie_chart_values(df, question):
    """
    This function creates pie charts from dataframes (df), and question number as an input  
    """
    def value_fn(x):
        print(x)
        return '{:.0f}'.format(total*x/100)
    
    colors = ['#203864', '#4472c4','#a5a5a5','#e3877d', '#8faadc', '#b4c7e7',  '#9dc3e6','#c00000']
    fig = plt.figure(figsize = [6,10])
    ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])
    total=df['values'].sum()    
    patches, texts, pcts = ax.pie(df['values'], colors = colors, autopct=value_fn,startangle=90, pctdistance=1.1)
    plt.legend(df['answer'], loc="center left", bbox_to_anchor=(1,0.5), fontsize=14) 
    plt.setp(pcts, fontweight='bold')
#    plt.show()
    name = question + '.png'
    fig.savefig(name, format='png', dpi=300, bbox_inches="tight")

### Upload data   

#read in exit survey data
survey_file_path =os.path.join(os.getcwd(),"CSPC_survey_analysis\exit_responses.csv")
survey_raw = pd.read_csv(survey_file_path, encoding = 'utf-8')

#read in q_type.csv which has the type of questions for the survey
survey_fileQ_path =os.path.join(os.getcwd(),"CSPC_survey_analysis\q_type.csv")
q_type = pd.read_csv(survey_fileQ_path, encoding = 'utf-8')

#subsets of quantitative dataset-----------
#the quantitative dataset will be divided up further into three different csvs
        #1) closed, multiple choice answers
        #2) closed, nominal/ranked answers
        #3) closed, multiple answers

#Questions 13, 15-20
subset1 =True
if subset1:
        #for subset csv #1 (mc_data.csv)
    #select data with type2 in q_type.csv as 'mc' to select closed, multiple choice answers
    mc_q = q_type[q_type['type_2'] == 'mc']
    #select first column to get a list of column names of 'survey_raw' for open-ended questions
    mc_q_list = mc_q['question'].tolist()
    mc_data = survey_raw[survey_raw.columns.intersection(mc_q_list)]

    #Question 13
    q13 = convert_values_per_capita(mc_data,'Question 13')
    pie_chart(q13,'Question 13')

    #Question 15
    q15 = convert_percent(mc_data,'Question 15')
    pie_chart(q15,'Question 15')

    #Question 16
    q16 = convert_percent(mc_data,'Question 16')
    pie_chart(q16,'Question 16')

    #Question 17
    q17 = convert_percent(mc_data,'Question 17')
    pie_chart(q17,'Question 17')

    #Question 18
    q18 = convert_percent(mc_data,'Question 18')
    pie_chart(q18,'Question 18')

    #Question 19
    q19 = convert_percent(mc_data,'Question 19')
    pie_chart(q19,'Question 19')

    # #Question 20
    q20 = convert_values(mc_data,'Question 20')
#   q20.to_csv("q20.csv")
    pie_chart_values(q20,'Question 20')

#Question 14,(multiple choice, closed)
subset3 = True
if subset3:
    #for subset csv #3 (multi_answer_data.csv)
    #select data with type2 in q_type.csv as 'multi-answer' to select closed, multi-selection answers
    multia_q = q_type[q_type['type_2'] == 'multi-answer']
        #select first column to get a list of column names of 'survey_raw' for open-ended questions
    multia_q_list = multia_q['question'].tolist()
    multia_data = survey_raw[survey_raw.columns.intersection(multia_q_list)]

    q14_list = ['Question 14Executive (e.g. President, CEO, VP, Executive Director)','Question 14Scientist/Researcher/Professor',\
        'Question 14Senior Management (e.g. Director, Manager)','Question 14Analyst, advisor, coordinator, officer, consultant, etc.',\
            'Question 14Student or Postdoctoral Fellow','Question 14Other','Question 14Other']
    df = survey_raw[q14_list]
 
    df1 = pd.concat([df, df.T.stack().reset_index(name='Question 14')['Question 14']], axis=1) #Combine columns
    df2 = df1['Question 14']
    df2.dropna()

    df3 = df2.value_counts(normalize = True) 
    df3 = pd.DataFrame(df3).reset_index()
    df3.columns = ['answer', 'percent']
    df3['percent'] = df3['percent']*100
    pie_chart(df3,'Question 14')