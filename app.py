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

# logger = logging.getLogger('openzwave')
# import openzwave
# from openzwave.node import ZWaveNode
# from openzwave.value import ZWaveValue
# from openzwave.scene import ZWaveScene
# from openzwave.controller import ZWaveController
# from openzwave.network import ZWaveNetwork
# from openzwave.option import ZWaveOption
# import time
# from flask_restful import Resource, Api
# import threading

##### db register######################
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'register'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#################### mail server #############################
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "asma.fakhfekh@gmail.com"
app.config["MAIL_PASSWORD"] = "24679797"
mail = Mail(app)

################# Timer clock ############
chour = 0
cminute = 0
csecond = 0

def real_time() :
    global chour 
    global cminute
    global csecond
    while True:
            dt = list(time.localtime())
            chour = dt[3] + 1
            cminute = dt[4]
            csecond = dt[5]
            time.sleep(1)
            return chour, cminute , csecond 
####### Network Creation  ##################
# count_network = 0
# network =   None
# def active_network():
#     global network
#     # print(threading.current_thread().name)
#     if network != None:
#         pass
#         if network.state>=network.STATE_AWAKED:
#             print("done creating the network ")
            
#         else:
#             network = Creating_a_network()
#     else:
#         network = Creating_a_network()

# api = Api(app)    
################ testing sweet alert Not working #####################  
# @eel.expose
# def include():
#     global network
#     active_network()
#     Adding_device_securly(network)
############ Def exterieur weather###########
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
################### def time and date #########
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



#################### chart page ################
labels =[]
values = []
day_values=[]
#take_temperature=True
@app.route('/chart')
def chart():
    global labels,values,day_values
    link=CreateConnection()
    data_chart_temperature=get_data_chart_temperature(link)
    for data in data_chart_temperature :
        values.append[0]
        labels.append[1]
    legend = 'Power consumption'
    Power_consumption = []

     
    temperature,pressure,humidity= weather()
    print ("############## temperature ")
    print(temperature)
    now,monthh,date_time=month()
    
    if date_time not in labels :
        #labels.append(date_time)
        print("list of days:",labels)
        day_values.clear()
        day_values.append(temperature)
        print('list of temperature taken during the day :',day_values)
        moyenne_temperature= mean(day_values)
        #values.append(moyenne_temperature)
        insertintoDB_chart_temperature(link , moyenne_temperature, date_time)
        
        
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
    
    
    data_chart_temperature=get_data_chart_temerature(link)


    bar_labels=labels
    bar_values=values

    return render_template('chart.html', title='Bitcoin Monthly Price in USD', max=17000, labels=bar_labels, values=bar_values,values_chart2=Power_consumption, labels_chart2=labels, legend=legend)





##################LOGIN  PAGE ######################
@app.route('/Login',methods=["GET","POST"])
def Login():
    error = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        connexion = CreateConnection()
        name = request.form['name']
        password = request.form['password']

        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM register.users WHERE name = %s AND password = %s', (name, password,))
        user = cur.fetchone()
        if user:
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            return redirect(url_for('Dashboard'))
        else:
            error = 'Incorrect username/password!'
    
    return render_template('Login.html', error=error)
########### REGISTER ##########################

@app.route('/register', methods=["GET", "POST"])
def register():
    error = ''
    
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        name = request.form['name']
        password = request.form['password']
        email = request.form['email']
         # Check if account exists using MySQL
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM register.users WHERE name = %s', (name,))
        user = cur.fetchone()
        # If account exists show error and validation checks
        if user:
            error = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            error = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', name):
            error = 'Username must contain only characters and numbers!'
        elif not name or not password or not email:
            error = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cur.execute('INSERT INTO register.users VALUES (NULL, %s, %s, %s)', (name, password, email,))
            mysql.connection.commit()
            error = 'You have successfully registered!'
            return render_template('Dashboard.html')
    elif request.method == 'POST':
            # Form is empty... (no POST data)
        error = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', error=error)


################## PAGE INSERT_DATA & TABLE network #############################
# @app.route('/info')
# def infodevice():
    
#     connexion = CreateConnection()
#     global network
#     active_network()

#     print ('network state',network.state)
#     d1,d2,d3,d4,d5,d6,d7,d8,d9,d10 = Info_Zwave_dongle(network)
#     memory =Memory_used()
#     #print ('##################################')
#     #print (type(network))
#     #print ('##################################')
#     #A,B,C= Sensors_information(network)
#     #Sensors_information(network)
    
