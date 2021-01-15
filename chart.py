from flask import Markup,make_response
from statistics import mean
import json,requests
import time
from time import sleep

#import eel
from flask import Flask,render_template, jsonify,request,url_for,logging ,redirect,session,g,flash
from flask import flash
# from PythonCode import *
import time
from MYsql import *
import logging
import sys, os, re
# import resource
#from flask_table import Table,Col
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL,MySQLdb
from flask_mail import Mail, Message
import smtplib
from test import *
#import json, database, base64
from random import choice,random
from datetime import datetime
#import person
import os, binascii
import requests, json
from math import*
app = Flask(__name__)

labels =[]
values = []
day_values=[]
#take_temperature=True

def month():
    now = datetime.now()
    monthh=now.strftime('%B')
    print("month:", monthh)
    year = now.strftime("%Y")
    print("year:", year)
    day = now.strftime("%d")
    print("day:", day)
    date_time=now.strftime("%m/%d/%Y")
    return (now,monthh,date_time)
#########
def weather():
    api_key = "bf4b2ee632780a97c7affde346b61b3f"
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = base_url + "appid=" + api_key + "&q=" + 'Aryanah' 
    response = requests.get(complete_url) 
    x = response.json() 
    if x["cod"] != "404": 
        y = x["main"] 
        current_temperature = round((y["temp"] - 273.1)*2)/2
        current_pressure = round(y["pressure"] *2)/2
        current_humidity = round(y["humidity"]* 2)/2
        z = x["weather"] 
        weather_description = z[0]["description"] 
        print(" Temperature (in kelvin unit) = " +
                        str(current_temperature) + 
            "\n atmospheric pressure (in hPa unit) = " +
                        str(current_pressure) +
            "\n humidity (in percentage) = " +
                        str(current_humidity) +
            "\n description = " +
                        str(weather_description)) 
        return (current_temperature,current_pressure,current_humidity)
############
labels =
values = current_temperature
day_values=[20,15,0]
@app.route('/chart')
def chart():
    global labels,values,day_values
    link=CreateConnection()
    # data_chart_temperature=get_data_chart_temperature(link)
    # for data in data_chart_temperature :
    #     values.append[0]
    #     labels.append[1]
    legend = 'Power consumption'
    Power_consumption = [] 
    date_time=month()    
    temperature,pressure,humidity= weather()
    if date_time not in labels :
        #labels.append(date_time)
        print("list of days:",labels)
        day_values.clear()
        day_values.append(temperature)
        print('list of temperature taken during the day :',day_values)
        moyenne_temperature= mean(day_values)
        #values.append(moyenne_temperature)
        # insertintoDB_chart_temperature(link , moyenne_temperature, date_time)
        
        
        print("avarge temperature of :",date_time, "is",moyenne_temperature)
        print("temperature of each day :",moyenne_temperature)
    else :
        day_values.append(temperature)
        print('list of temperature taken during the day:',day_values)
        moyenne_temperature= mean(day_values)
        print("avarge temperature of the day :",moyenne_temperature)
        values.pop()
        values.append(moyenne_temperature)
        print("temperature values of the main list",values)
    
    
    # data_chart_temperature=get_data_chart_temerature(link)


    bar_labels=labels
    bar_values=values

    return render_template('chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values,values_chart2=Power_consumption, labels_chart2=labels, legend=legend)




if __name__ == "__main__":
    #active_network()
    #char = Info_Zwave_dongle(network)
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True)