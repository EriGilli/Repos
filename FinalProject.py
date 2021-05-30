#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed May 26 10:18:20 2021

@author: egilli
"""

#Import Packages
import pandas as pd
import numpy as np
import mysql.connector
import matplotlib.pyplot as plt
import seaborn as sns


#Import Data via SQL: World Happiness 2008-2020

sql_import = mysql.connector.connect( host = "127.0.0.1", user = "root", password = "Rosalia21", database = "Test")
mycursor = sql_import.cursor()
mysqldata = mycursor.execute("select * from worldhappinessreport where year>=2008 order by year DESC")
DataFetch= mycursor.fetchall()
WorldHappiness = pd.DataFrame(DataFetch)
print(WorldHappiness.head())

#Setting Column Names 
WorldHappiness.columns = ['CountryName', 'year' , 'Ladder score', 'GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perception of corruption', 'Positive effect', 'Negative effect']
DF1= WorldHappiness[['CountryName', 'year' , 'Ladder score', 'GDP per capita', 'Social support', 'Healthy life expectancy', 'Freedom to make life choices', 'Generosity', 'Perception of corruption']]
print(DF1)

#Reusable Function for cleansing imported datasets

def df_check(path):
   df0 = pd.read_csv(path)
   print(df0.info())
   print(df0.isnull().sum())
   df0.fillna("Unknown", inplace=True)
   df0.drop_duplicates(inplace=True)
   print(df0)
   print('Data Check completed')

#Import from CSV: World Happiness 2021

df_check('/Users/egilli/Documents/Introductory Data Analytics /CSV/world-happiness-report-2021 .csv')

WorldHappiness2021 = pd.read_csv('/Users/egilli/Documents/Introductory Data Analytics /CSV/world-happiness-report-2021 .csv')
Dataprep = WorldHappiness2021.iloc[:,[0,2,6,7,8,9,10,11]]
DF2 = Dataprep.rename(columns = {'Country name':'CountryName','Logged GDP per capita':'GDP per capita','Perceptions of corruption':'Perception of corruption'}, inplace = False)
print(DF2)

DF2.insert(loc=1, column='year', value='2021')   
print(DF2)

#Joining World Happiness 2008-2020 with World Happiness 2021

DF3 = pd.concat([DF1,DF2], ignore_index=True)
print(DF3)

#List import: European Country's Names

EuropeList= ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Cyprus', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'United Kingdom']
EuropeList_df = pd.DataFrame(EuropeList)
EuropeList_df.columns =['CountryName']
EuropeList_df.insert(loc=1, column='Continent', value='Europe') 
print(EuropeList_df)

#Merget existing Datasets
DF4 = pd.merge(DF3,
              EuropeList_df,
              how='outer',
              on='CountryName')
print(DF4)

#Focus on Europe:Locate Europen countries
Index_DF4 = DF4.set_index('Continent')
print(Index_DF4)

Europe_Focus = Index_DF4.loc[['Europe'],:]
print(Europe_Focus)

#Seek Ladder scores details across European countries throughout the years
Europe_Focus.groupby(['CountryName']).agg({'Ladder score':['mean', 'min', 'max']}).reset_index()
Ladderscore_Europe = Europe_Focus.groupby(['year']).agg({'Ladder score':'mean'}).reset_index()

#Europe: Quality of Life perception 2008 - 2021
plt.plot(Ladderscore_Europe['year'],Ladderscore_Europe['Ladder score'])
plt.xlabel('Year')
plt.ylabel('Ladder Score')
plt.title('Europe: Quality of Life Perception 2008 - 2021')
plt.show()



#Correlation among Happiness Variables
Happiness_Variables = DF4.groupby(['CountryName']).agg({'Ladder score': 'mean',
                                           'GDP per capita': 'mean',
                                           'Social support': 'mean',
                                           'Healthy life expectancy': 'mean',
                                           'Freedom to make life choices':'mean'}).reset_index()
EuropeHappiness_Variables= Europe_Focus.groupby(['CountryName']).agg({'Ladder score': 'mean',
                                           'GDP per capita': 'mean',
                                           'Social support': 'mean',
                                           'Healthy life expectancy': 'mean',
                                           'Freedom to make life choices':'mean'}).reset_index()

print(EuropeHappiness_Variables)
sns.pairplot(Happiness_Variables)
sns.pairplot(EuropeHappiness_Variables)

#Life Expectancy Analysis 

Life_Expenctancy_Analysis = Europe_Focus.groupby(['year']).agg({'Healthy life expectancy':['mean', 'min', 'max']}).reset_index()
Life_Expenctancy_mean = Europe_Focus.groupby(['year']).agg({'Healthy life expectancy':'mean'}).reset_index()
Life_Expenctancy_min = Europe_Focus.groupby(['year']).agg({'Healthy life expectancy':'min'}).reset_index()
Life_Expenctancy_max = Europe_Focus.groupby(['year']).agg({'Healthy life expectancy':'max'}).reset_index()
print(Life_Expenctancy_mean)

fig = plt.figure()
plt.plot(Life_Expenctancy_min['year'], Life_Expenctancy_min['Healthy life expectancy'], label = "Life_Expectancy_min")
plt.plot(Life_Expenctancy_max['year'], Life_Expenctancy_max['Healthy life expectancy'], label = "Life_Expectancy_max")
plt.xlabel('Year')
plt.ylabel('Healthy Life Expectancy')
plt.title('Europe: Healthy Life Expectancy 2008 - 2021')
plt.legend()
plt.show()
fig.show()

#Ranking Ladder Scores in European countryes 
LS_maxvalue= Europe_Focus.groupby(['CountryName']).agg({'Ladder score':'max'}).reset_index()
print(LS_maxvalue)

LifeLadder_ranking = []
for x in LS_maxvalue['Ladder score']:
    if x >= 07.50:
       LifeLadder_ranking.append('High')
    elif x <= 06.50:
       LifeLadder_ranking.append('Low')
    else:
        LifeLadder_ranking.append('Medium')

LifeLadder_ranking0= LS_maxvalue.insert(loc=2, column='LifeLadder_ranking', value=LifeLadder_ranking) 

print(LS_maxvalue)
print(LifeLadder_ranking0)

#United Kingdom Check
UnitedKingdom_Analysis= Europe_Focus[Europe_Focus.CountryName == 'United Kingdom']
Df_index= UnitedKingdom_Analysis.set_index('year')
Df_iloc= Df_index.iloc[:,[1,2,3,4]]
print(Df_iloc)
print('Code done')


