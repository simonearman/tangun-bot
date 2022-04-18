import discord
from dotenv import load_dotenv
from os import getenv
from random import randint
from helpers import find_private_role

client = discord.Client(intents=discord.Intents(guilds=True, members=True, messages=True))
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
        if len(args) == 0:
            return
        if len(args) == 1:
            rng_min = 1
        else:
            rng_min = int(args.pop(0))
        rng_max = int(args.pop(0))
        await message.channel.send(f"Losowa liczba od {rng_min} do {rng_max}: **{randint(rng_min, rng_max)}**")
    elif command == "role":
        option = args.pop(0)
        if option == "info":
            role = find_private_role(message.author)
            await message.channel.send(f"Właściciel roli: {role.members[0].mention}\n"
                                       f"Nazwa roli: **{role.name}**\n"
                                       f"Kolor roli: **{role.color}**")
        elif option == "name":
            if len(args) == 0:
                return
            role = find_private_role(message.author)
            role_name = " ".join(args)
            await role.edit(name=role_name)
            await message.channel.send(f"Twoja rola nazywa się teraz **{role_name}**")
        elif option == "color":
            if len(args) == 0:
                return
            role = find_private_role(message.author)
            if args[0].startswith("#"):
                args[0] = args[0][1:]
            if len(args[0]) > 6:
                await message.channel.send(f"**#{args[0]}** nie jest poprawnym kolorem heksadecymalnym (maksymalnie 6 cyfer)")
                return
            try:
                role_color = int(args[0], 16)
            except ValueError:
                await message.channel.send(f"**#{args[0]}** nie jest poprawnym kolorem heksadecymalnym (0-9, A-F)")
                return
            await role.edit(color=role_color)
            await message.channel.send(f"Twoja rola posiada teraz kolor **#{hex(role_color)[2:]}**")

client.run(getenv("TOKEN"))
