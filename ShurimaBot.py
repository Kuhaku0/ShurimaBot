from Settings import API_KEY
from Settings import TOKEN
import requests
import discord
from discord.ext import commands


Shurima = discord.Client()
bot_prefix = "s."
shurima = commands.Bot(command_prefix=bot_prefix)
summoners_list = dict()


@shurima.event
async def on_ready():

    shurima.send_message(shurima.get_channel("427772573313531904"), "use command s.h")
    await shurima.change_presence(game=discord.Game(name="s.h"))


def get_info(summoner_name):

    url = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'\
        .format(summoner_name, API_KEY)
    result = requests.get(url).json()
    return result


@shurima.command(pass_context=True)
async def summoner(summoner_name):
    global summoners_list
    if str(summoner_name.message.content) == "s.summoner":
        name = summoners_list.get(str(summoner_name.message.author))
    else:
        name = summoner_name.message.content[11:]
    info = get_info(name)
    summoner_id = info["id"]
    summoner_level = info["summonerLevel"]
    url = 'https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}?api_key={}'\
        .format(summoner_id, API_KEY)
    result = requests.get(url).json()

    await shurima.say("{} : Level {} :".format(name, summoner_level))

    if result:
        queue_type = ""
        for i in result:
            if i["queueType"] == 'RANKED_SOLO_5x5':
                queue_type = "Solo/Duo"
            elif i["queueType"] == 'RANKED_FLEX_SR':
                queue_type = "Flex"
            elif i["queueType"] == 'RANKED_FLEX_TT':
                queue_type = "Flex 3c3"

            ranking = "{} : Rank : {} {} | League Points : {} | Wins : {} | Losses {}". \
                format(queue_type, i['tier'], i['rank'], i['leaguePoints'], i['wins'], i['losses'])

            await  shurima.say(ranking)
    else:
        await shurima.say("Unranked")


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
                          "3. s.summoner [summoner_name] \n"
                          "4. s.add_summoner [summoner_name] \n"
                          "5. s.bestplayer")
    else:
        await shurima.say("List of Command : \n"
                          "1. s.h \n"
                          "2. s.summoner [summoner_name] \n"
                          "3. s.bestplayer \n"
                          "4. s.add_summoner [summoner_name]")


@shurima.command(pass_context=True)
async def add_summoner(summoner_name):

    summoners = dict()
    summoners[str(summoner_name.message.author)] = str(summoner_name.message.content[15:])
    global summoners_list
    summoners_list.update(summoners)


@shurima.command(pass_context=True)
async def bestplayer():
    await shurima.say("Drouyg Beard est le plus Mauvais :3")


@shurima.command(pass_context=True)
async def test():

    await shurima.say("test function")


shurima.run(TOKEN)
