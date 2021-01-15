from flask import Flask,render_template, jsonify,request,url_for,logging ,redirect,session
from flask import flash
from PythonCode import *
import time
from MYsql import *
import logging
import sys, os, re
import resource
#from flask_table import Table,Col
from flask_sqlalchemy import SQLAlchemy
from flask_mysqldb import MySQL
from flask_mysqldb import MySQL,MySQLdb
from flask_bcrypt import bcrypt
from flask_mail import Mail, Message
import smtplib
from test import *
#import json, database, base64
from random import choice
from datetime import datetime
#import person
import os, binascii
#### for the moment not needed 

#logging.getLogger('openzwave').addHandler(logging.NullHandler())
#logging.basicConfig(level=logging.DEBUG)
#logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('openzwave')
import openzwave
from openzwave.node import ZWaveNode
from openzwave.value import ZWaveValue
from openzwave.scene import ZWaveScene
from openzwave.controller import ZWaveController
from openzwave.network import ZWaveNetwork
from openzwave.option import ZWaveOption
import time
from flask_restful import Resource, Api
import threading
##### db register######################
app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'admin'
app.config['MYSQL_PASSWORD'] = 'admin'
app.config['MYSQL_DB'] = 'register'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
mysql = MySQL(app)

#logged_in = {}
#api_loggers = {}


#################### mail server #############################
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "asma.fakhfekh@gmail.com"
app.config["MAIL_PASSWORD"] = "24679797"
mail = Mail(app)

################# Timer function ############
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
####### network creation##################
count_network = 0

network =   None

def active_network():
    global network
    # print(threading.current_thread().name)
    if network != None:
        pass
        if network.state>=network.STATE_AWAKED:
            print("done creating the network ")
            
        else:
            network = Creating_a_network()
    else:
        network = Creating_a_network()

api = Api(app)        
###################### Home ######################
@app.route('/')
def home():
    return render_template('home.html')
@app.route('/automation')
def automation():
    return render_template('automation.html')
@app.route('/products')
def products():
    return render_template('products.html')


##################LOGIN  ######################
@app.route('/Login',methods=["GET","POST"])
def Login():
    error = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form:
        connexion = CreateConnection()
        # Create variables for easy access
        name = request.form['name']
        password = request.form['password']
        # Check if account exists using MySQL
        cur = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cur.execute('SELECT * FROM register.users WHERE name = %s AND password = %s', (name, password,))
        # Fetch one record and return result
        user = cur.fetchone()
        # If account exists in accounts table in out database
        if user:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = user['id']
            session['name'] = user['name']
            # Redirect to home page
            return redirect(url_for('Dashboard'))
        else:
            # Account doesnt exist or username/password incorrect
            error = 'Incorrect username/password!'
    # Show the login form with message (if any)
    return render_template('Login.html', error=error)
########### REGISTER ##########################

@app.route('/register', methods=["GET", "POST"])
def register():
    
    # msg=""
    # if request.method == 'GET':
    #     return render_template("register.html")
    # else:
    #     name = request.form['name']
    #     email = request.form['email']
    #     #
        
    #     #password = request.form['password'].encode('utf-8')
    #     #hash_password = bcrypt.hashpw(password, bcrypt.gensalt())
    #     password = request.form['password']
    #     hash_password_data=hash_password(password) #from test.py

    #     cur = mysql.connection.cursor()
    #     cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password_data,))
    #     mysql.connection.commit()
    #     session['name'] = request.form['name']
    #     session['email'] = request.form['email']
    #     user = cur.fetchone()
        
    #     if user:
    #         msg = 'Account already exists!'
    #     elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
    #         msg = 'Invalid email address!'
    #     elif not re.match(r'[A-Za-z0-9]+', name):
    #          msg = 'Username must contain only characters and numbers!'
    #     elif not password or not email:
    #         msg = 'Please fill out the form!'
    #     else:
    #         # Account doesnt exists and the form data is valid, now insert new account into accounts table
    #         cur.execute("INSERT INTO users (name, email, password) VALUES (%s,%s,%s)",(name,email,hash_password_data,))
    #         #curl.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', ( name,password, email,))
    #         mysql.connection.commit()
    #         msg = 'Welcome!, You have successfully registered!'
    #         return render_template('Dashboard.html')
    #      elif request.method == 'POST':
    #             # Form is empty... (no POST data)
    #     msg = 'Please fill out the form!'
    #  # Show registration form with message (if any)
        
        #return redirect('/register.html', msg=msg) 
    error = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
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


################## INSERT_DATA & TABLE #############################
@app.route('/info')
def infodevice():
    # for the data in MYsql.py
    connexion = CreateConnection()
    #for the network creation 
    global network
    active_network()

    #print some information 
    print (network.state)
    d1,d2,d3,d4,d5,d6,d7,d8,d9,d10 = Info_Zwave_dongle(network)
    memory =Memory_used()
    #print ('##################################')
    #print (type(network))
    #print ('##################################')
    #A,B,C= Sensors_information(network)
    #Sensors_information(network)
    
    print("--------------ALL devices --------------------")
    for node in network.nodes:
        nodeALL = network.nodes[node]
        #NODE= str(node)
        #print ('len node id' , len(str(node)))
        len_node_Name = len(str(nodeALL.product_name))
        try:
            if len_node_Name > 0:
                insertintoDB(connexion, nodeALL.product_name , node)
                #print ('##################################')
                #print ('Node Names', nodeALL.product_name)
                #print ('Node', node)
                #print ('##################################')
        except:
            print ("None Type ===> Empty")
        
    dataresults = getAllData(connexion)
    Nodeid ,Names = createlists(dataresults)

    #print (sensor)
    #sensor = Sensors_information(network)
    #print(sensor)
    # ,A=A,B=B,C=C
    return render_template('info.html' , Nodeid= Nodeid ,Names=Names,d1=d1,d2=d2,d3=d3,d4=d4,d5=d5,d6=d6,d7=d7,d8=d8,d9=d9,d10=d10,memory=memory) 
    #return "info" + str (network.nodes_count)
