"""this fils is made for
[*] Contain all strings outputs in one place
[*] Json file selected will be save in cache
[*] could Change Languages in app for not in demo

By default, uses 'en-us.json' file inside the 'strings' top-level folder.py
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
