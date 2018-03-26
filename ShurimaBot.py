from Settings import API_KEY
import requests


def get_info(summoner_name):
    url = 'https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}'.format(summoner_name, API_KEY)
    r = requests.get(url)
    result = r.json()
    return result


def summoner():
    summoner_name = input("Tapez votre nom d'invocateur : ")
    info = get_info(summoner_name)
    summoner_id = info["id"]
    url = 'https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}?api_key={}'.format(summoner_id, API_KEY)
    r = requests.get(url)
    result = r.json()

    solo_q = ["rank : {} {}".format(result[1]['tier'], result[1]['rank']),
              "League Points : {}".format(result[1]['leaguePoints']),
              "Wins : {}".format(result[1]['wins']),
              "Losses : {}".format(result[1]['losses'])]

    flex = ["rank : {} {}".format(result[0]['tier'], result[0]['rank']),
            "League Points : {}".format(result[0]['leaguePoints']),
            "Wins : {}".format(result[0]['wins']),
            "Losses : {}".format(result[0]['losses'])]
    print("Solo/Duo : ")
    for i in solo_q:
        print(i, end=" | ")

    print("\n")
    print("Flex : ")
    for y in flex:
        print(y, end=" | ")


summoner()


