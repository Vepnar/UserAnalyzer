from bot import dbot as bot
import discordutil as du

#Add role command
@bot.command(pass_context=True)
async def addrole(ctx):
    #Get the author
    author = ctx.message.author
    #Parse the args from the command
    args = du.splitCmd(ctx.message.content)
    #Check if the user has permission to add roles
    if du.hasPermissions(author) < 1:
        #Send a message if they dont
        await ctx.send(du.get('role.nopermission',author=author.name,level=2))
        #Stop everything
        return
    #Check if there is 1 role mention
    if not len(ctx.message.role_mentions) == 1:
        #Send message if dont
        await ctx.send(du.get('role.onemention',author=author.name))
        #Stop everything
        return
    #Store the role in a easier to use way
    role = ctx.message.role_mentions[0]
    #Check how the command is used
    if len(args)==1:
        #Create the role
        if not du.createRole(role.id,args[0],0):
            #Send a message if the creation failed
            await ctx.send(du.get('role.createfailed',author=author.name))
        else:
            #Send a message if it was successfull
            await ctx.send(du.get('role.createsuccessfull',author=author.name,role=args[0]))
    elif len(args)==2:
        #Turn second argument into a int
        group = du.getInt(args[1])
        #Check if the int is nothing
        if group is None:
            #Send a error message that it is not an int
            await ctx.send(du.get('role.notanumber',author=author.name))
            #Stop everything
            return
        #Try to create to role
        if not du.createRole(role.id,args[0],group):
            #Send a message that it failed
            await ctx.send(du.get('role.createfailed',author=author.name))
        else:
            #Send a message that it was successfull
            await ctx.send(du.get('role.createsuccessfull',author=author.name,role=args[0]))
    else:
        #Send the help messgae
        await ctx.send(du.get('role.addhelp'))
    
#Get a role command
# Group lower than 0 is only optainable thru events
# Group higher than 0 can conflict with other roles
# Group with 0 is selectable for users without any problem
@bot.command(pass_context=True)
async def role(ctx): 
    #Get the author
    author = ctx.message.author
    #Get the server
    server = author.guild
    #Parse the args from the command
    args = du.splitCmd(ctx.message.content)
    #Check if the args are right
    if len(args) == 1:
        #Get the id of the role and the group
        roleId,group = du.getRole(args[0])
        #Check if the role exists
        if roleId is None:
            #Send a not found message if the role is not found
            await ctx.send(du.get('role.notfound',author=author.name))
        #Check if the role is selectable
        elif 0>group: 
            #Send error if it is not
            await ctx.send(du.get('role.notavailable',author=author.name))
        #Check if it is a group role
        elif 0<group:
            #Get all the other roles in the group from the database
            ids = du.getRolesByGroup(group)
            #Make an empty array for the roles
            noroles = []
            #Loop thru the data from the database
            for norole in ids:
                #Parse the id of the role and add it to the new array
                noroles.append(norole[0])
            #Loop thru all the roles of the author
            for role in author.roles:
                #Check if the role of the author conflicts with the new one
                if role.id in noroles:
                    #Remove the conflicting one
                    await author.remove_roles(role)
            #Look for the new role
            for role in server.roles:
                #Check if it is the new role
                if roleId == role.id:
                    #Add the new role
                    await author.add_roles(role)
                    #Send a message if the new role is added
                    await ctx.send(du.get('role.added',author=author.name))
                    #Stop this
                    return
            #Send a message that the new role is not found
            await ctx.send(du.get('role.notfound',author=author.name))
        #Check if the role is group type 0
        elif group == 0:
            #Check if the user already has this role
            for role in author.roles:
                #Check if the id is the smae
                if roleId == role.id:
                    #Remove it
                    await author.remove_roles(role)
                    #Show a message that it is deleted
                    await ctx.send(du.get('role.removed',author=author.name))
                    #Stop everything
                    return
            #Look for the new roles
            for role in server.roles:
                #Check if it is the same
                if roleId == role.id:
                    #Add it
                    await author.add_roles(role)
                    #Send a message that it is added
                    await ctx.send(du.get('role.added',author=author.name))
                    #Stop this
                    return
            #Send a message that the new role is not found
            await ctx.send(du.get('role.notfound',author=author.name))
    else:
        #Send a help message
        await ctx.send(du.get('role.gethelp'))

@bot.command(pass_context=True)
async def roles(ctx): 
    #Get all roles from the database
    roles = du.getRoles()
    #Get the author from the message
    author = ctx.message.author
    #Check if there are roles in the database
    if not roles:
        #Return that there are no roles
        await ctx.send(du.get('role.noroles',author=author.name))
        #Stop this event
        return
    #Get a nice title for the message
    msg = du.get('role.title')
    #Loop thru the roles
    for role in roles:
        #Add the role to the message with formatting
        msg+='\n{:10s} {:3d}'.format(role[0].title(),role[1])
    #Close the message
    msg +='```'
    #And send it
    await ctx.send(msg)
    
@bot.command(pass_context=True)
async def delrole(ctx):
    #Get the author
    author = ctx.message.author
    #Parse the args from the command
    args = du.splitCmd(ctx.message.content)
    #Check if the user has permission to add roles
    if du.hasPermissions(author) < 1:
        #Send a message if they dont
        await ctx.send(du.get('role.nopermission',author=author.name,level=2))
        #Stop everything
        return
    #Check the args
    if not len(args) == 1:
        #Send message if dont
        await ctx.send(du.get('role.onemention',author=author.name))
        #Stop everything
        return
    #Execute a sql command to delete the role
    du.voidExecute('DELETE FROM Roles WHERE name=?',[args[0]])
    #Send a message that it was successful
    await ctx.send(du.get('role.deleted',author=author))