from django.contrib import admin
from django import forms
from pymongo import MongoClient
from bson.objectid import ObjectId

# Kết nối với MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client.QuanLyWebBanBanh