#     print("--------------ALL devices --------------------")
#     for node in network.nodes:
#         nodeALL = network.nodes[node]
#         #NODE= str(node)
#         #print ('len node id' , len(str(node)))
#         len_node_Name = len(str(nodeALL.product_name))
#         try:
#             if len_node_Name > 0:
#                 insertintoDB(connexion, nodeALL.product_name , node)
#                 #print ('##################################')
#                 #print ('Node Names', nodeALL.product_name)
#                 #print ('Node', node)
#                 #print ('##################################')
#         except:
#             print ("None Type ===> Empty")
        
    dataresults = getAllData(connexion)
    Nodeid ,Names = createlists(dataresults)

    #print (sensor)
    #sensor = Sensors_information(network)
    #print(sensor)
    # ,A=A,B=B,C=C
    return render_template('info.html' , Nodeid= Nodeid ,Names=Names,d1=d1,d2=d2,d3=d3,d4=d4,d5=d5,d6=d6,d7=d7,d8=d8,d9=d9,d10=d10,memory=memory) 
    #return "info" + str (network.nodes_count)
###############################  PAGE ADD EXCLUDE  ###############################
Nodeidlist =[]
Nameslist=[]
@app.route('/config', methods=["GET", "POST"])
def config():

    global Nodeidlist ,Nameslist
    Nodeidlist.clear()
    Nameslist.clear()

    global network
    active_network()
    #connexion = CreateConnection()   
    print("--------------ALL devices before inclusion --------------------")
    msg=''
    for node in network.nodes:
        nodeALL = network.nodes[node]
        print (nodeALL.product_name,node)
        Product =nodeALL.product_name
        len_node_Name = len(str(nodeALL.product_name))
        try:
            if len_node_Name > 0:
                if nodeALL.product_name not in Nameslist :
                    Nameslist.append(nodeALL.product_name)
                    if node not in Nodeidlist:
                        Nodeidlist.append(node)

                print ("####### 1")
                print ('Node',Nodeidlist ,'list',Nameslist)


                #insertintoDB(connexion, nodeALL.product_name , node)
                #print ('##################################')
                #print ('Node Names', nodeALL.product_name)
                #print ('Node', node)
                #print ('##################################')
        except:
            print ("None Type ===> Empty")
    #dataresults = getAllData(connexion)
    #Nodeid ,Names = createlists(dataresults)

    #action = Adding_device_securly(network)

    if request.method == 'GET':
        return render_template('config.html',Nodeidlist=Nodeidlist ,Nameslist=Nameslist,msg=msg)
    else:
        
        if request.form['submit_button'] == 'Add a new device':
            #flash("Please, Wait 30 seconds for the device to be included !")
            action=Adding_device_securly(network)
            #threading.Thread(name='adding a new device',target=Adding_device_securly(network)).start()
            print("Adding_device_securly")
            

        elif request.form['submit_button'] == 'Exclude a device':
            action = exclude_device(network)
    
    print("--------------ALL devices after inclusion  --------------------")
    for node in network.nodes:
        nodeALL = network.nodes[node]
        print (nodeALL.product_name,node)
        Product =nodeALL.product_name
        len_node_Name = len(str(nodeALL.product_name))
        try:
            if len_node_Name > 0:
                if nodeALL.product_name not in Nameslist :
                    Nameslist.append(nodeALL.product_name)
                    if node not in Nodeidlist:
                        Nodeidlist.append(node)

                print ("############# 2 ")
                print ('Node',Nodeidlist ,'list',Nameslist)


                #insertintoDB(connexion, nodeALL.product_name , node)
                #print ('##################################')
                #print ('Node Names', nodeALL.product_name)
                #print ('Node', node)
                #print ('##################################')
        except:
            print ("None Type ===> Empty")

    print (Nodeidlist ,Nameslist)
    #network =network, Product= Product, nodeALL=nodeALL 
    
    return render_template('config.html',Nodeidlist=Nodeidlist ,Nameslist=Nameslist,action=action)
