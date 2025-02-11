
import discord
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True  # Make sure to enable member intents

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')

    # The user that should not be kicked (replace with actual user ID)
    exempt_user_id = # Change this to the user ID you want to exempt

    # Fetch the server (replace with your server ID)
    guild = bot.get_guild(1334865937882677311)  # Change this to your server ID

    # Kick all members except the exempt one
    for member in guild.members:
        if member.id != exempt_user_id:
            try:
                await member.kick(reason="Server lockdown")
                print(f"Kicked {member.name}")
            except discord.Forbidden:
                print(f"Could not kick {member.name}, missing permissions.")
            except discord.HTTPException as e:
                print(f"Error while kicking {member.name}: {e}")

    # Delete all roles except default ones (like @everyone)
    for role in guild.roles:
        if role.name != "@everyone":
            try:
                await role.delete(reason="Server lockdown")
                print(f"Deleted role {role.name}")
            except discord.Forbidden:
                print(f"Could not delete {role.name}, missing permissions.")
            except discord.HTTPException as e:
                print(f"Error while deleting role {role.name}: {e}")

    # Delete all channels
    for channel in guild.channels:
        try:
            await channel.delete(reason="Server lockdown")
            print(f"Deleted channel {channel.name}")
        except discord.Forbidden:
            print(f"Could not delete {channel.name}, missing permissions.")
        except discord.HTTPException as e:
            print(f"Error while deleting channel {channel.name}: {e}")

YOUR_BOT_TOKEN = "TOKEN HERE"


bot.run(YOUR_BOT_TOKEN)