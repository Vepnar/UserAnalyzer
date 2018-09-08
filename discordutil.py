import re
import bot
import nltk
import json
import random
import sqlite3
import classes

from nltk.tokenize import word_tokenize


#Create a variable for the database
db = None

############################
# Text processing commands #
############################

def splitCmd(cmd,delfirst=1,mentions=True,channels=True,roles=True):
    #Delete mentions from string if enabled
    if mentions:
        #Delete it!
        cmd = re.sub(r'<@!?([0-9]+)>','',cmd)
    #Delete channels from string if enabled
    if channels:
        #Delete it!
        cmd = re.sub(r'<@!?([0-9]+)>','',cmd)
    #Delete roles from string if enabled
    if roles:
        #Delete it!
        cmd = re.sub(r'<@&!?([0-9]+)>','',cmd)     
    #Delete double spaces
    cmd = re.sub(r"(\s\s)+" , " ", cmd)
    cmd = cmd.strip()
    #Check if spaces in command
    if ' ' in cmd:
        #Split command at spaces
        return cmd.split(' ')[delfirst:]
    #Return command as array
    return []           

#Check if user has permission to do admin commands
#Returns '0' for no permissons
#Return '4' for higest level permisson
def hasPermissions(user):
    if user.id ==319799124797030400:
        return 4
    if user.guild.owner == user:
        return 3
    return 0

#Check if something has a cooldown
def isInCooldown(code,msg):
    #Create a cooldown code
    code = code+str(msg)
    #Read all cooldowns
    for c in bot.cooldowns:
        #Check if it is the same code
        if c.check(msg):
            #Return the remaining time if found
            return c.remain()
    #Return 0 if not found
    return 0

#Add a cooldown to something
def putCooldown(code,msg,time):
    #Create a cooldown code
    code = code+str(msg)
    #Create a cooldown object
    c = classes.cooldown(code,time)
    #Add it to the cooldown list
    bot.cooldowns.append(c)
        
#Turn a string in a int
def getInt(string):
    #Run the code safe
    try:
        #Transform if it is possible and return it
        return int(string)
    #return None if not possible
    except:
        return None

##############################
# Better database executions #
##############################

#Check if global database exists
def checkDB():
    global db
    #Checks if global database is set or not
    if db is None:
        #If it is not set connect/create the database
        db = sqlite3.connect('data/discord.db')
#Execute sql commands without getting return data
def voidExecute(command,args,commit=False):
    global db
    #Create a cursor for the database
    cur = db.cursor()
    #Check if args is empty
    if args:
        #Execute the sql with args if not
        cur.execute(command,args)
    else:
        #Execute sql without args
        cur.execute(command)
    #Check if auto commit is enabled
    if commit:
        #Commit last command
        db.commit()
#Used to get 1 one line from the database
def getDataExecute(command,args,commit=False):
    global db
    #Create a cursor for the database
    cur = db.cursor()
    #Check if args is empty
    if args:
        #Execute the sql with args if not
        cur.execute(command,args)
    else:
        #Execute sql without args
        cur.execute(command)
    #Get one line of data from the fetched data
    data = cur.fetchone()
    #Close the cursor
    cur.close()
    #Check if auto commit is enabled
    if commit:
        #Commit last command
        db.commit()
    #Return data found in database could be none
    return data

#Used to get many lines from the database
def getBigDataExecute(command,args,commit=False):
    #Create a cursor for the database
    cur = db.cursor()
    #Check if args is empty
    if args:
        #Execute the sql with args if not
        cur.execute(command,args)
    else:
        #Execute sql without args
        cur.execute(command)
    #Get one line of data from the fetched data
    data = cur.fetchall()
    #Close the cursor
    cur.close()
    #Check if auto commit is enabled
    if commit:
        #Commit last command
        db.commit()
    #Return data found in database could be none
    return data


#Convert item got from database into int
#Return 0 if there is not int
def getIntExecute(command,args,commit=False):
    #Use previous function to get raw data
    data = getDataExecute(command,args,commit=commit)
    #Return 0 if there is no data in the database
    if data is None:
        return 0
    else:
        #return the number if found in the database
        return data[0]
