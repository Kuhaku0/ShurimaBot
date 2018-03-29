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
    em = discord.Embed(title="{}".format(name), description="Level : {}".format(summoner_level))

    url = 'https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}?api_key={}'\
        .format(summoner_id, API_KEY)
    result = requests.get(url).json()

    if result:
        for i in result:
            if i["queueType"] == 'RANKED_SOLO_5x5':
                em.add_field(name="Solo/Duo", value="Rank : {} {} \nLeague Points : {} \nWins : {} | Losses : {}"
                             .format(i['tier'], i['rank'], i['leaguePoints'], i['wins'], i['losses']), inline=True)
            elif i["queueType"] == 'RANKED_FLEX_SR':
                em.add_field(name="Flex 5c5", value="Rank : {} {} \nLeague Points : {} \nWins : {} | Losses : {}"
                             .format(i['tier'], i['rank'], i['leaguePoints'], i['wins'], i['losses']), inline=True)
            elif i["queueType"] == 'RANKED_FLEX_TT':
                em.add_field(name="Flex 3c3", value="Rank : {} {} \nLeague Points : {} \nWins : {} | Losses : {}"
                             .format(i['tier'], i['rank'], i['leaguePoints'], i['wins'], i['losses']), inline=True)
    else:
        em.add_field(name="Unraked", value="None")

    await shurima.say(embed=em)


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
        em = discord.Embed(title="Liste Of commands", description="List of Command : \n"
                                                                  "1. s.h \n"
                                                                  "2. s.summoner [summoner_name] \n"
                                                                  "3. s.bestplayer \n"
                                                                  "4. s.add_summoner [summoner_name]\n"
                                                                  "5. s.config")
        await shurima.say(embed=em)
    else:
        em = discord.Embed(title="Liste Of commands", description="List of Command : \n"
                                                                  "1. s.h \n"
                                                                  "2. s.summoner [summoner_name] \n"
                                                                  "3. s.bestplayer \n"
                                                                  "4. s.add_summoner [summoner_name]")
        await shurima.say(embed=em)


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
    '''embed = discord.Embed(title="title ~~(did you know you can have markdown here too?)~~",
                          colour=discord.Colour(0xda4294), url="https://discordapp.com",
                          description="this supports on top of the previously shown subset of markdown.",
                          timestamp=datetime.datetime.utcfromtimestamp(1522161520))

    embed.set_image(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_thumbnail(url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_author(name="author name", url="https://discordapp.com",
                     icon_url="https://cdn.discordapp.com/embed/avatars/0.png")
    embed.set_footer(text="footer text", icon_url="https://cdn.discordapp.com/embed/avatars/0.png")

    embed.add_field(name="🤔", value="some of these properties have certain limits...")
    embed.add_field(name="😱", value="try exceeding some of them!")
    embed.add_field(name="🙄",
                    value="an informative error should show up, and this view will remain as-is until all issues are 
                    fixed")
    embed.add_field(name="<:thonkang:219069250692841473>", value="these last two", inline=True)
    embed.add_field(name="<:thonkang:219069250692841473>", value="are inline fields", inline=True)

    await shurima.say(
        content="this `supports` __a__ **subset** *of* ~~markdown~~ 😃 ```js\nfunction foo(bar) {\n  console.log(bar);\n
        }\n\nfoo(1);```",
        embed=embed)'''


shurima.run(TOKEN)
