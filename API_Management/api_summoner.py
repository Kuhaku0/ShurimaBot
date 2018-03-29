from Settings import API_KEY
import requests


class Summoner:

    def __init__(self, summoner_name):
        url = "https://euw1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}?api_key={}"\
            .format(summoner_name, API_KEY)
        self.summoner_info = requests.get(url).json()

    def get_summoner_profile_icon_id(self):
        return self.summoner_info["profileIconId"]

    def get_summoner_level(self):
        return self.summoner_info["summonerLevel"]

    def get_summoner_id(self):
        return self.summoner_info["id"]
