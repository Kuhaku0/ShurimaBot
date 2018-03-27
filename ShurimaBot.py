from Settings import API_KEY
from Settings import TOKEN
import requests
import discord
from discord.ext import commands


Shurima = discord.Client()
bot_prefix = "s."
shurima = commands.Bot(command_prefix=bot_prefix)


@shurima.event
async def on_ready():

    shurima.send_message(shurima.get_channel("427772573313531904"), "use commande s.h")


def get_info(summoner_name):

    url = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'\
        .format(summoner_name, API_KEY)
    r = requests.get(url)
    result = r.json()
    return result


@shurima.command(pass_context=True)
async def summoner(summoner_name):

    name = summoner_name.message.content[11:]
    info = get_info(name)
    summoner_id = info["id"]
    url = 'https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}?api_key={}'\
        .format(summoner_id, API_KEY)
    r = requests.get(url)
    result = r.json()

    if result:
        solo_q = "{} : Solo/Duo : Rank : {} {} | League Points : {} | Wins : {} | Losses {}".\
            format(name, result[1]['tier'], result[1]['rank'], result[1]['leaguePoints'], result[1]['wins'],
                   result[1]['losses'])
        flex = "{} : Flex : Rank : {} {} | League Points : {} | Wins : {} | Losses {}".\
            format(name, result[0]['tier'], result[0]['rank'], result[0]['leaguePoints'], result[0]['wins'],
                   result[0]['losses'])
        await shurima.say(solo_q)
        await shurima.say(flex)
    else:
        await shurima.say("{} : Unranked".format(name))


@shurima.command(pass_context=True)
async def config(ctx):

    srv = ctx.message.server
    role = ctx.message.author.roles
    srv_role = []
    srv_role_object = ctx.message.server.roles
    lst_role = ["Challenger", "Master", "Diamant", "Platine", "Gold", "Silver", "Bronze", "Unranked"]

    for i in srv_role_object:
        srv_role.append(str(i))

    if "admin" in [i.name.lower() for i in role]:
        await shurima.say("Creating roles ...")
        for i in lst_role:
            if i not in srv_role:
                shurima.create_role(srv, name=i)
        await shurima.say("command help s.h")
    else:
        await shurima.say("You have not the permission for execute this command")


@shurima.command(pass_context=True)
async def h(ctx):

    author_role = ctx.message.author.roles

    if "admin" in [i.name.lower() for i in author_role]:
        await shurima.say("List of Command : \n"
                          "1. s.h \n"
                          "2. s.config \n"
                          "3. s.summoner [summoner_name]")
    else:
        await shurima.say("List of Command : \n"
                          "1. s.h \n"
                          "2. s.summoner [summoner_name]")


@shurima.command(pass_context=True)
async def test(ctx):

    test = ctx.message.server.roles
    lst = ["Challenger"]
    for i in test:
        y = str(i)
        if y in lst:
            print('la')
        else:
            print(y)
            print(lst)


shurima.run(TOKEN)
