import re
import random


class SupportBot:
    negatives = ("don't", "stop", "nothing")
    exits = ("bye", "see you", "quit", "pause", "exit", "goodbye", "later")

    def __init__(self):
        self.matching = {"how_to_pay_bill": [r".*how.*pay (a|the) bill.*", r".*where.*pay (a|the|my)? bill.*"],
                         "pay_bill": [r".*want.*pay (a|the|my)? bill.", r".*need.*pay (a|the|my)? bill.*"],
                         "menu": [r".*(can|could)?.*(have|see|bring)? (the)?.* menu.*"],
                         "bathroom": [r".*where.*bathroom.*"]}

    def welcome(self):
        name = input("Hey, my name is Blop. Could you tell me your name, please?\n>")

        task = input(f"Hey {name}, what can I help you with?\n>")
        task = task.lower()
