"""discordにメッセージを送るスクリプト
    引数にトークンを渡すと動きます
"""

import sys
import asyncio
import discord

CLIENT = discord.Client()
TOKEN = sys.argv[1]
CONNECTING = True


@CLIENT.event
async def on_ready():
    """いつもの
    いつものon_ready君だよ
    接続1回目に入るチャンネル決めてループぶん回すよ
    """
    global CONNECTING
    channels = CLIENT.get_all_channels()
    i = 0
    if CONNECTING:

        for channel in channels:
            print("{}: {}".format(i, channel.name))
            i += 1
        selected = input("何番のチャンネルに接続しますか?\n")
        i = 0
        channels = CLIENT.get_all_channels()
        selected_channel_id = 0

        for channel in channels:
            if i == int(selected):
                selected_channel_id = channel.id
                break
            i += 1
        selected_channel = CLIENT.get_channel(selected_channel_id)
        asyncio.ensure_future(sender(selected_channel))
        CONNECTING = False


async def sender(channel):
    """
    Exitって入力するまで入力された文字をdiscordに文章を送ります
    Args:
        channel(Discord.Channel): 最初にメッセージを送る先です
    """
    while True:
        input("\033[2mPress Enter...\033[m")
        async with channel.typing():
          message = input("\033[1m>>>")

        if len(message.strip()) == 0:
            continue
        
        print("\033[m", end="")
        if message == ":exit":
            exiter()
        if message == ":change":
            channel = select_channel()
            continue
        emojis = list(await channel.guild.fetch_emojis())
        if message.count(":") >= 2:
            mess_list = list(message)
            colons = []
            i = 0
            info = {"del": [], "emoji": []}
            for charactor in message:
                if charactor == ":":
                    colons.append(i)
                i += 1

            encount = 0
            for raw_emoji in emojis:
                for i in range(len(colons) - 1):
                    if encount == 0:
                        encount -= 1
                        continue
                    if raw_emoji.name == message[colons[i] + 1: colons[i + 1]]:
                        info["del"].append([colons[i], colons[i+1]])
                        info["emoji"].append(raw_emoji)
                        encount = 2
            print(info)
            deleted = 0
            for i in range(len(info["del"])):
                delete_start = info["del"][i][0] - deleted
                delete_end = info["del"][i][1] - deleted + 1

                del mess_list[delete_start: delete_end]
                mess_list.insert(info["del"][i][0] - deleted, "{}")
                deleted += info["del"][i][1] - info["del"][i][0]
                print(info["del"][i][0])
            message = "".join(mess_list)
            for i in info["emoji"]:
                print(i)
                print(message)
                message = message.replace("{}", str(i), 1)

        await channel.send(message)

def select_channel():
    """
    Returns:
        Discord.Channel
    """
    channels = CLIENT.get_all_channels()
    i = 0
    for channel in channels:
        print("{}: {}".format(i, channel.name))
        i += 1
    selected = input("何番のチャンネルに接続しますか?")
    i = 0
    channels = CLIENT.get_all_channels()
    selected_channel_id = 0
    for channel in channels:
        if i == int(selected):
            selected_channel_id = channel.id
            break
        i += 1
    selected_channel = CLIENT.get_channel(selected_channel_id)
    return selected_channel

def exiter():
    """
    :exitの実装 なんで関数化してるかというと、深い事情があります
    Args:
        なんもない
    Returns:
        なんもない
    """
    print ("クライアントを終了します...")
    print ("理由はわかりませんがこれにはしばらく時間がかかります...")
    sys.exit()

CLIENT.run(TOKEN)
