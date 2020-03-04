import discord
import sys


token = sys.argv[1]
client = discord.Client()

@client.event
async def on_message(message):
    print("{} : {} / {}".format(message.channel ,message.author, message.content))

client.run(token)
