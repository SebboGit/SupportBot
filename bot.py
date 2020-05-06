import re
import random
import time
import sys
from nltk import pos_tag
import spacy
from collections import Counter
from helper import preprocess, compare, extract_nouns, get_similarity
from responses import responses, blank, menu_food, menu_price

word2vec = spacy.load("en_core_web_md")


def progress_bar():
    print("Paying ...")
    for i in range(101):
        time.sleep(0.02)
        i = i / 100.0
        bar_len = 20
        block = int(round(bar_len * i))
        text = "\r[{0}]".format("#" * block + "-" * (bar_len - block))
        sys.stdout.write(text)
        sys.stdout.flush()
    print(" Done ...\n")


class ChatBot:
    negatives = ("don't", "stop", "nothing")
    exits = ("bye", "see you", "quit", "pause", "exit", "goodbye", "later", "no")

    def __init__(self):
        self.matching = {"pay_bill": [r".*(want|need)?.*pay.*(the|my)? bill.*", r".*get.*(the|my)? bill.*"],
                         "menu": [r".*(can|could)?.*(have|see|bring)?.*(the)?.* menu.*",
                                  r".*what.*you.*recommend.*"]}
        self.customer = ""
        self.bill_amount = 0

    def welcome(self):
        self.customer = input("Hey, my name is Blooooop. Could you tell me your name, please?\n> ")

        task = input(f"Hey {self.customer}, what can I help you with?\n> ").lower()

        if task in self.negatives:
            answer = input("Are you sure you don't need my help? [yes|no]\n> ")
            if answer.lower() == "yes":
                print("Okay, have a nice day!")
                return
            else:
                task = input(f"What can I help you with, {self.customer}?\n> ").lower()

        self.handle_conversation(task)

    def handle_conversation(self, reply):
        while not self.exit_bot(reply):
            reply = self.respond(reply)

    def exit_bot(self, reply):
        for exit_ in self.exits:
            if exit_ in reply:
                print("Okay, have a nice day!")
                return True
        return False

    @staticmethod
    def find_match(reply, possible_responses):
        bow_user = Counter(preprocess(reply))
        bow_responses = [Counter(preprocess(response)) for response in possible_responses]
        similarity_list = [compare(bow_user, response) for response in bow_responses]
        idx = similarity_list.index(max(similarity_list))
        return possible_responses[idx]

    def respond(self, reply):
        for key, value in self.matching.items():
            for pattern in value:
                match = re.match(pattern, reply)
                if match and key == "pay_bill":
                    return self.show_billing_options()
                if match and key == "menu":
                    return self.show_menu()
        best_response = self.find_match(reply, responses)
        entity = self.find_entities(reply)
        print(best_response.format(entity))

        reply = input(f"Anything else, {self.customer}?\n> ")
        return reply

    @staticmethod
    def find_entities(reply):
        tagged_reply = pos_tag(preprocess(reply))
        nouns = extract_nouns(tagged_reply)
        tokens = word2vec(" ".join(nouns))
        category = word2vec(blank)
        result = get_similarity(tokens, category)

        result.sort(key=lambda x: x[2])
        if len(result) < 1:
            return blank
        else:
            return result[-1][0]

    def show_billing_options(self):
        pay_option = input(f"You can either pay with cash or by card.\nHow would you like to pay?\n> ")
        if pay_option.lower() == "cash":
            print("Alright. That's {}$ in total.".format(self.bill_amount))
            progress_bar()
            print(f"Thank you, {self.customer}")
            return input(f"Anything else, {self.customer}?\n> ")
        elif pay_option.lower() == "card":
            self.pay_bill()

    def pay_bill(self):
        card_number = input("Please enter your card number to pay the bill.\n> ")
        card_number = re.findall(r"\b\d+\b", card_number)
        progress_bar()
        print("Your credit card {} was charged with {}$".format(card_number, self.bill_amount))
        return input(f"Anything else, {self.customer}?\n> ")

    def show_menu(self):
        print("Here's the menu for you:\n")
        for food in zip(menu_food, menu_price):
            print(f"{food[0].capitalize()} for {food[1]}$")
        food_wish = input("\nWhat would you like to order?\n> ").lower()
        for word in food_wish.split():
            if word in menu_food:
                idx = menu_food.index(word)
                self.bill_amount += menu_price[idx]
                break
        else:
            print("Sorry, I didn't get that.")
            return self.show_menu()
        return input(f"Sure. Anything else, {self.customer}?\n> ")


bot = ChatBot()
bot.welcome()
