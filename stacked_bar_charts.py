#This is the base code is for creating stacked bar charts
#Example graphs will be created for Q8

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import textwrap
import matplotlib.ticker as mtick

#read in exit survey data (raw .csv file downloaded from simplesurvey)
#thie file is also available in the CSPC 2021 conference data analysis folder
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

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

#graph
ax = df.plot(kind='barh', #selecting the order of columns
                    stacked=True, 
                    color=colors_stacked,
                    figsize=(10, 6))  
#looping to label text for label_df in white
for n, x in enumerate([*label_df.index.values]):
    for (proportion, x_loc) in zip(label_df.loc[x],
                                    label_df.loc[x].cumsum()):
                
        plt.text(x=(x_loc - proportion) + (proportion / 2) + 0.8, #placement of text
                 y=n,
                 s=proportion, #the label
                 color="white",
                 fontsize=8) 
#looping to label text for df['NaN'] in black
for n, x in enumerate([*Nan_df.index.values]):
    for (proportion) in zip(Nan_df.loc[x]):
                
        plt.text(x=90, #x placement
                 y=n, #y placement
                 s=14, #label
                 color="black",
                 fontsize=8) 
ax.legend(loc="upper left", ncol = 7, prop={'size': 8}) #adjust the legend position and font size
ax.set(xlabel='Percentage of Responses', ylabel='') #label for x axis
ax.set_yticklabels([textwrap.fill(e, 12.5) for e in df.index]) #wraps the text
ax.xaxis.set_major_formatter(mtick.PercentFormatter()) #add percent symbol to x-axis
figq8 = plt.gcf()
plt.show()
plt.draw()
figq8.savefig('Question 8', dpi=300)



