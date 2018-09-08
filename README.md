# UserAnalyzer
A discord bot that analyses word usage

## Commands
all the commands start with `$`

###Roles
**$addrole** `@rolemention rolename [group]`
__This command is for administrators__
They can use this command to make a role optainable
group = 0 not conflicting with any other group
group = -1 (negative) this role is only optainable thru events 
group = 1 (postive higher than 0) this role will conflict with other roles from the same group

**$delrole** `rolename`
__This command is for administrators__
They can use this command to make a role not optainable

**$roles** 
__Everyone can use this command__
You can use it to show all the roles

**$role** `rolename` 
__Everyone can use this command__
You can use this command to get a role that is optainable