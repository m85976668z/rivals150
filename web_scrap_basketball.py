from selenium import webdriver
import selenium
import pandas as pd
import numpy as np 
import re
import os


PATH = "C:\Program Files (x86)\chromedriver.exe"
driver = webdriver.Chrome(PATH)


driver.get("https://n.rivals.com/prospect_rankings/rivals150/2021")

main = driver.find_element_by_tag_name("main")
main_content = main.find_element_by_id("articles")
table = main_content.find_element_by_tag_name("table")
tbody = table.find_element_by_tag_name("tbody")
tr = tbody.find_elements_by_class_name("prospect-table-row")


#create a list for items: 
table_item = []

for player in tr:
    rank = int(player.find_elements_by_class_name("rank")[0].text)
    first_name = player.find_elements_by_class_name("first-name")[0].text
    last_name = player.find_elements_by_class_name("last-name")[0].text
    name = first_name +' ' +last_name
    stars = player.find_elements_by_class_name("star-on")
    star = len(stars)
    position = player.find_elements_by_class_name("position")[0].text
    loc_school = player.find_elements_by_class_name("break-text")[0].text.split("\n")
    city = loc_school[0].split(",")[0]
    state = loc_school[0].split(",")[1]
    high_school = loc_school[1]
    height = player.find_elements_by_class_name("height")[0].text
    height1 = re.sub(r'[^\w\s]', ' ', height).split(" ")
    cm = round(int(height1[0])*30.48 + int(height1[1])*2.54,1)
    weight = player.find_elements_by_class_name("weight")[0].text
    kg = round(int(weight)*0.454,1)
    school_name = player.find_elements_by_class_name("school-name")[0].text.split("\n")
    if len(school_name) == 1:
        status = school_name[0]
        school = "NA"
        commit_type = "NA"
    else:
        status = "Decided"
        school = school_name[0]
        commit_type = school_name[2]
    table_item.append([rank,name,position,star,city,state,high_school,cm,kg,status,school,commit_type])

df = pd.DataFrame(table_item,columns =['Rank','Name','Position','Star','City','State','High_School','Height','Weight',
'Status','Committed_School','Committed_Type'])
df.head()
df.to_csv('rivals_0308.csv',index=False)


driver.quit()

