#Import necessary libraries
import numpy as np
import sqlite3
from bs4 import BeautifulSoup
import urllib2
import json

#Parsing the food name and nutritional values

nutritional_titles = []
foods = []
nutritional_values = []
food_found = 10000 #From test/fail, I figured out that the food id's start from 10000

num_foods = 2010000 #Approximately the amount of food items in MyFitnessPal website

#Keep on iterating for all foods
while(food_found != num_foods):
    
    #Variables for temp. storage
    nutritional_value = []
    nutritional_title = []
    
    #Load url's html
    url = 'http://www.myfitnesspal.com/food/calories/' + str(food_found)
    page = BeautifulSoup(urllib2.urlopen(url).read())

    #Extract the food name from the <title> tag
    food = str(page.title).replace("<title>Calories in ", "")
    food = food.replace(" - Calories and Nutrition Facts | MyFitnessPal.com</title>", "")
    
    #If food name isn't found in <title>, go on
    if food == "<title>Calorie Chart, Nutrition Facts, Calories in Food | MyFitnessPal.com</title>":
        continue
        
    #Keep on iterating through the food number in url
    food_found += 1
        
    #Find all the <tr> tags and loop through it's <td> tags to extract nutritional information
    rows = page.find_all('tr')
    for i in rows:
        cols = i.find_all('td')
        cols = [i.text.strip() for i in cols if len(i) != 0]

        nutritional_title.append(cols[0].encode())
        nutritional_value.append(cols[1].encode())
        nutritional_title.append(cols[2].encode())
        nutritional_value.append(cols[3].encode())

    #Add this current food's data to the master list
    nutritional_title = [i for i in nutritional_title if len(i) > 0] #This makes sure there's no empty string's added
    nutritional_value = [i for i in nutritional_value if len(i) > 0] #This makes sure there's no empty string's added
    foods.append(food)
    
    #Take out all the empty strings in the master list
    nutritional_titles.append(nutritional_title)
    nutritional_values.append(nutritional_value)


#Create and access holmusk.db
conn = sqlite3.connect('holmusk.db')
print "Database opened"

#Destroy table FOOD_INFO to make sure we're not replicating tables
conn.execute("DROP TABLE FOOD_INFO")

#Create table and it's necessary fields
conn.execute('''CREATE TABLE FOOD_INFO
       (ID INT PRIMARY KEY     NOT NULL,
       Food           TEXT    NOT NULL,
       Company      TEXT,
       Calories        TEXT,
       Sodium         TEXT,
       Total_Fat        TEXT,
       Potassium        TEXT,
       Saturated        TEXT,
       Total_Carbs        TEXT,
       Polyunsaturated        TEXT,
       Dietary_Fiber        TEXT,
       Monounsaturated TEXT,
       Sugars        TEXT,
       Trans        TEXT,
       Protein        TEXT,
       Cholesterol        TEXT,
       Vitamin_A        TEXT,
       Calcium        TEXT,
       Vitamin_C        TEXT,
       Iron        TEXT);''')

print "Table created successfully"

#Close databse
conn.close()

#Access database 'holmusk'
conn = sqlite3.connect('holmusk.db')
print "Database opened"

#Loop through all the data gathered during web scraping and insert it into table
for i in range(len(foods)):
    curr_str = "INSERT INTO FOOD_INFO VALUES(" + str(i) + "," + "'" + foods[i] + "', 'companyA'"
    
    if len(nutritional_values[i]) != 0:
        for j in nutritional_values[i]:
            curr_str += ", '" + j + "'"
    
    curr_str += ')'
    conn.execute(curr_str);

#Commit the database
conn.commit()
print "Elements commited to DB"

#Close the database
conn.close()

