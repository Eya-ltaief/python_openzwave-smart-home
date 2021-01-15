import logging
import sys, os
import resource
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

device="/dev/ttyACM0"
log="Debug"
listlabel=[]
listvalue=[]
listunit=[]

for arg in sys.argv:
    if arg.startswith("--device"):
        temp,device = arg.split("=")
    elif arg.startswith("--log"):
        temp,log = arg.split("=")
    elif arg.startswith("--help"):
        print("help : ")
        print("  --device=/dev/yourdevice ")
        print("  --log=Info|Debug")

#Define some manager options
options = ZWaveOption(device, \
  config_path="/home/pi/venv3/lib/python3.7/site-packages/openzwave/config", \
  user_path=".", cmd_line="")

options.set_log_file("OZW_Log.log")
options.set_append_log_file(False)
options.set_console_output(False) # Notification, changed to False to shows onely my informations 
options.set_save_log_level(log)
options.set_logging(False)
options.lock()

#Get the volume of memory used 
def Memory_used():
    return(resource.getrusage(resource.RUSAGE_SELF).ru_maxrss / 1024.0)

#Create a network object
def Creating_a_network():
    network = ZWaveNetwork(options, log=None)
    time_started = 0
    print("------------------------------------------------------------")
    print("Waiting for network awaked : ")
    print("------------------------------------------------------------")
    for i in range(0,50):
        #print ("############### My Test #############")
        if network.state>=network.STATE_AWAKED:
            #print ("==================== Network Awaked #############")
            print("done creating the network ")
            break
        else:
            #print ("==================== Not Awaiked in Else Tes#############")
            sys.stdout.write(".")
            sys.stdout.flush()
            time_started += 1
            time.sleep(1.0)
    if network.state<network.STATE_AWAKED:
        #print ("############### My network not awaked #############")
        print(".")
        print("Network is not awake but continue anyway")
    return(network)
    
def Power_level(network):
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_power_levels() :
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value : {}".format(network.nodes[node].get_power_level(val)))

def battery_level(network):
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_battery_levels() :
            #print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            #print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  label: {}".format(network.nodes[node].values[val].label))
            print("  value : {}".format(network.nodes[node].get_battery_level(val)))

def Adding_device_securly(network):
    print("press 3 time on the buttom")
    time_started = 0
    for i in range(0,35):
        if network.controller.add_node(False)==True:
            print("the request was sent successfully")
            print("Refresh : Nodes in network : {}".format(network.nodes_count)) 
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time_started += 1
            time.sleep(1.0)
    return network.nodes_count

def exclude_device(network):
    print("press 3 time on the buttom")
    time_started = 0
    for i in range(0,35):
        if network.controller.remove_node()==True:
            print("the request was sent successfully")
            print("Refresh : Nodes in network : {}".format(network.nodes_count)) 
        else:
            sys.stdout.write(".")
            sys.stdout.flush()
            time_started += 1
            time.sleep(1.0)
    return network.nodes_count
    
def Info_Zwave_dongle(network):
    print("Use openzwave library : {}".format(network.controller.ozw_library_version))
    print("Use python library : {}".format(network.controller.python_library_version))
    print("Use ZWave library : {}".format(network.controller.library_description))
    print("Network home id : {}".format(network.home_id_str))
    print("Controller node id : {}".format(network.controller.node.node_id))
    print("Controller node version : {}".format(network.controller.node.version))
    print("Nodes in network : {}".format(network.nodes_count))

    print("Controller capabilities : {}".format(network.controller.capabilities))
    print("Controller node capabilities : {}".format(network.controller.node.capabilities))
    print("Driver statistics : {}".format(network.controller.stats))
    return network.controller.ozw_library_version, network.controller.python_library_version,network.controller.library_description,network.home_id_str,network.controller.node.node_id,network.controller.node.version ,network.nodes_count,network.controller.capabilities,network.controller.node.capabilities,network.controller.stats

