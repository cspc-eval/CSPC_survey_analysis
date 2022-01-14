#This is the base code is for creating bar charts
#Graphs will be created for Q1, Q2a

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
#import textwrap
#import numpy as np
import matplotlib.ticker as mtick

#read in exit survey data (raw .csv file downloaded from simplesurvey)
#thie file is also available in the CSPC 2021 conference data analysis folder
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
    
        g = sns.catplot(x = 'answer', y = 'percent', kind = "bar", data = q, order = order, palette = colors)
        
        # extract the matplotlib axes_subplot objects from the FacetGrid
        ax = g.facet_axis(0, 0)

        # iterate through the axes containers
        for c in ax.containers:
            labels = [f'{int(v.get_height())}%' for v in c]
            ax.bar_label(c, labels=labels, label_type='edge')

        ax.yaxis.set_major_formatter(mtick.PercentFormatter(decimals = 0)) #add percent symbol to x-axis
        ax.set(xlabel='', ylabel='') #calling for the labels for x,y axes and title
        fig = plt.gcf()
        plt.show()
        fig.savefig(column, dpi=300)

#------------------------------------------------
#Question 1 and Question 2a)
#take questions that are to be graphed as a bar chart for the consultation deck
bars = survey_raw[['Question 1', 'Question 2a)']]
#run the function for bar charts
bar_chart(bars, colors, order)