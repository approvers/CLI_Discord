import discord
import sys

token = sys.argv[1]
client = discord.Client()


TEMPLATE = "\033[48;5;{};38;5;007;1m {} \033[48;5;{};38;5;016m {} \033[m"

CHANNEL_COLOR_LIST = [
    69, 70, 97, 130, 166, 178, 214
]

AUTHOR_COLOR_LIST = [
    123, 190, 195, 219, 225, 229
]

channel_history = []
author_history = []

@client.event
async def on_ready():
    print("\033[2J")
    print("\033[1;1H")

@client.event
async def on_message(message):

    # 履歴を探る
    if message.channel.name not in channel_history:
        channel_history.append(message.channel.name)
    if message.author.display_name not in author_history:
        author_history.append(message.author.display_name)
    
    channel_index = channel_history.index(message.channel.name)
    author_index = author_history.index(message.author.display_name)

    channel_color = CHANNEL_COLOR_LIST[channel_index % len(CHANNEL_COLOR_LIST)]
    author_color = AUTHOR_COLOR_LIST[author_index % len(CHANNEL_COLOR_LIST)]

    print(TEMPLATE.format(channel_color, message.channel.name, author_color, message.author.display_name))
    print("  " + message.content)
    print()

client.run(token)
