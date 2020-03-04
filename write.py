import discord
import sys
import asyncio

client = discord.Client()
token = sys.argv[1]


@client.event
async def on_ready():
    channels = client.get_all_channels()
    i = 0
    for ch in channels:
        print("{}: {}".format(i, ch.name))
        i += 1
    selected = input("何番のチャンネルに接続しますか?")
    i = 0
    channels = client.get_all_channels()
    selected_channel_id = 0
    for ch in channels:
        if i == int(selected):
            selected_channel_id = ch.id
            break
        i += 1
    selected_channel = client.get_channel(selected_channel_id)
    await selected_channel.send("ユーザーが来ました")
    asyncio.ensure_future(sender(selected_channel))


async def sender(channel):
    while True:
        message = input()
        if message == ":change":
            channel = select_channel()
            continue
        await channel.send(message)


def select_channel():
    channels = client.get_all_channels()
    i = 0
    for ch in channels:
        print("{}: {}".format(i, ch.name))
        i += 1
    selected = input("何番のチャンネルに接続しますか?")
    i = 0
    channels = client.get_all_channels()
    selected_channel_id = 0
    for ch in channels:
        if i == int(selected):
            selected_channel_id = ch.id
            break
        i += 1
    selected_channel = client.get_channel(selected_channel_id)
    return selected_channel


client.run(token)