def Sensors_information(network):
    global listlabel,listvalue,listunit
    listlabel.clear()
    listvalue.clear()
    listunit.clear()
    values = {}
    #print ('##################################')
    #print ('IN Loop Function',type(network))
    print ('##################################')
    for node in network.nodes:
        for val in network.nodes[node].get_sensors() :
            network.nodes[12].set_config(72057594249478374,255)
            
            print(" wakeup/name :{}/{}".format(network.nodes[node].name,network.nodes[node].can_wake_up()))
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  value: {} ".format(network.nodes[node].get_sensor_value(val)))
            print("  label:{}".format(network.nodes[node].values[val].label))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value: {} ".format(network.nodes[node].get_sensor_value(val)))
            print (" unit: {} ".format( network.nodes[node].values[val].units))
            #print (" commande class : {} ".format( network.nodes[node].command_classes))
            

            """
            
            
            configs = network.nodes[12].get_configs()
            for c in configs:
                print (configs[c])  
                """
            
            listlabel.append(network.nodes[node].values[val].label)
            listvalue.append(network.nodes[node].get_sensor_value(val))
            listunit.append(network.nodes[node].values[val].units)
    #return network.nodes[node].get_sensor_value(val), network.nodes[node].values[val].units,network.nodes[node].values[val].label
    return listlabel,listvalue,listunit

def dimmers_Info(network):
    # 3atani node 8 man3arch emt3 chno / node 8 emte3 bulb
    print( "knowing about all dimmers")
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_dimmers() :
            print(" values :{}".format(val))
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label:{}".format(network.nodes[node].values[val].label))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value: {} {}".format(network.nodes[node].get_dimmer_level(val), network.nodes[node].values[val].units))
            return node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance

def thermostat_Info(network):
    # ma3tata chy
    print( "knowing about all thermostat")
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_thermostats() :
            print(" values :{}".format(val))
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label:{}".format(network.nodes[node].values[val].label))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value: {} {}".format(network.nodes[node].get_dimmer_level(val), network.nodes[node].values[val].units))
            return node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance




def SetLightOFF(network): 
    #emte3 dimmers zeda eli node 8 
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_dimmers() :
            network.nodes[node].set_dimmer(val,-45)
            print(network.nodes[node].set_dimmer(val,-45))
            if network.nodes[node].set_dimmer(val,-45) == False : 
                print(" light is off ")


def SetLightOn(network):
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_dimmers() :
            network.nodes[node].set_dimmer(val,100)
            print(network.nodes[node].set_dimmer(val,100))
            if network.nodes[node].set_dimmer(val,100) == False : 
                print(" light is on ")


def LightTest(network):
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_switches_all() :
    #for node in network.nodes:
        #for val in network.nodes[node].get_dimmers() :
            if node == 11 :
                print('turnning light on node 11')
                #print(val,network.nodes[node].values[val].id_on_network,network.nodes[node].values[val].label,node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance)
                print('state',network.nodes[node].get_switch_all_state(val))
                network.nodes[node].set_switch_all(val,'Off')
                #print('result',network.nodes[node].set_switch_all(val,'On and Off Enabled')) 
            else : 
                pass 
                #print(network.nodes[node].set_dimmer(val,100))
                #if network.nodes[node].set_dimmer(val,100) == True : 
                   # print(" light is on ") 