##################### def saison #################
def saison_weather():
    
    now,monthh,date_time=month()
    monthlist = ['January','February','March','April','May','June','July','August','September','October','November','December']
    for i in range (0,len(monthlist)):
        if monthh == monthlist[i]:
            print('####### month is ',monthh)
            if i in [0,1,2,9,10,11]:
                saison= "coldsaisons"
            elif i in [3,4,5,6,7,8]:
                saison= "Hotsaisons"
            return saison 
                

################## Dashboard/MAIL SENDER FOR ALARM ###############################
@app.route('/Dashboard' , methods=["GET", "POST"])
def Dashboard():
    
    
    
    global network
    active_network()
    saison = saison_weather()
    
    print('################ our saison is #########')
    print(saison)
    if saison == "coldsaisons":
        print("comparaw ")

    
    msgg=''
    tip=''
    #if 'loggedin' in session:
    # # User is loggedin show them the home page
     #   return render_template('Dashboard.html', name=session['name'])
    #     print(name=session['name'])
    # # User is not loggedin redirect to login page
    #return redirect(url_for('Login'))

    now,monthh,date_time=month()
    monthlist = ['march','february','january','december','november','october','august','july','june','may','april','september']
    listlabel,listvalue,listunit = Sensors_information(network)
    print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)
    lenlist = len(listlabel)
    print('length',lenlist)
    temperature,pressure,humidity= weather()
    print("################## outside data #####################")
    print(temperature,pressure,humidity)

    if request.method == 'GET':
        return render_template('Dashboard.html', listunit=listunit ,listlabel =listlabel , listvalue= listvalue, lenlist=lenlist, msgg=msgg, pressure=pressure, temperature=temperature, humidity=humidity, monthh=monthh,monthlist=monthlist, tip=tip, saison=saison)
    else:
        if request.form['confirmBtn'] == 'On':
            print('button on detected')
            action = SetLightOn(network)
            print(action,'light is on')
        if request.form['confirmBtn'] == 'Off':
            action = SetLightOFF(network)   
            print(action,'light is off')
        if request.form['confirmBtn'] == 'ON':
            action = onwallplug(network)
            print(action,'wallplug is on')
        if request.form['confirmBtn'] == 'OFF':
            action = offwallplug(network)
            print(action,'wall plug is off')
            


    return render_template('Dashboard.html', listunit=listunit ,listlabel =listlabel , listvalue= listvalue,lenlist=lenlist, msgg=msgg, pressure=pressure, temperature=temperature ,humidity=humidity, monthh=monthh,monthlist=monthlist, tip=tip)

############# PAGE ALL SCENES ############              

@app.route('/scenario', methods=['GET', 'POST'])
def scenario ():
    global network
    active_network()
    global Motion_activate
    global count_light_time
    global count_scene
    if request.method == 'GET':
        return render_template('scenario.html')
    
    else:

        if request.form['confirmBtn'] == 'Deactivate':
            count_light_time = False
            action = SetLightOFF(network)
        if request.form['confirmBtn'] == 'Alarm Set':
            threading.Thread(name='alarm scene thread',target=motion_scene()).start()
        if request.form['confirmBtn'] == 'Alarm Stop':
            Motion_activate = False
        

    return render_template ('scenario.html')
#### absent mode #####
@app.route('/scenario2', methods=['GET', 'POST'])
def scenario2 ():
    global network
    active_network()
    listlabel,listvalue,listunit = Sensors_information(network)
    print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)
    lenlist = len(listlabel)
    print('length',lenlist)
    
    if request.method == "POST":
        selected_contacts = request.form.getlist("wall")
        print(selected_contacts)
    
    # if request.method == 'GET':
    #     return render_template('scenario2.html', listunit=listunit ,listlabel =listlabel , listvalue= listvalue)
    # else:
    #     phase= request.form.get('wall')
    #     print(phase)
    #         # action = offwallplug(network)
    #         # print(action,'wall plug is off')
        
       
    return render_template ('scenario2.html', listunit=listunit ,listlabel =listlabel , listvalue= listvalue)     
            
            
