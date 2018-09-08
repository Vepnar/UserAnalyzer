from bot import dbot as bot,discord
import discordutil as du

#Run this when bot is started
@bot.event
async def on_ready():
    #Show the username
    print('Logged in as {}'.format(bot.user.name))
    #Update the 'playing'
    await bot.change_presence(game=discord.Game(name='$'))
    #Show that the game is changed in the terminal
    print('Game changed!')

#TODO add a help thingy
async def sendHelp(msg):
    pass

#TODO Add levels
#TODO Add user analystics
#Used to process words in the message
def processMessage(msg):
    #Process the message and increase the word quality
    con = ' '.join(du.splitCmd(msg.content,delfirst=0))
    print(con)
    #Get the author of the message
    author = msg.author
    #Check the lenght of the message
    if len(con) > 7 and len(con) > 256:
        #Stop event if too long or too short
        return
    #Check if the first letter is a character or number
    if not con[0].isalpha():
        #Stop if it is not a letter
        return
    #Check if in cooldown
    if du.isInCooldown('\x01',author.id):
        #Stop if in the cooldown
        return
    #Check if message is usable
    if not du.checkIsUsable(con):
        #Stop if not usable
        return
    #Turn message into words
    words = du.msgToWords(con)
    #Add words to database
    du.addWordToDB(words)
    #Put a cooldown on the player
    du.putCooldown('\x01',author.id,60)
    
    
#Message event
@bot.event
async def on_message(message):
    #Check if the sender is a bot
    if message.author.bot:
        #Stop if it is a bot
        return
    #Check if the message starts with $help
    elif message.content.startswith('$help'):
        #Send help information if requested
        await sendHelp(message)
        #Stop the event
        return
    processMessage(message)
    #Command processing here
    await bot.process_commands(message)