"""this file is made for
[*] Contain all strings outputs in one place
[*] Json file selected will be save in cache

By default, uses 'en-us.json'
"""
import json

default_locale = "en-us"
cached_strings = {}


def refresh():
    global cached_strings
    with open(f"{default_locale}.json") as f:
        cached_strings = json.load(f)


def gettext(name):
    return cached_strings[name]


refresh()
