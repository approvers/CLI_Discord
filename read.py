import discord
import sys
import re
import wave
import pygame.mixer
import atexit

import utils

# --- 起動引数
mention_notify = []

token = sys.argv[1]
client = discord.Client()
guild = None

notify_sound = None

# チャンネル名とユーザー名の書式設定
# CHANNEL_COLOR_LISTと AUTHOR_COLOR_LIST の値によって色が決まる
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
    global guild, mention_notify, notify_sound #TODO: Hey, too many global! Do classificate this asap, loxy!
    guild = client.guilds[0]

    # 起動引数からオプションを取得する
    income_option = ""
    for arg in sys.argv:
        if arg.startswith("--"):
            income_option = arg[2:]
            continue
        elif arg.startswith("-"):
            income_option = arg[1:]
            continue
        
        if income_option == "m" or income_option == "mention":
            mention_notify = arg.split(",")
        income_option = ""
    
    # メンション通知音を読み込む
    pygame.mixer.pre_init(buffer=512)
    pygame.mixer.init()
    notify_sound = pygame.mixer.Sound("./mention_notify.wav")

    # 画面を初期化してカーソルを(1, 1)に持ってく
    print("\033[2J")
    print("\033[1;1H")
    
    # 水色の背景、サーバー名は太字、「に接続しています」は普通の文字
    # そのあと書式設定を解除
    print("\033[48;5;069;1m {} \033[m\033[;48;5;069mに接続しています \033[m".format(guild.name))
    if income_option != "":
        print("\033[38;5;208;1mよくわからんオプション指定がありました\033[m")

    for name in mention_notify:
        print("\033[38;5;192;1m@{}へのメンションは通知対象です\033[m".format(name))
    print()
    
    # ユーザーに通知し終わったあとにeveryoneとhereを通知対象リストに入れる
    mention_notify.append("everyone")
    mention_notify.append("here")


@client.event
async def on_message(message):
    global latest_typer
    
    msg = message.content
    # メンションを探る
    # MITライセンス下のRappptz/discord.pyリポジトリから引っ張ってきたコードを改変して使ってます
    # 具体的には https://github.com/Rapptz/discord.py/blob/5e6335750819588062790c6b93d604d3bc7c3862/discord/utils.py#L503 です
    while True:
        mention_match = re.search(r'<@(everyone|here|[!&]?[0-9]{17,21})>', msg)
        if mention_match is None:
            break
        contents = mention_match[0]
        styled_mention = ""

        if contents == "everyone" or contents == "here":
            mentioned_name = contents
            styled_mention += "\a"
        else:
            mention_id = int(contents[3:-1])
            if contents[2] == "!":
                mentioned_user = guild.get_member(mention_id)
                mentioned_name = mentioned_user.display_name
                if mentioned_user.display_name in mention_notify or mentioned_user.name in mention_notify:
                    styled_mention += "\033[48;5;052m"
                    notify_sound.play()
            elif contents[2] == "&":
                mentioned_name = guild.get_role(int(contents[3:-1])).name
                if mentioned_name in mention_notify:
                    styled_mention += "\033[48;5;052m"
                    notify_sound.play()
        
        styled_mention += "\033[38;5;220;1m@{}\033[m".format(mentioned_name)

        length = mention_match.end() - mention_match.start()
        msg = utils.replace_at(msg, mention_match.start(), length, styled_mention)
    
    # コンソールをキレイにするために、
    # 最後に「打込中」と表示された人と、
    # メッセージを送信した人が一致した場合は、
    # コンソールをキレイにするために打込み中表示を消す
    
    no_typing_interrpution = len(typing_condition) > 0 and typing_condition[-1] == message.author.id
    
    if no_typing_interrpution:
        # 一個上に行く
        print("\033[1A\033[2K", end="")
        if latest_typer == message.author.id:
            # 同じ人が連続して送信した場合はもっと上に行く
            print("\033[1A\033[2K", end="")
        
    channel_color = get_channel_color(message.channel)
    author_color = get_user_color(message.author)
    if no_typing_interrpution and latest_typer != message.author.id:
        # 違う人がタイピングしたらチャンネル名／ユーザー名を書く
        print(TEMPLATE.format(channel_color, message.channel.name, author_color, message.author.display_name))
    
    print("  " + msg)
    print()
    
    latest_typer = message.author.id
    typing_condition.clear()

@client.event
async def on_typing(channel, user, when):
    author_color = get_user_color(user)

    if user.id not in typing_condition:
        typing_condition.append(user.id)
        # 紫背景に「打込」→背景が消えてユーザー固有の色＋太字でユーザー名
        print("\033[48;5;128;1m 打込 \033[;38;5;{};1m {} \033[m".format(author_color, user.display_name))

@client.event
async def on_member_update(before: discord.Member, after: discord.Member):

    STATUS_DISPLAY_INFO = {
        discord.Status.online : [28, "オン"],   # 緑
        discord.Status.idle   : [32, "放置"],   # 若干濁った水色
        discord.Status.dnd    : [160, "取込"],  # 真っ赤ではない赤
        discord.Status.offline: [240, "オフ"],  # 灰色
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
    # ステータスに応じた色が設定される(STATUS_DISPLAY_INFO参照)
    # そのあと、背景色が消えてユーザー固有の色＋太字でユーザー名が描画される
    print("\033[48;5;{};1m {} \033[;38;5;{};1m {} \033[m".format(status_color, prefix, author_color, after.display_name))

def at_exit():
    pygame.quit()

atexit.register(at_exit)
client.run(token)
