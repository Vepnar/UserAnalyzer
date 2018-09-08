# UserAnalyzeer
A discord bot that analyses word usage  

## Commands
all the commands start with `$`  

### Roles

**$addrole** `@rolemention rolename [group]`  
_This command is for administrators_  
They can use this command to make a role optainable  
group = 0 not conflicting with any other group  
group = -1 (negative) this role is only optainable thru events  
group = 1 (postive higher than 0) this role will conflict with other roles from the same group  

**$delrole** `rolename`  
_This command is for administrators_  
They can use this command to make a role not optainable  

**$roles**  
_Everyone can use this command_  
You can use it to show all the roles  

**$role** `rolename`  
_Everyone can use this command_  
You can use this command to get a role that is optainable  