#ma3atat chy 
def bulbs_info(network): 
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_rgbbulbs() :
            print("node/name/index/instance : %s/%s/%s/%s" % (node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label/help : %s/%s" % (network.nodes[node].values[val].label,network.nodes[node].values[val].help))
            print("  id on the network : %s" % (network.nodes[node].values[val].id_on_network))
            print("  level: %s" % (network.nodes[node].get_dimmer_level(val)))
            return network.nodes[node].get_dimmer_level(val)


def SetRbgwligh(network):
    print ('*****start*****')
    for node in network.nodes:
        for val_id in network.nodes[node].get_rgbbulbs():
            if val_id is not None:
                print("ok")
                network.nodes[node].set_rgbw(val_id,"5")
            else :
                print("NOT ok")
                pass


def switch(network) :
    print("Retrieve switches  compatibles devices on the network    ")
    print("------------------------------------------------------------")
    values = {}
    for node in network.nodes:
        for val in network.nodes[node].get_switches() :
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value / items:  / {}".format(network.nodes[node].get_switch_all_item(val), network.nodes[node].get_switch_all_items(val)))
            print("  state: {}".format(network.nodes[node].get_switch_all_state(val)))           
    print("Retrieve switches all compatibles devices on the network    ")
    print("------------------------------------------------------------")
    for node in network.nodes:
        for val in network.nodes[node].get_switches_all() :
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("  label/help : {}/{}".format(network.nodes[node].values[val].label,network.nodes[node].values[val].help))
            print("  id on the network : {}".format(network.nodes[node].values[val].id_on_network))
            print("  value / items:  / {}".format(network.nodes[node].get_switch_all_item(val), network.nodes[node].get_switch_all_items(val)))
            print("  state: {}".format(network.nodes[node].get_switch_all_state(val)))           



# get switch 3atetni node 10 emt3 WALL PLUG , switch all 3atetni lkol menhom lnode 8 
def offwallplug(network):
    for node in network.nodes:
        for val in network.nodes[node].get_switches():
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("state: {}".format(network.nodes[node].get_switch_state(val)))
            network.nodes[node].set_switch(val,False)
            print('the state command',network.nodes[node].set_switch(val,False))
            """
            if val_id is not None:
                network.nodes[node].set_switch(val,True)
            else :
                print("NOT ok")
                pass

"""
def onwallplug(network):
    for node in network.nodes:
        for val in network.nodes[node].get_switches():
            print("node/name/index/instance : {}/{}/{}/{}".format(node,network.nodes[node].name,network.nodes[node].values[val].index,network.nodes[node].values[val].instance))
            print("state: {}".format(network.nodes[node].get_switch_state(val)))
            network.nodes[node].set_switch(val,True)
            print('the state command',network.nodes[node].set_switch(val,True))

####################### Main #####################################
""" 
network=Creating_a_network()
print("--------------ALL devices --------------------")
for node in network.nodes:
    nodeALL = network.nodes[node]
    print (nodeALL.product_name)

print("--------------Do you wanna add devices --------------------")
ADDING_Request=input(" Do you wanna add devices? print yes or no: " )
if ADDING_Request == "yes":
    Adding_device_securly(network)
    
else :
    pass
print("--------------knowing About the Motion sensor --------------------")
Sensors_information(network)
print("--------------knowing About the thermo --------------------")
thermostat_Info(network)

#offwallplug(network)

print("---- excluding the device ----------")
Excluding_Request=input("do you want to exclude the device ? print yes or no: " )
if Excluding_Request == "yes":
    exclude_device(network)
else :
    pass






print("--------------ALL devices --------------------")
for node in network.nodes:
    nodeALL = network.nodes[node]
    print (nodeALL,nodeALL.product_name.model)
    
#print("########################print rgb info ##########################")   
#SetRbgwligh(network)

  
print("########################set the light ##########################")
SetLightOn(network)


#Power_level(network)

print("###########switch info ########################")
switch(network)

print("##########bulbs info ########################")
bulbs_info(network)
print("##########light is off ########################")
SetLightOn(network)

#print("#########dimmers info #####################")
#dimmers_Info(network)

print ("turning offfffffffff")
offwallplug(network)

A,B,C=Sensors_information(network)
print("--------------ALL devices --------------------")
for node in network.nodes:
    nodeALL = network.nodes[node]
    print (nodeALL.product_name)
print("############## here's label list ########### ")
print(A)
print("############## here's value list ########### ")
print(B)
print

Adding_device_securly(network)
print("--------------ALL devices --------------------")
for node in network.nodes:
    nodeALL = network.nodes[node]
    print (nodeALL.product_name)
Sensors_information(network)




#dimmers_Info(network)
#SetLightOn(network)
#print("changing colors")

#SetRbgwligh(network)

SetLightOn(network)
#bulbs_info(network)
    
#print("Memory use : {} Mo".format(Memory_used()))
#print("--------------knowing About the z-wave --------------------")
#Info_Zwave_dongle(network)

print("--------------knowing About the Motion sensor --------------------")
Sensors_information(network)
print("--------------knowing About the Motion sensor Baterry--------------------")
Baterry_Request=input("do you want to know the baterry level ? print yes or no: " )
if Baterry_Request == "yes":
    battery_level(network)
else :
    pass

"""
 def neighbors(self):
        """
        The neighbors of the node.
        :rtype: set()
        """
        return self._network.manager.getNodeNeighbors(self.home_id, self.object_id)