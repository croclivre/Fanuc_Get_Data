import pandas as pd
from bs4 import BeautifulSoup
import urllib.request
import datetime

#Adress should be like 'http://xxx.xxx.xxx.xxx/MD/NUMREG.VA' 

def robot_url_pointer(adress,start,end,choice):
    
    response = urllib.request.urlopen(adress)
    html = response.read()
    soup = BeautifulSoup(html,features="html.parser")
    table = soup.find("pre").find(text=True)
    
    #rework the data string into a standard format
    datasplit = table.split("\n")
    new_strings = []
    new_strings1 = []
    new_strings2 = []
    
    for string in datasplit:
        new_string = string.replace(" = ", ",")
        new_strings.append(new_string)  
        
    for string in new_strings:
        new_string1 = string.replace("  '", ",")
        new_strings1.append(new_string1)
        
    #Format the comment section of the register to remove unwanted caracter      
    for string in new_strings1:
        new_string2 = string.replace("' \r", "")
        new_strings2.append(new_string2)  


    df = pd.DataFrame({'NumReg' : new_strings2})
    df = pd.DataFrame(df.NumReg.str.split(',',None).tolist(),columns = ['NumReg','Valeurs','Comment'])
    df = df.iloc[start:end]
   
    if choice == "REG":
        return_list = df['Valeurs'].values.tolist()
    
    elif choice == "COLUMN_NAME":
        return_list = df['Comment'].values.tolist()
    
    else:
        return_list = "invalid parameter for the last choice"

    return(return_list)
    
