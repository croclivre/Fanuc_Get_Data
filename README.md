# Fanuc_Get_Data
Quick hack to get the registry or other data from the Fanuc robots with python

First of all, English isn't my first language so they might be many spelling error... 

My job is to program robots, vision system, machines and first and foremost not doing stupid repetitive stuff 
like taking the production data from the robots registry by hand day after day.

So I wanted to get data from the robot without having an acces to roboguide and the Karel language.
So the whole idea his to use the webpage of the robot 'http://xxx.xxx.xxx.xxx/MD/NUMREG.VA' and parse it with BeautifulSoup
Reframe that data and then export it to a SQL database.

With multiple robots in the shop, I want to create a main code with subprocess, this code is intended to be a subprocess only.

