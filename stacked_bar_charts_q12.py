#This is the base code is for creating stacked bar charts
#Creates figure for 1Q2

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
#Question 4 requires a stacked bar chart
#the questions has multiple columns so first collect all columns for question 12

#extract all columns for Question 4 
filter_col = [col for col in survey_raw if col.startswith('Question 12')] #creates a list of column names for question 4

#create a subset of data for question 12
q12 = survey_raw[filter_col] 

#calculate the percentage of each answer and transposes the dataframe
df = q12.apply(lambda x: x.value_counts(normalize = True, dropna=False)).T 
#Fill in 'NaN' for NAs
df.columns = df.columns.fillna('NaN')

#add a new column for labelling the graph
df['Questions'] = ['Acts as a forum for exploration of issues in science, technology, & innovation policy', 'Strengthens connections between stakeholders and sectors of society', 'Engages early career individuals', 'Promotes / engages in research and analysis in science policy'] 
#set the questions column as the index
df = df.set_index('Questions') 
#multiply all values by 100 to get the percentage in '%' rather than in decimals
df = df*100
#set null counts for opinions to zero
df.fillna(0, inplace=True)

#rearrange column order
df = df[['Strongly agree', 'Agree' , 'Neutral', 'Disagree', 'Strongly disagree', 'Unsure', 'NaN']]

#change some column types to int
#df[['Strongly agree', 'Agree' , 'Neutral', 'Disagree', 'Strongly disagree', 'Unsure', 'NaN']] = df[['Strongly agree', 'Agree' , 'Neutral', 'Disagree', 'Strongly disagree', 'Unsure', 'NaN']].round(0).astype(int)

df[['Strongly disagree']].round(1)

#create a list of colors to be used in the bar charts
colors_stacked = ['#203864', '#4472c4', '#b4c7e7', '#e3877d', '#c00000', '#a5a5a5', '#C5C9C7']

#graph
ax = df.plot(kind='barh', #selecting the order of columns
                    stacked=True, 
                    color=colors_stacked,
                    figsize=(10, 8),
                    width=0.75)  

#looping to label text for proportion text
for n, x in enumerate([*df.index.values]):
    for (proportion, x_loc) in zip(df.loc[x],
                                    df.loc[x].cumsum()):
        if proportion>2:
                
            ax.text(x=(x_loc - proportion) + (proportion / 2)*0.9, #placement of text
                     y=n-0.08,
                     s=round(proportion), #the label
                     color="white",
                     fontsize=8) 


ax.set_xlim([0, 100])
# legend
ax.legend(loc="upper center", bbox_to_anchor=(0,0.87,1,0.2), ncol = 7, prop={'size': 8}) #adjust the legend position and font size
# x-axis formatting
ax.set(xlabel='Percentage of Responses', ylabel='') #label for x axis
ax.set_yticklabels([textwrap.fill(label, 14) for label in df.index]) #wraps the text
ax.xaxis.set_major_formatter(mtick.PercentFormatter()) #add percent symbol to x-axis
figq12 = plt.gcf()
plt.show()
plt.draw()
figq12.savefig('Question 12', dpi=300)