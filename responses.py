import random

response_1 = "The {} has a gluten-free option, but it is not vegan"
response_2 = "We have a selection of sides to go along with the {}, including mashed potatoes or fries."
response_3 = "{} includes habanero, so it is a bit spicy!"
response_4 = "{} costs " + str(int(random.uniform(12, 30)))
blank = "food"


responses = [response_1, response_2, response_3, response_4]