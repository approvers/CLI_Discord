"""discordにメッセージを送るスクリプト
    引数にトークンを渡すと動きます
"""

import sys
import asyncio
import discord

CLIENT = discord.Client()
TOKEN = sys.argv[1]
CONNECTING = True

def replace_at(string, start, length, new_text):
    """
    指定した文字列の指定した範囲を、指定した文字列で置きかえる。
    :param string: 置き換え対象の文字列
    :param start: 置き換え開始場所
    :param length: 置き換える長さ
    :param new_text: 置き換え後の文字列

    replace_at("ABXXXCD", 2, 3, "--")
    >>> AB--CD
    """

    left = string[:start]
    right = string[start + length:]
    return left + new_text + right


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
            print("空文字送んなカス")
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
        
        # --- メンションを探す
        # 必要なデータを持ってくる
        guild: discord.Guild = CLIENT.guilds[0]
        members = guild.members
        roles = guild.roles

        index = -1
        raw_mentions = []
        # 文字列をパースする
        while index < len(message):
            location = message.find("@", index + 1)
            if location == -1:
                break
            
            # @からあとの部分
            # この直後にユーザー名かロール名が来てれば
            # メンションとして認識されるわけだ
            mention_text = message[message.find("@", index + 1) + 1:]
            for member in members:
                if mention_text.find(member.display_name) == 0 or \
                   mention_text.find(member.name) == 0:
                    raw_mentions.append(member)
                    break
            for role in roles:
                if mention_text.find(role.name) == 0:
                    raw_mentions.append(role)
                    break

            index = location
 
        for raw_mention in raw_mentions:
            if isinstance(raw_mention, discord.Member):
                message = message.replace("@" + raw_mention.display_name, raw_mention.mention)
                message = message.replace("@" + raw_mention.name, raw_mention.mention)
            elif isinstance(raw_mention, discord.Role):
                if not raw_mention.mentionable:
                    print("\033[38;5;208;1m役職「{}」はメンション出来ません\033[m".format(raw_mention.name))
                    print("たぶんロールの設定で無効になってる")
                message = message.replace("@" + raw_mention.name, raw_mention.mention)
            
            print("\033[38;5;120;4mメンション >> {}\033[m".format(raw_mention.name))
        

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
