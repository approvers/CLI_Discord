import discord
import sys
import asyncio

token = sys.argv[1]
client = discord.Client()
guild = None

TEMPLATE = "\033[48;5;{};38;5;007;1m {} \033[48;5;{};38;5;016m {} \033[m"

CHANNEL_COLOR_LIST = [
    69, 70, 97, 130, 166, 178, 214
]

AUTHOR_COLOR_LIST = [
    123, 190, 195, 219, 225, 229
]

channel_history = []
author_history = []


def get_channel_color(channel):
    # 履歴を探る
    if channel.name not in channel_history:
        channel_history.append(channel.name)
    channel_index = channel_history.index(channel.name)
    channel_color = CHANNEL_COLOR_LIST[channel_index % len(CHANNEL_COLOR_LIST)]

    return channel_color

def get_user_color(author):
    if author.display_name not in author_history:
        author_history.append(author.display_name)
    
    author_index = author_history.index(author.display_name)
    author_color = AUTHOR_COLOR_LIST[author_index % len(AUTHOR_COLOR_LIST)]

    return author_color


@client.event
async def on_ready():
    global guild

    guild = client.guilds[0]
    print("\033[2J")
    print("\033[1;1H")
    
    print("\033[48;5;069;1m {} \033[m\033[48;5;069mに接続しています \033[m".format(guild.name))
    print()


@client.event
async def on_message(message):
    
    channel_color = get_channel_color(message.channel)
    author_color = get_user_color(message.author)

    print(TEMPLATE.format(channel_color, message.channel.name, author_color, message.author.display_name))
    print("  " + message.content)
    print()

@client.event
async def on_typing(channel, user, when):
    author_color = get_user_color(user)
    print("\033[38;5;{};2m{}がタイピング中です\033[m".format(author_color, user.display_name))

@client.event
async def on_member_update(before: discord.Member, after: discord.Member):
    status: discord.Status = after.status
    status_text = ""

    if status == discord.Status.online:
        status_text = "オンライン"
    elif status == discord.Status.idle:
        status_text = "放置中"
    elif status == discord.Status.dnd:
        status_text = "お取り込み中"
    elif status == discord.Status.offline:
        status_text = "オフライン"
    else:
        status_text = "█████中"

    author_color = get_user_color(after)
    print("\033[38;5;{};2m{}は{}です\033[m".format(author_color, after.display_name, status_text))

client.run(token)
