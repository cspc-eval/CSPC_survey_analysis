#This is the base code is for creating horizontal bar charts
#Example graphs will be created for Q12d

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import textwrap
import matplotlib.ticker as mtick

#read in exit survey data (raw .csv file downloaded from simplesurvey)
#thie file is also available in the CSPC 2021 conference data analysis folder
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')

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
g2d = sns.catplot(y = 'answer', x = 'percent', kind = "bar", data = q2d, color = '#203864')
g2d.fig.set_size_inches(8, 6) #set figure size
# extract the matplotlib axes_subplot objects from the FacetGrid
ax = g2d.facet_axis(0, 0)
# iterate through the axes containers
for c in ax.containers:
    labels = [f'{int(v.get_width())}%' for v in c]
    ax.bar_label(c, labels=labels, label_type='edge', padding = 2)
ax.set_yticklabels([textwrap.fill(e, 30) for e in q2d['answer'].head()]) #wraps the text
ax.set(xlabel='', ylabel='') #calling for the labels for x,y axes and title
ax.xaxis.set_major_formatter(mtick.PercentFormatter()) #add percent symbol to x-axis
fig = plt.gcf()
plt.tight_layout()
plt.show()
fig.savefig('Question 2d)', dpi=300)
#can also look at reducing the word count for each answer (y axis label)
