import requests

class RegistryChecker:
    def __init__(self):
        self.cbr_api = "https://cbr.ru/inside/warning-list/"

    def check_cbr_blacklist(self, inn, name):
        return False 

    def check_bankruptcy(self, inn):
        return False