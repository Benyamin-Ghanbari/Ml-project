# in this program first we create our dataset with web scraping , and then we build our model 
# car price prediction
import requests
from bs4 import BeautifulSoup
import mysql.connector
import re
from sklearn import tree
from sklearn import preprocessing
# create dataset and store to data base
brand = input('please enter your brand : ')
model = input('please enter your model : ')
brand = brand.lower()
model = model.lower()
price_list = []
title_list=[]
miles_list = []
accidents_list=[]
transmission_list=[]
for page in range (2, 12):
    result = requests.get('https://www.truecar.com/used-cars-for-sale/listings/'+brand+'/'+model+'/?page=%i'%page)
    soup = BeautifulSoup(result.text , "html.parser")
    trucar_body = soup.find_all("div", attrs={"class" :"card-content order-3 vehicle-card-body"})

    for info in trucar_body :
    
        price_list = info.select_one("div.heading-3.my-1.font-bold").text
        title_list= info.select_one("h1.heading-base hidden-md-up flex flex-col truncate pt-3 pl-2").text
        miles_list =(info.select_one("div.flex flex-col")).text
        accidents_list = info.select_one('div.pl-2 md:pl-3 mt-3 border-l-2 border-l-[#999999] col-12').text
    for i in range(0, len(title_list)):
    
        title_list[i] =  re.sub(r'\s+', ' ',title_list[i]).strip()
        price_list[i] = re.sub(r'\s+', ' ',price_list[i]).strip()
        miles_list[i] = re.sub(r'\s+', ' ',miles_list[i]).strip()
        print(title_list[i], miles_list[i],price_list[i] )

#-------------------------------
#saving in database

mydatabase = mysql.connector.connect(user = 'user', password = 'password', host = 'host', database = 'database')
mycursor = mydatabase.cursor()
mycursor.execute("CREATE TABLE tablename(name VARCHAR(255), miles VARCHAR(255), accident VARCHAR(255) ,price VARCHAR(255))")
sql = "INSERT INTO tablename (name, ,miles, accident,price) VALUES (%s, %i, %i, %i)"
for j in range (0, len(title_list)):
    val1 = (title_list[j], miles_list[j],accidents_list[j] ,price_list[j])
    mycursor.execute(sql, val1)
mydatabase.commit()

#-------------------------------------------------------------------------------------
#machine learning

x = []
y = []


connection = mysql.connector.connect(host='host',
                                         database='databasename',
                                         user='user',
                                         password='password')

sql_select_Query = "select * from Tablename"
cursor = connection.cursor()
cursor.execute(sql_select_Query)
records = cursor.fetchall()
label_encoder = preprocessing.LabelEncoder()

for row in records:
    row[0]= label_encoder.fit_transform(row[0])
    row[0].unique()
    x.append(row[0:3])
    y.append(row[3])

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x, y)
new_data = []
print("enter brand and model , miles and accident : ")
for i in range (0, 3):
    new_data.append(input())
answer= clf.predict(new_data)
print(answer)
