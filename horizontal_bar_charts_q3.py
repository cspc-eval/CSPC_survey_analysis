#This is the base code is for creating horizontal bar charts
#graphs will be created for Q3

# Note that respondents could select multiple options for Q3 response.
# Therefore, the percentages shown in the figure reflect how many (out of all respondents) selected each option.

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import textwrap
import matplotlib.ticker as mtick

def convert_percent(survey_raw, filter_col):
    """
    This function will take the raw data and create a dataframe with a summary of data showing the percentages of each answer.
    The function will return a pandas dataframe.
    """
    n = survey_raw.shape[0] # number of respondants to survey
    df = survey_raw[filter_col].count()
    df = pd.DataFrame(df).reset_index()
    df.columns = ['answer', 'percent']
    df['percent'] = df['percent'].divide(n) *100
    return df



#read in exit survey data (raw .csv file downloaded from simplesurvey)
#thie file is also available in the CSPC 2021 conference data analysis folder
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

##extract all columns for Question 3
filter_col = [col for col in survey_raw if col.startswith('Question 3') and not col.endswith('.1')]

#convert survey data into percent responses per option in Q3
df = convert_percent(survey_raw, filter_col)

#clean up question 3 dataframe
df['answer'] = df['answer'].str.replace('Question 3', '')
# sort the columns by %, then move 'Other' to be plotted at the end
df = df.sort_values('percent')
df['order'] = [6, 0, 1, 2, 3, 4, 5]
df = df.set_index('order')
df = df.sort_values('order')

#graph
g3 = sns.catplot(y = 'answer', x = 'percent', kind = "bar", data = df, color = '#203864')
g3.fig.set_size_inches(12, 6) #set figure size
# extract the matplotlib axes_subplot objects from the FacetGrid
ax = g3.facet_axis(0, 0)
# iterate through the axes containers
for c in ax.containers:
    labels = [f'{int(v.get_width())}%' for v in c]
    ax.bar_label(c, labels=labels, label_type='edge', padding = 2)
ax.set_yticklabels([textwrap.fill(label, 30) for label in df['answer']]) #wraps the text
ax.set(xlabel='Percentage of Respondents', ylabel='') #calling for the labels for x,y axes and title
ax.xaxis.set_major_formatter(mtick.PercentFormatter()) #add percent symbol to x-axis
ax.set_xlim([0, 80])
fig = plt.gcf()
plt.tight_layout()
plt.show()
fig.savefig('Question 3', dpi=300)
#can also look at reducing the word count for each answer (y axis label)
