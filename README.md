# Fanuc_Get_Data
This network as given me answer and knowledge in the past, so I would like to share a project : 

Quick hack to get the registry or other data from the Fanuc robots with python

My job is to program robots, vision system, machines, so I hate doing stupid repetitive stuff like taking the production data from the robots registry day after day.

So I wanted to get data from the robot without having an acces to roboguide and the Karel language. 

So the whole idea his to use the webpage of the robot 'http://xxx.xxx.xxx.xxx/MD/NUMREG.VA' , parse it with BeautifulSoup, and then reframe the acquired data and export it to a SQL database.

The code is on github : https://github.com/croclivre/Fanuc_Get_Data​​​

The way I reset the production data is with an MQTT broker, I send a command to a ESP32 boards which he activate a solid state relay so that the robot reset it's registry and then doesn't have to handle the realtime. 



