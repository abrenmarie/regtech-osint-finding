import requests

class CBRChecker:
    def __init__(self):
        self.blacklist_url = "https://cbr.ru/inside/warning-list/" 

    def check_blacklist(self, inn, name):
        is_blacklisted = False 
        return is_blacklisted