###############################  ADD EXCLUDE  ###############################
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
            action = Adding_device_securly(network)
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
################## Dashboard/MAIL SENDER FOR ALARM ###############################
@app.route('/Dashboard' , methods=["GET", "POST"])
def Dashboard():
    #if 'loggedin' in session:
    # # User is loggedin show them the home page
     #   return render_template('Dashboard.html', name=session['name'])
    #     print(name=session['name'])
    # # User is not loggedin redirect to login page
    #return redirect(url_for('Login'))
    global network
    active_network()

    listlabel,listvalue,listunit = Sensors_information(network)
    print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)
    lenlist = len(listlabel)
    print('length',lenlist)
    #Power_level(network)

    if request.method == 'GET':
        return render_template('Dashboard.html', listunit=listunit ,listlabel =listlabel , listvalue= listvalue,msg=msg,lenlist=lenlist)
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


    return render_template('Dashboard.html', listunit=listunit ,listlabel =listlabel , listvalue= listvalue, msg=msg,lenlist=lenlist, msgg=msgg)

############# ALL SCENES PAGES############              

@app.route('/scenario', methods=['GET', 'POST'])
def scenario ():
    global count_light_time
    global count_scene
    listlabel,listvalue,listunit = Sensors_information(network)
    if request.method == 'GET':
        return render_template('scenario.html')
    
    else:
        for i in range(len(listlabel)):
            if listlabel[i] == "Sensor" :
            print("movement is detected",listvalue[i])
            if request.form['submit'] == 'activate':
                print("request been taken")
                if listvalue[i] == True:
                    action = SetLightOn(network)
                else:
                    action = SetLightOFF(network)
            
        if request.form['confirmBtn'] == 'Deactivate':
            count_light_time = False
            action = SetLightOFF(network)
        if request.form['confirmBtn'] == 'Alarm Set':
            threading.Thread(target=scsensor()).start()
        if request.form['confirmBtn'] == 'Alarm Stop':
            count_scene = False
    

    return render_template ('scenario.html')
################# scene 1 light with time ( one botton for activation )##########
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
            if request.form['confirmBtn'] == 'Activate your scene':
                threading.Thread(target=sclight_Time()).start()

    return render_template("scenario1.html")
############################## Def scene MOTION ALARM #############
Motion_activate= True
def motion_scene(network):
    global network
    active_network()

    msg = Message("z-wave platform ALARM ", sender="asma.fakhfekh@gmail.com", recipients=["asma.fakhfekh@gmail.com"])
    msg.body = "detected motion in the house !"
    
    while Motion_activate:
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

    #while count_scene :
    for count in range (0,50) :
        print('scene luminance activated')
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
        print(chour, cminute , csecond)
        if hours<=str(chour) and str(chour)<=hoursf:
            print("comparring hours")
            if minutes<=str(cminute) and str(cminute)<=minutef:
                print("comparing minutes")
                print("ON")
                action = SetLightOn(network)
            else :
                print('current time',chour,'is not in the chosen periode',' ',hours,'to',hoursf,' ','to turn on the light') 
                action = SetLightOFF(network)
                print("Off")
        time.sleep(2)
        # if request.form['confirmBtn'] == 'OFF':
        # if str(chour) <= hoursf:
        # if str(cminute) <= minutesf:
        #     #if str(csecond) <= secondesf:
        #         print("OFF")
        #         action = SetLightOFF(network)


    
@app.route('/index')
def index():
    #global network
    #active_network()
    #listlabel,listvalue,listunit = Sensors_information(network)
    #print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)
    #listlabel=['sensor','Luminance']
    #listvalue=[1,2]
    ll=[10,50,100]

    # for i in range(len(listlabel)):
    #     if listlabel[i] == "Luminance" :
    #         print("light intensity detected",listvalue[i])
    #         if listvalue[i] > 100 :
    #             print("turning the light off ")
    #             action = SetLightOFF(network)
    #             #time.sleep(2)
    #         else :
    #             print("turning the light on")
    #             action = SetLightOn(network)

    return render_template('index.html',ll=ll)

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

     

@app.route('/chart')
def chartTempHUM():
    connexion = CreateConnection()
    dataresults = getAllData(connexion)
    datahumi =listhumi 
    datatemp =listTemp
    datadate =listdate 
    createlists(dataresults)
    return render_template('chart.html',labels=datadate, values=datatemp)


@app.route('/scenario3')
def scenario3():
    global count_scene
    global network
    active_network()
    listlabel,listvalue,listunit = Sensors_information(network)
    print('listlabel =',listlabel ,'listvalue=',listvalue ,'listunit=',listunit)
    for i in range(len(listlabel)):
        if listlabel[i] == "sensor" :
            print("movement is detected",listvalue[i])
            if listvalue[i] == True:
                action = SetLightOn(network)
            else:
                action = SetLightOFF(network)
         


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