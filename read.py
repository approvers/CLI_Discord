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

typing_condition = []

latest_typer = -1

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
    
    print("\033[48;5;069;1m {} \033[m\033[;48;5;069mに接続しています \033[m".format(guild.name))
    print()


@client.event
async def on_message(message):
    global  latest_typer

    channel_color = get_channel_color(message.channel)
    author_color = get_user_color(message.author)
    
    no_typing_interrpution = len(typing_condition) > 0 and typing_condition[-1] == message.author.id
    
    # 最後に「打込中」と表示された人と、
    # メッセージを送信した人が一致した場合は、
    # コンソールをキレイにするために打込み中表示を消す
    if no_typing_interrpution:
        print("\033[1A\033[2K", end="")
        if latest_typer == message.author.id:
            print("\033[1A\033[2K", end="")
    
    if latest_typer != message.author.id:
        print(TEMPLATE.format(channel_color, message.channel.name, author_color, message.author.display_name))
    print("  " + message.content)
    print("  " + str(typing_condition))
    print()
    
    latest_typer = message.author.id
    typing_condition.clear()

@client.event
async def on_typing(channel, user, when):
    author_color = get_user_color(user)

    if user.id not in typing_condition:
        typing_condition.append(user.id)
        print("\033[48;5;128;1m 打込 \033[;38;5;{};1m {} \033[m".format(author_color, user.display_name))

@client.event
async def on_member_update(before: discord.Member, after: discord.Member):

    STATUS_DISPLAY_INFO = {
        discord.Status.online : [28, "オン"],
        discord.Status.idle   : [32, "放置"],
        discord.Status.dnd    : [160, "取込"],
        discord.Status.offline: [240, "オフ"],
    }

    status: discord.Status = after.status
    status_text = ""
    
    # ステータス以外の変化でもこのイベントは引っかかるので、
    # とりあえずステータス以外の変更は弾いておく
    if before.status == after.status:
        return

    typing_condition.append(-1)
    
    status_color, prefix = STATUS_DISPLAY_INFO[after.status]

    author_color = get_user_color(after)
    print("\033[48;5;{};1m {} \033[;38;5;{};1m {} \033[m".format(status_color, prefix, author_color, after.display_name))

client.run(token)
