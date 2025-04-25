from django.db import models
from pymongo import MongoClient

class Cake:
    def __init__(self, name, price, description, image):
        self.name = name
        self.price = price
        self.description = description
        self.image = image