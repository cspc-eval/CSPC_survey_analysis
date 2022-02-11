#This is the base code is for creating stacked bar charts
#Creates figure for Q4: logical aspects

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
#the questions has multiple columns so first collect all columns for question 4

#extract all columns for Question 4 
filter_col = [col for col in survey_raw if col.startswith('Question 4')] #creates a list of column names for question 4

#create a subset of data for question 4
q4 = survey_raw[filter_col] 

#calculate the percentage of each answer and transposes the dataframe
df = q4.apply(lambda x: x.value_counts(normalize = True, dropna=False)).T 
#Fill in 'NaN' for NAs
df.columns = df.columns.fillna('No Response')

#add a new column for labelling the graph
df['Questions'] = ['Registration process', 'Virtual conference platform', 'Virtual networking opportunities', 'Exhibition booth interactions', 'Gamification', 'Ease of navigating virtual conference', 'Tech support quality', 'Ease of navigating online conference program', 'Conference duration', 'Conference accessibility', 'Panel A/V quality'] 

#set the questions column as the index
df = df.set_index('Questions') 
df = df.reindex(['Virtual networking opportunities', 'Exhibition booth interactions', 'Gamification', 'Tech support quality', 'Ease of navigating online conference program', 'Ease of navigating virtual conference', 'Virtual conference platform', 'Panel A/V quality', 'Conference duration', 'Conference accessibility', 'Registration process']) 

#multiply all values by 100 to get the percentage in '%' rather than in decimals
df = df*100

#rearrange column order
df = df[['Outstanding', 'Excellent' , 'Good', 'Fair', 'Poor', 'No Response']]

#change some column types to int
#df[['Outstanding', 'Excellent' , 'Good', 'Fair', 'Poor', 'NaN']] = df[['Outstanding', 'Excellent' , 'Good', 'Fair', 'Poor', 'NaN']].round(0).astype(int)

#create a list of colors to be used in the bar charts
colors_stacked = ['#203864', '#4472c4', '#b4c7e7', '#e3877d', '#c00000', '#FFFFFF']#'#a5a5a5', '#C5C9C7']

#graph
ax = df.plot(kind='barh', #selecting the order of columns
                    stacked=True, 
                    color=colors_stacked,
                    figsize=(15, 15),
                    width=0.75)  

#looping to label text for proportion text
text_color = ['white', 'white', 'white', 'white', 'white', 'black']
for n, x in enumerate([*df.index.values]):
    for (proportion, x_loc, x_txt) in zip(df.loc[x],
                                    df.loc[x].cumsum(), text_color):
        if proportion>2:
                
            ax.text(x=(x_loc - proportion) + (proportion / 2)*0.9, #placement of text
                     y=n-0.08,
                     s=round(proportion), #the label
                     color=x_txt,
                     fontsize=10) 
# Highlight the no response bar in black edgecolor
for b in ax.containers[5]:
    b.set_edgecolor('grey')
    b.set_linewidth(0.5)

ax.set_xlim([0, 100])
# legend
ax.legend(loc="upper center", bbox_to_anchor=(0,0.84,1,0.2), ncol = 7, prop={'size': 12}) #adjust the legend position and font size
# x-axis formatting
ax.tick_params(axis='y', labelsize=12)
ax.tick_params(axis='x', labelsize=12)
ax.set(xlabel='Percentage of Responses', ylabel='') #label for x axis
ax.xaxis.get_label().set_fontsize(12)
ax.set_yticklabels([textwrap.fill(label, 14) for label in df.index]) #wraps the text
ax.xaxis.set_major_formatter(mtick.PercentFormatter()) #add percent symbol to x-axis
figq4 = plt.gcf()
plt.show()
plt.draw()
figq4.savefig('Question 4', dpi=300)