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
    print("Log")


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


shurima.run(TOKEN)
