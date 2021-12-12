#This code is for the creation of graphs to be included in the consultation session with external stakeholders
#Graphs are to be created for Q1, Q2a, Q2d and Q8

#import packages
import pandas as pd
from matplotlib import pyplot as plt

#read in exit survey data
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

#create a list of colors to be used in the bar charts
colors = ['#203864', '#4472c4', '#b4c7e7', '#a5a5a5', '#c00000']

#function for creating the bar charts
def bar_chart(df, colors):
    """
    This function creates bar charts from dataframes (df) as an input and loops through each column to create a bar graph (output) for each column. 
    The function also takes in 'colors' as a parameter and should be a list of colors.
    """
    for column in df:
        q = df[column].value_counts(normalize = True) 
        q = pd.DataFrame(q).reset_index()
        q.columns = ['answer', 'percent']
    
        plt.bar(q['answer'], q['percent'], color = colors)
        plt.title(column)
        plt.show()

#take questions that are to be graphed as a bar chart for the consultation deck
bars = survey_raw[['Question 1', 'Question 2a)', 'Question 2d)']]
#run the function for bar charts
bar_chart(bars, colors)

#Question 2d needs customization as the x axis labels were unreadable

#Question 8 requires a stacked bar chart
survey_raw['Question 8']