################# PAGE scene 1 light with time ( one botton for activation )##########
hoursf=0
hours=0
minutef=0
minutes=0
@app.route('/scenario1', methods=['GET', 'POST'])
def scenario1():
    
    global hours,hoursf,minutes,minutef
    global network 
    active_network()

    if request.method == 'GET':
        return render_template('scenario1.html')
    else:
        if request.method == 'POST':
            hours = request.form["hour"]
            hoursf = request.form["hourf"]
            minutef = request.form["minutef"]
            minutes = request.form["minutes"]
            print("################## taken time ################## ")
            print('start at',hours,":",minutes,'end at',hoursf,":",minutef)
            if request.form['confirmBtn'] == "Activate":
                threading.Thread(name='light with Time scene',target=sclight_Time()).start()

    return render_template("scenario1.html")
############################## Def scene MOTION ALARM #############
Motion_activate = True
def motion_scene():
    global Motion_activate
    global network
    active_network()
    msg = Message("z-wave platform ALARM ", sender="asma.fakhfekh@gmail.com", recipients=["asma.fakhfekh@gmail.com"])
    msg.body = "detected motion in the house !"
    while Motion_activate :
        print(Motion_activate)
        listlabel,listvalue,listunit = Sensors_information(network)
        print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)
        if len(listlabel) != 0 :
            for i in range(len(listlabel)):
                #print("list is not empty")
                if listlabel[i] == "Sensor" :
                    print("motion sensor detected",listvalue[i])
                    if listvalue[i] == True :
                        print("alarm email") 
                        with app.app_context():
                            mail.send(msg)
                    else :
                        pass
        time.sleep(5)

#################### DEF SCENE LIGHT LIMUNISITY  ##########################
count_scene= True
def scsensor():
    global count_scene

    global network
    active_network()
    listlabel,listvalue,listunit = Sensors_information(network)
    print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)

    while count_scene :
        time.sleep(1)
        for i in range(len(listlabel)):
            if listlabel[i] == "Luminance" :
                print("light intensity detected",listvalue[i])
                if listvalue[i] < 100 :
                    action = SetLightOn(network)
                    print("turning the light on ")
                    #time.sleep(1)
                if listvalue[i] > 500 :
                    print("turning the light off")
                    action = SetLightOFF(network)
            else:
                print('Motion sensor is not included and luminance is not detected ') 
        time.sleep(5)
################ DEF SCENE LIGHT WITH TIME ##############

count_light_time = True 
def sclight_Time():
    global count_light_time
    global network
    global hours,hoursf,minutes,minutef
    active_network()
    
    global chour, cminute, csecond
    chour,cminute, csecond = real_time()

    print("################## curent time ################## ")
    print(chour, cminute , csecond)


    
    while count_light_time :
        chour,cminute, csecond = real_time()
        print("################## curent time ################## ")
        print(chour,':',cminute ,':', csecond)
        if hours<=str(chour) and str(chour)<=hoursf:
            if minutes<=str(cminute) and str(cminute)<=minutef:
                print("we are in the periode to turn the light ON")
                action = SetLightOn(network)
            else :
                print('current time',chour,'is not in the chosen periode',' ',hours,'to',hoursf,' ','to turn on the light') 
                action = SetLightOFF(network)
                print("we are in the periode to turn the light Off")
        time.sleep(2)



    
@app.route('/index')
def index():
    global saison
    saison = saison_weather()
    render_template('index.html')
  
@app.route('/lightON')
def lightON():
    global network
    active_network()
    char =bulbs_info(network)
    SetLightOn(network)
    return render_template('lightON.html',char=char)

@app.route('/lightOFF')
def lightOFF():
    global network
    active_network()
    char =bulbs_info(network)
    string =dimmers_Info(network)
    print(char)
    print (string)
    SetLightOFF(network)
    return render_template('lightOFF.html', char=char)

     

# @app.route('/chart')
# def chartTempHUM():
#     connexion = CreateConnection()
#     dataresults = getAllData(connexion)
#     datahumi =listhumi 
#     datatemp =listTemp
#     datadate =listdate 
#     createlists(dataresults)
#     return render_template('chart.html',labels=datadate, values=datatemp)

@app.route('/exit')
def exit(network):
    network.stop()

@app.route('/logout')
def logout():
    # Remove session data, this will log the user out
   session.pop('loggedin', None)
   session.pop('id', None)
   session.pop('username', None)
   # Redirect to login page
   return redirect(url_for('home'))

if __name__ == "__main__":
    #active_network()
    #char = Info_Zwave_dongle(network)
    app.secret_key = "^A%DJAJU^JJ123"
    app.run(debug=True, host='0.0.0.0', port= 7501,threaded=True)



