import json

from manager.services import StringManagerService


class StringManager(StringManagerService):
    def __init__(self):
        self.default_locale = "en-us"
        self.cached_strings = {}
        self.refresh_cache()

    def refresh_cache(self) -> None:
        with open(f"manager/strings/{self.default_locale}.json") as f:
            self.cached_strings = json.load(f)

    def gettext(self, name) -> str:
        return self.cached_strings.get(name)
