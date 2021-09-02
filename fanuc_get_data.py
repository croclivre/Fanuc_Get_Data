import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import influxdb_client
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS

#Let's define a function for we working the data incoming from fanuc robot
def replace_string(df_name,string1,string2):
    new_strings = []
    for string in df_name:
        new_string = string.replace(string1,string2)
        new_strings.append(new_string) 
    return(new_strings)

#Adress should be like 'http://xxx.xxx.xxx.xxx/MD/NUMREG.VA' 
#Function to get the registry from the robot into a list
def robot_url_pointer(adress,start,end,choice):
    
    adress = adress + "/MD/NUMREG.VA"
    response = urllib.request.urlopen(adress)
    html = response.read()
    soup = BeautifulSoup(html,features="html.parser")
    table = soup.find("pre").find(text=True)
    
    #rework the data string into a standard format
    datasplit = table.split("\n")
    datasplit = replace_string(datasplit," = ", ",")
    datasplit = replace_string(datasplit,"  '", ",")
    datasplit = replace_string(datasplit,"' \r", "")   

    df = pd.DataFrame({'NumReg' : datasplit})
    df = pd.DataFrame(df.NumReg.str.split(',',None).tolist(),columns = ['NumReg','Valeurs','Comment'])
    df = df.iloc[start:end]
   
    if choice == "REG":
        return_list = df['Valeurs'].values.tolist()
    
    elif choice == "COLUMN_NAME":
        return_list = df['Comment'].values.tolist()
        return_list = [x.replace(' ', '_') for x in return_list]

    else:
        return_list = "invalid parameter for the last choice"

    return(return_list)

def get_fanuc_alarm(adress):
    adress = adress + "/MD/ERRALL.LS"
    response = urllib.request.urlopen(adress)
    html = response.read()
    soup = BeautifulSoup(html,features="html.parser")
    table = soup.find("pre").find(text=True)
    #rework the data string into a standard format
    datasplit = table.split("\n")
    datasplit = replace_string(datasplit,"   ", "")
    datasplit = replace_string(datasplit,"  '", ",")
    datasplit = replace_string(datasplit,"' \r", "")  

    df = pd.DataFrame({'NumReg' : datasplit})
    df = df = df.iloc[2:]
  
    df = pd.DataFrame(df.NumReg.str.split('"',None).tolist(),columns = ['Alarm_number','Datetime','Comment','a','b','c','d'])
    df = df[['Alarm_number','Datetime','Comment']]
    df = df.join(df.pop('Datetime').str.split(expand=True))
    df = df.set_axis(['Alarm_number','Comment','Date','Time'], axis=1, inplace=False)

    return(df)
    
def influxdb_read_alarm(org,db_url,token):
    
    client = InfluxDBClient(url=db_url, token=token, org=org)
    query = 'from(bucket: "Exemple")   |> range(start: -24h) |> filter(fn: (r) => r["_measurement"] == "Alarm")   |> filter(fn: (r) => r["_field"] == "Alarm_ID")  |> yield(name: "max")'
    result = client.query_api().query(org="Plastiques Moore", query=query)
    
    results = []
    for table in result:
        for record in table.records:
            results.append((record.get_value(), record.get_field()))
            
    return(results)

def influxdb_write(robot_adress,start_range,end_range,org,bucket,db_url,token):

    column_name = robot_url_pointer(robot_adress,start_range,end_range,"COLUMN_NAME")
    register = robot_url_pointer(robot_adress,start_range,end_range,"REG")

    #Let's build the framework to write the data to influx db
    len_list = len(register)
    publish_list = [None]*len_list

    for x in range(len_list):
        publish_list[x] = influxdb_client.Point("Production_Data").tag("Numero_Machine","Machine_Exemple").field(column_name[x], register[x])
   
    client = InfluxDBClient(url=db_url, token=token)
    write_api = client.write_api(write_options=SYNCHRONOUS)
    write_api.write(bucket, org, publish_list)

def influxdb_write_alarm(robot_adress,org,bucket,db_url,token):

    client = influxdb_client.InfluxDBClient(url=db_url, token=token)
    
    df = get_fanuc_alarm(robot_adress)
    alarm_name = df['Comment'] 
    alarm_id = pd.to_numeric(df['Alarm_number'], downcast="integer")
    #time_alarm = df['Time']
    
    #Let's build the framework to write the data to influx db
    len_list = len(alarm_id)
    
    alarm_id_filtered = []
    alarm_name_filtered = []
    next_value = max(influxdb_read_alarm(org,db_url))
    z = 0

    for y in range(len_list):
        if(alarm_id[y]>next_value[0]):
             z = z + 1
             alarm_id_filtered[z] = alarm_id[y]
             alarm_name_filtered[z] = alarm_name[y]
    print(alarm_id_filtered)
    
    #Write the alarm list if it's not empty
    if(len(alarm_id_filtered) > 0):
        len_list = len(alarm_id_filtered)
        publish_list = [None]*len_list

        for x in range(len_list):
            publish_list[x] = influxdb_client.Point("Alarm").tag("Alarm_Name",alarm_name_filtered[x]).field("Alarm_ID", alarm_id_filtered[x])
    
        write_api = client.write_api(write_options=SYNCHRONOUS)
        write_api.write(bucket, org, publish_list)
        print("Writing done")
    
    else:
        print("No Alarm registered")