def getJsonExecute(command,args,commit=False):
    #Use previous function to get raw data
    data = getDataExecute(command,args,commit=commit)
    #Return empty dict if there is no data in the database
    if data is None:
        return {}
    else:
        #Try to parse the string from the database to dict
        try:
            return json.loads(data[0])
        except:
            #Return empty dict if it failed
            return {}
######################
# Specific for users #
######################

def checkUserDB():
    #Run an sql that returns 1 if a table exists
    exists = getIntExecute("select 1 from sqlite_master where type='table' and name='Users';",[])
    #return nothing if it exists
    if exists:
        return
    #Create table for the database
    voidExecute("CREATE TABLE Users\
     (ID BLOB PRIMARY KEY NOT NULL,\
     NAME TEXT,\
     XP INT,\
     LEVEL INT,\
     MONEY INT,\
     ANALYZED TEXT,\
     GAMES TEXT,\
     EXTRA TEXT\
     );" ,[],commit=True)
#If enabled it will check if the specific user database exists
def checkUser(userid,username,commit=True):
    #Check if user exists in this database
    exists = getIntExecute("SELECT EXISTS(SELECT 1 FROM Users WHERE ID='?' LIMIT 1);",[userid])
    #stop the event if exists
    if exists:
        return
    #Create a new user if not exists
    voidExecute("INSERT INTO Users(ID,NAME,XP,LEVEL,MONEY,ANALYZED,GAMES,EXTRA),\
    VALUES (?,?,0,0,0,?,?,?)",[userid,username,None,None,None ],commit=commit)
#Update a int in the database for the user
def setUserint(user,item,value):
    #Check if the user is in the database
    #If not this function will also generate a new one
    checkUser(user.id,user.username,commit=False)
    #This will update the user INTOrmation
    voidExecute("UPDATE Users set ? = ? where ID = ?",[item,value,user.id],commit=True)
#Update a String in the database for a user
def setUserString(user,item,value):
    #Check if the user is in the database
    #If not this function will also generate a new one
    checkUser(user.id,user.username,commit=False)
    #This will update the user INTOrmation
    voidExecute("UPDATE Users set ? = ? where ID = ?",[item,value,user.id],commit=True)
#Update a JSON string in the database
def setUserJson(user,item,value):
    #Check if the user is in the database
    #If not this function will also generate a new one
    checkUser(user.id,user.username,commit=False)
    #Convert dict to json string
    value = json.dumps(value)
    #This will update the user INTOrmation
    voidExecute("UPDATE Users set ? = ? where ID = ?",[item,value,user.id],commit=True)

######################
# Specific for Roles #
######################

def checkRoleDB():
    #Run an sql that returns 1 if a table exists
    exists = getIntExecute("select 1 from sqlite_master where type='table' and name='Roles';",[])
    #return nothing if it exists
    if exists:
        return
    #Create table for the database
    voidExecute("CREATE TABLE Roles\
     (name TEXT PRIMARY KEY NOT NULL,\
     id BLOB,\
     rgroup INT\
     );",[],commit=True)

#Used to find roles
def getRole(name):
    #Make the role name lowercase
    name = name.lower()
    #Execute the sql command
    data = getDataExecute('SELECT id,rgroup FROM Roles WHERE name = ?',[name])
    #Check if the data non existing
    if data is None:
        #return None 2 times
        return None,None
    #Return first row of data
    return data

#Used to find roles
def getRolesByGroup(group):
    #Execute a sql command to get the id of the role
    data = getBigDataExecute('SELECT id FROM Roles WHERE rgroup = ?',[group])
    if data is None:
        #return None
        return None
    #Return all of it
    return data
def getRoles():
    #Select all data from the role table
    data = getBigDataExecute('SELECT name,rgroup FROM Roles;',[])
    #Check if the table is empty
    if data is None:
        #Return nothing if empty
        return None
    #Return found data
    return data

