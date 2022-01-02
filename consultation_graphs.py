#This code is for the creation of graphs to be included in the consultation session with external stakeholders
#Graphs are to be created for Q1, Q2a, Q2d and Q8

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import textwrap
import numpy as np

#read in exit survey data
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

#create a list of colors to be used in the bar charts
colors = ['#203864', '#4472c4', '#b4c7e7', '#a5a5a5', '#c00000']

#create a list of the orders for the x axis
order = ["Outstanding", "Excellent", "Good", "Fair", "Poor"]

#function for creating the bar charts
def bar_chart(df, colors, order):
    """
    This function creates bar charts from dataframes (df) as an input and loops through each column to create a bar graph (output) for each column. 
    The function also takes in 'colors' as a parameter and should be a list of colors, and 'order' which is a list of the preferred order of x axis.
    """
    for column in df:
        q = df[column].value_counts(normalize = True) 
        q = pd.DataFrame(q).reset_index()
        q.columns = ['answer', 'percent']
        q['percent'] = q['percent']*100
    
        ax = sns.catplot(x = 'answer', y = 'percent', kind = "bar", data = q, order = order, palette = colors)
        ax.set(xlabel='', ylabel='', title=column) #calling for the labels for x,y axes and title
        plt.show()

#------------------------------------------------
#Question 1 and Question 2a)
#take questions that are to be graphed as a bar chart for the consultation deck
bars = survey_raw[['Question 1', 'Question 2a)']]
#run the function for bar charts
bar_chart(bars, colors, order)

#--------------------------------------------------
#Question 2d: "For CSPC 2022 next year, would you prefer"; output: horizontal bar chart
#Question 2d needs customization as the x axis labels are quite long
def convert_percent(question):
    """
    This function will take the raw data and create a dataframe with a summary of data showing the percentages of each answer.
    The function will return a pandas dataframe.
    """
    df = survey_raw[question].value_counts(normalize = True) 
    df = pd.DataFrame(df).reset_index()
    df.columns = ['answer', 'percent']
    df['percent'] = df['percent']*100
    return df

question = 'Question 2d)' 
q2d = convert_percent(question) 

#graph
ax = sns.catplot(y = 'answer', x = 'percent', kind = "bar", data = q2d, color = '#203864')
ax.set_yticklabels([textwrap.fill(e, 30) for e in q2d['answer'].head()]) #wraps the text
plt.show()
#can also look at reducing the word count for each answer (y axis label)

#--------------------------------------------------------
#Question 8 requires a stacked bar chart
#the questions has multiple columns so first collect all columns for question 8

#extract all columns for Question 8 "Please indicate your agreement with the following statements about the 2021 CSPC conference" 
filter_col = [col for col in survey_raw if col.startswith('Question 8')] #creates a list of column names for question 8

#create a subset of data for question 8
q8 = survey_raw[filter_col] 

#calculate the percentage of each answer and transposes the dataframe
df = q8.apply(lambda x: x.value_counts(normalize = True, dropna=False)).T 
#Fill in 'NaN' for NAs
df.columns = df.columns.fillna('NaN')

#add a new column for labelling the graph
df['Questions'] = ['Welcoming and Inclusive Environment', 'Commitment to Diversity and Equity', 'Content Included Diverse Perspectives'] 
#set the questions column as the index
df = df.set_index('Questions') 
#multiply all values by 100 to get the percentage in '%' rather than in decimals
df = df*100

#rearrange column order
df = df[['Strongly Agree', 'Agree' , 'Neutral', 'Disagree', 'Strongly Disagree', 'Unsure', 'NaN']]

#change some column types to int
df[['Strongly Agree', 'Agree' , 'Neutral', 'Unsure', 'NaN']] = df[['Strongly Agree', 'Agree' , 'Neutral', 'Unsure', 'NaN']].round(0).astype(int)
#round column values to single decimal 
df[['Disagree', 'Strongly Disagree']] = df[['Disagree', 'Strongly Disagree']].round(1)

#create a list of colors to be used in the bar charts
colors_stacked = ['#203864', '#4472c4', '#b4c7e7', '#e3877d', '#c00000', '#a5a5a5', '#C5C9C7']

#select columns with values that are to be labelled
label_df = df[['Strongly Agree', 'Agree' , 'Neutral', 'Unsure']]
#select NaN column
Nan_df = df[['NaN']]
Nan_df

#graph
ax = df.plot(kind='barh', #selecting the order of columns
                    stacked=True, 
                    color=colors_stacked,
                    figsize=(10, 6))  

#looping to label text for label_df in white
for n, x in enumerate([*label_df.index.values]):
    for (proportion, x_loc) in zip(label_df.loc[x],
                                    label_df.loc[x].cumsum()):
                
        plt.text(x=(x_loc - proportion) + (proportion / 2) + 1.8,
                 y=n,
                 s=proportion, 
                 color="white",
                 fontsize=8) 

#looping to label text for df['NaN'] in black
for n, x in enumerate([*Nan_df.index.values]):
    for (proportion) in zip(Nan_df.loc[x]):
                
        plt.text(x=90,
                 y=n,
                 s=14, 
                 color="black",
                 fontsize=8) 


ax.legend(loc="upper left", ncol = 7, prop={'size': 8}) #adjust the legend position and font size
ax.set(xlabel='Percentage of Responses', ylabel='') #label for x axis
ax.set_yticklabels([textwrap.fill(e, 12.5) for e in df.index]) #wraps the text
figq8 = plt.gcf()
plt.show()
plt.draw()
figq8.savefig('q8', dpi=300)



