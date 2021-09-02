from fanuc_get_data import *

"""I created a program so that we can use a for loop with a table of parameter when we want to execute
the data collection of the data. With numpy and as I used it in the fanuc_get_data program, we can
reshape a table as we which

I put in comment the structure of the function
Two parameter are use for the robot  :
robot_adress = http://???.???.???.???  # add in the background of the function this section for the register : /MD/NUMREG.VA
start_range and end_range : value in between of the register you want to acquired

Paramter to write to the influx database
org, bucket,db_url

influxdb_write(robot_adress,start_range,end_range,org,bucket,db_url,host)
"""
#Influx DB parameters
org =  "org"
bucket = "Bucket"
db_url = "http://localhost:8086"

#robot IP adress
robot_adress = 'http://xxx.xxx.xxx.xxx'

#influxdb_write(robot_adress,100,110,org,bucket,db_url)


"""We can also get the alarm history of the robot"""

"""Now we need to reset the data on the robot
We need to send a signal to the ESP32"""

#To be done

"""
                        Let's get the alarm log from the robot
We'll first need to read the last id number of alarm on the fanuc robot from the database
and then read from the robot and compare the two dataframe and write the new alarm if there are some
"""

#influxdb_write_alarm(robot_adress,org,bucket,db_url)