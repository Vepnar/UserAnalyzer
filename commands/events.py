from bot import dbot as bot,discord

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
    #Command processing here
    await bot.process_commands(message)