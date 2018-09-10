# UserAnalyzer
A discord bot that analyses word usage.

## Commands
Commands are called with `$`.

### Roles

**$addrole** `@rolemention rolename [group]`  
_This command is for administrators_  
Makes a given role available.
- `group = 0` - No limits
- `group = -1` (negative) - Makes a role only obtainable through events.
- `group = 1` (postive higher than 0) - Makes a role conflict with other roles with the same value. Users will only be able to obtain one of the roles in a certain group. 

**$delrole** `rolename`  
_This command is for administrators_  
Makes a given role unavailable.

**$roles**  
_Everyone can use this command_  
Gives a list of every available role.

**$role** `rolename`  
_Everyone can use this command_  
If available, gives user the given role.
