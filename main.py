#Discord stuff
import bot

if __name__ == '__main__':
    #Used for the discord bot to login
    token = ''

    #Open file with token that you cant read
    with open('/home/arjan/discord.tkn','r') as f:
        #Read first line and get rid of newline character
        token = f.readline()[:-1]
    
    #Start the discord bot
    bot.start(token)


