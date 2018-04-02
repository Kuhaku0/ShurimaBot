from Settings import API_KEY
import requests


class League:

    def __init__(self, summoner_id):
        url = 'https://euw1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}?api_key={}' \
            .format(summoner_id, API_KEY)
        self.summoner_league = requests.get(url).json()

    def get_summoner_rank(self):
        summoner_rank = "{} {}"\
            .format(self.summoner_league["tier"], self.summoner_league["rank"])
        return summoner_rank

    def get_summoner_queue_type(self):
        return self.summoner_league["queueType"]

    def get_summoner_hot_streak(self):
        return self.summoner_league["hotStreak"]

    def get_summoner_mini_series(self):
        return self.summoner_league["miniSeries"]

    def get_summoner_wins(self):
        return self.summoner_league["wins"]

    def get_summoner_veteran(self):
        return self.summoner_league["veteran"]

    def get_summoner_losses(self):
        return self.summoner_league["losses"]
