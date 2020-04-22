import re
import random
import time
import sys


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


class SupportBot:
    negatives = ("don't", "stop", "nothing")
    exits = ("bye", "see you", "quit", "pause", "exit", "goodbye", "later", "no")
    bill_amount = round(random.uniform(12, 35), 2)

    def __init__(self):
        self.matching = {"how_to_pay": [r".*how.*pay.*(the)? bill.*",
                                        r".*where.*pay.*(the|my)? bill.*", ".*how.*pay.*"],
                         "pay_bill": [r".*want.*pay.*(the|my)? bill.*", r".*need.*pay.*(the|my)? bill.*"],
                         "menu": [r".*(can|could)?.*(have|see|bring)?.*(the)?.* menu.*"],
                         "bathroom": [r".*where.*bathroom.*"]}
        self.customer = ""

    def welcome(self):
        self.customer = input("Hey, my name is Blooooop. Could you tell me your name, please?\n> ")

        task = input(f"Hey {self.customer}, what can I help you with?\n> ")

        if task.lower() in self.negatives:
            answer = input("Are you sure you don't need my help? [yes|no]\n> ")
            if answer.lower() == "yes":
                print("Okay, have a nice day!")
                return
            else:
                task = input(f"What can I help you with, {self.customer}?\n> ")

        self.handle_conversation(task)

    def handle_conversation(self, reply):
        while not self.exit_bot(reply):
            reply = self.find_match(reply)

    def exit_bot(self, reply):
        for exit_ in self.exits:
            if exit_ in reply.lower():
                print("Okay, have a nice day!")
                return True
        return False

    def find_match(self, reply):
        for key, value in self.matching.items():
            for pattern in value:
                match = re.match(pattern, reply.lower())
                if match and key == "how_to_pay":
                    return self.show_billing_options()
                if match and key == "pay_bill":
                    return self.pay_bill()

        return input("Sorry, I didn't understand. Could you ask again differently?\n> ")

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


bot = SupportBot()
bot.welcome()
