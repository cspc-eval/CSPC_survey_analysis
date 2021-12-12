#This code is for the creation of graphs to be included in the consultation session with external stakeholders
#Graphs are to be created for Q1, Q2a, Q2d and Q8

#import packages
import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns

#read in exit survey data
survey_raw = pd.read_csv("exit_responses.csv", encoding = 'utf-8')