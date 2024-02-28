import glob
import json
from exception import UnknownLangCode, UnknownTranslationKey


class Translator:
    """
    Übersetzungsklasse mit automatischer Einlesung.
    Um eine neue Sprache hinzufügen, einfach eine neue .json Datei mit dem Language Code unter ./translations/languages
    erstellen.
    """
    def __init__(self, lang_code) -> None:
        self.locals = []
        self.lang_codes = []
        self.lang = lang_code

        for i in glob.glob(r".\translations\languages\*.json"):
            with open(i) as file:
                data = json.load(file)
                # TODO: Funktioniert evt. nicht unter Linux wegen Path Prefix
                data_lang_code = i.split("languages\\")[1].split(".")[0]
                self.locals.append([data_lang_code, data])
                self.lang_codes.append(data_lang_code)

        if lang_code not in self.lang_codes:
            raise UnknownLangCode

    def translate(self, key) -> str:
        """
        :param key: Übersetzungsschlüssel, z.B. "main.title"
        :return: übersetzter String
        """
        for i in self.locals:
            if i[0] == self.lang:
                return i[1][key]
        raise UnknownTranslationKey

    def change_lang(self, lang_code) -> None:
        # TODO: Checken ob lang_code valid ist.
        self.lang = lang_code

    def get_lang(self) -> str:
        """
        Gibt die momentan verwendete Sprache zurück
        :return: ISO Sprachcode, z.B. "de-DE"
        """
        return self.lang