#Create a role in the database
def createRole(rid,name,rgroup,commit=True):
    #Make the role name lowercase
    name = name.lower()
    #Execute a sql command to insert the role in the database
    try: 
        voidExecute('INSERT INTO Roles(name,id,rgroup)\
        VALUES (?,?,?)',[name,rid,rgroup],commit=True)
        return True
    except: #This can fail if the item already exists
        return False #Return false if failed
    #Check if the commit function is enabled
    
#########################
# Specific for Language #
#########################

#Used to check if the locale table exists
def checkLocaleDB():
    #Run an sql that returns 1 if a table exists
    exists = getIntExecute("select 1 from sqlite_master where type='table' and name='Message'",[])
    #return nothing if it exists
    if exists:
        return
    #Create table for the database
    voidExecute("CREATE TABLE Message\
     (id TEXT PRIMARY KEY NOT NULL,\
     text BLOB\
     );",[],commit=True)

#Used to add message to the database
def addMessage(name,msg,commit=True):
    #Make the role name lowercase
    name = name.lower()
    #Execute a sql command to insert the role in the database
    try: 
        voidExecute('INSERT INTO Message(id,text)\
        VALUES (?,?)',[name,msg],commit=True)
    except Exception as ex: #This can fail if the item already exists
        print(ex)
        return False #Return false if failed
    return True
#Used to messages
def getMessage(name):
    #Make the role name lowercase
    name = name.lower()
    #Execute a sql command to get the id of the role and the rgroup of the role
    data = getDataExecute('SELECT text FROM Message WHERE id=?',[name])
    #Check if the data non existing
    if data is None:
        #return None 2 times
        return None
    #Return first row of data
    return data[0]
def get(msg ,**args):
    out = getMessage(msg)
    if out is None:
        return 'Error, locale not found for {}'.format(msg)
    try:
        return out.format(**args)
    except:
        return 'Error, in formatting {}'.format(msg)
if __name__=='__main__':
    checkDB()
    #addMessage('role.noroles','❌ **{author}**, Er zijn geen rollen gevonden')
    addMessage('role.deleted','✔️ **{author}**, De rol is succesvol verwijderd!')

###################
# Word processing #
###################
#Check WordDB
def checkWordDB():
    #Run an sql that returns 1 if a table exists
    exists = getIntExecute("select 1 from sqlite_master where type='table' and name='Words'",[])
    #return nothing if it exists
    if exists:
        return
    #Create table for the database
    voidExecute("CREATE TABLE Words\
     (word TEXT PRIMARY KEY NOT NULL,\
     amount INT\
     );",[],commit=True)

#Check if message is usefull for things
def checkIsUsable(msg):
    #Check if there are spaces in the message
    if not ' ' in msg:
        #Return false if not
        return False
    #Check if the message is longer than 9 characters
    if len(msg) < 9:
        #Return false if not
        return False
    #Check if message contains at least 3 words
    if len(msg.split(' ')) < 2:
        #Return false if not
        return False
    #Return true if it is a good message
    return True

#Change the line to a array of words
def msgToWords(msg):
    #Split all words
    words = word_tokenize(msg)
    #Create an array for newly processed words
    lw = []
    #Loop thru all current words
    for w in words:
        #Check it the word is only letters
        if w.isalpha():
            #Add it to the newly proccesd words
            lw.append(w)
    #Return the newly processed words
    return lw

#Add the processed words to the database
def addWordToDB(words):
    #Loop thru all the words
    for word in words:
        #Check if the word is already in the database
        out = getIntExecute('SELECT EXISTS(SELECT 1 FROM Words WHERE word=?);',[word])
        #Check if it is 0 or None
        if out is None or out == 0:
            #Add a row to the database
            voidExecute('INSERT INTO Words(word,amount)\
    VALUES (?,1)',[word])
        #If update the row in the database
        else:
            #Execute to sql command to update the words
            voidExecute('UPDATE Words SET amount = amount + 1 WHERE word = ?',[word])
    #Save the database
    db.commit()