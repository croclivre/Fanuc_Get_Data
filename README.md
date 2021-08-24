# Fanuc_Get_Data
Quick hack to get the registry or other data from the Fanuc robots with python

  First of all, English isn't my first language so they might be many spelling error... 
  I'm a beginner at python programming, so feel free to comment and add to the project
  
  My job is to program robots, vision system, machines.
  But, first and foremost I hate doing stupid repetitive stuff like taking the production data from the robots registry day after day.

  So I wanted to get data from the robot without having an acces to roboguide and the Karel language.
  So the whole idea his to use the webpage of the robot 'http://xxx.xxx.xxx.xxx/MD/NUMREG.VA' , parse it with BeautifulSoup, and then reframe the acquired data and   export it to a SQL database.
  
   
  The way I reset the production data is with an MQTT broker, I send a command to a ESP32 boards which he activate a solid state relay so that the robot reset it's 
  registry and then doesn't have to handle the realtime
