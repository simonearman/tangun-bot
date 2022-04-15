import discord
from dotenv import load_dotenv
from os import getenv
from random import randint

client = discord.Client()
load_dotenv()


@client.event
async def on_ready():
    print(f"Ready! Logged in as {client.user}")


@client.event
async def on_message(message):
    if message.author.bot or not message.content.startswith("s!"):
        return
    args = message.content[2:].split()
    command = args.pop(0).lower()
    if command == "ping":
        await message.channel.send("pong")
    elif command == "say":
        await message.delete()
        await message.channel.send(" ".join(args))
    elif command == "rng":
        if len(args) == 1:
            rng_min = 1
        else:
            rng_min = int(args.pop(0))
        rng_max = int(args.pop(0))
        await message.channel.send(f"Losowa liczba od {rng_min} do {rng_max}: **{randint(rng_min, rng_max)}**")

client.run(getenv("TOKEN"))
