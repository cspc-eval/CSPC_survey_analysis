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
        ax.set(xlabel='', ylabel='percent', title=column) #calling for the labels for x,y axes and title
        plt.show()

#------------------------------------------------
#Question 1 and Question 2a)
#take questions that are to be graphed as a bar chart for the consultation deck
bars = survey_raw[['Question 1', 'Question 2a)']]
#run the function for bar charts
bar_chart(bars, colors, order)

#Question 2d: "For CSPC 2022 next year, would you prefer"; output: horizontal bar chart
#Question 2d needs customization as the x axis labels were unreadable
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
q2d = convert_percent(question) #example of how to use the function "convert_percent"


ax = sns.catplot(y = 'answer', x = 'percent', kind = "bar", data = q2d, color = '#203864')
ax.set_yticklabels([textwrap.fill(e, 30) for e in q2d['answer'].head()]) #wraps the text
plt.show()
#still need to adjust the margins so that the text is readable
#can also look at reducing the word count for each answer (y axis label)

#--------------------------------------------------------
#Question 8 requires a stacked bar chart
#the questions has multiple columns so first collect all columns for question 8

#extract all columns for Question 8 "Please indicate your agreement with the following statements about the 2021 CSPC conference" 
filter_col = [col for col in survey_raw if col.startswith('Question 8')] #creates a list of column names for question 8
q8 = survey_raw[filter_col] #creates a subset of data for question 8

df = q8.apply(lambda x: x.value_counts(normalize = True, dropna=False)).T #calculates the percentage of each answer and transposes the dataframe
df.columns = df.columns.fillna('NaN')

df['Questions'] = ['Welcoming and Inclusive Environment', 'Commitment to Diversity and Equity', 'Content Included Diverse Perspectives'] #add new column for labelling graph
df = df.set_index('Questions') #set the questions column as the index
df = df*100
#create a list of colors to be used in the bar charts
colors_stacked = ['#203864', '#4472c4', '#b4c7e7', '#a5a5a5', '#e3877d', '#c00000', '#E6E6FA']

#create a list of the orders for the x axis
order_stacked = ['Strongly Agree', 'Agree' , 'Neutral', 'Disagree', 'Strongly Disagree', 'Unsure', 'NaN']


ax = df[order_stacked].plot(kind='barh', #selecting the order of columns
                    stacked=True, 
                    color=colors_stacked,
                    figsize=(10, 6))  

""" for n, x in enumerate([*df.index.values]):
    for (proportion, y_loc) in zip(df.loc[x],
                                    df.loc[x].cumsum()):
                
        plt.text(x=(y_loc - proportion) + (proportion / 2),
                 y=n - 0.11,
                 s=f'({np.round(proportion * 100, 1)}%)', 
                 color="black",
                 fontsize=12,
                 fontweight="bold")  """ 
ax.legend(loc="upper left", ncol = 7, prop={'size': 8}) #adjust the legend position and font size
ax.set(xlabel='Percentage of Responses', ylabel='') #label for x axis
ax.set_yticklabels([textwrap.fill(e, 12.5) for e in df.index]) #wraps the text
plt.show()