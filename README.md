# Fanuc_Get_Data
Quick hack to get the registry or other data from the Fanuc robots with python

  First of all, English isn't my first language so they might be many spelling error... 
  I'm a beginner at python programming, so feel free to comment and add to the project
  
  My job is to program robots, vision system, machines and first and foremost not doing stupid repetitive stuff 
  like taking the production data from the robots registry by hand day after day.

  So I wanted to get data from the robot without having an acces to roboguide and the Karel language.
  So the whole idea his to use the webpage of the robot 'http://xxx.xxx.xxx.xxx/MD/NUMREG.VA' and parse it with BeautifulSoup,
  reframe the data and then export it to a SQL database.

  With multiple robots in the shop, I wanted to create a subproce, in which I just only have to import the code and add the parameter, this code is intended to be a subprocess only, but I'm pretty sure that it isn't program to do that
  
  The way I reset the production data is with an MQTT broker, I send a command to a ESP32 boards which he activate a solid state relay so that the robot reset it's 
  registry and then doesn't have to handle the realtime
