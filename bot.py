# -*- encoding: utf-8 -*-
import asyncio
import importlib
import os
import discordutil as du
#import useNetwork as AI

import discord
from discord.ext import commands

#Set variables 
uptime = 0
cooldowns = []
dbot = None

async def backgroundProcess():
    global cooldowns,uptime
    #Begin counting uptime
    #Wait until the bot is ready
    await dbot.wait_until_ready()
    #Start loop of checking stuff
    while True:
        #Add 1 second to the uptime
        uptime+=1
        #Create a list for deleting items
        dellist = []
        #Go thru all items in the cooldown list
        for i in range(len(cooldowns)):
            #Remove 1 second of the cooldown
            cooldowns[i].tick()
            #Check if cooldown is deletable
            if cooldowns[i].remove:
                #Add item to delete list
                dellist.append(i)
        #Go thru all deletable items
        for item in dellist:
            #delete item from cooldown
            del cooldowns[item]
        #Sleep 1 second using asynchronous
        await asyncio.sleep(1)


#No comments for you
#it was hard to write
#so it should be hard to read
def registerCommands():
    module = importlib.import_module('commands')
    globals().update(
        {n: getattr(module, n) for n in module.__all__} if hasattr(module, '__all__') 
        else 
        {k: v for (k, v) in module.__dict__.items() if not k.startswith('_')
    })
#Init the databases and classes
def init():
    #Start the database itself
    du.checkDB()
    #Check locale part
    du.checkLocaleDB()
    #Check user part
    du.checkUserDB()
    #Check role part
    du.checkRoleDB()
    #Check word part
    du.checkWordDB()

#Start the bot
def start(token):
    global dbot,cooldowns
    #set variables here so it wont be reset when this file is imported
    cooldowns = []
    #create the bot
    dbot =commands.Bot(command_prefix='$' ,description='An User analyzing bot')
    #Register commands
    registerCommands()
    #Run all inits
    init()
    #Register background process
    dbot.loop.create_task(backgroundProcess())
    #Run the bot
    dbot.run(token)