import requests
import config


SUCCESS = 200
WRONG_API_KEY = 401
API_KEY_BLOCKED = 402
OVER_LIMIT = 404
MAX_TEXT_SIZE = 413
CANNOT_BE_TRANSLATED = 422
UNSUPPORTED_TRANSLATING_DIRECTION = 501


def translate(word, from_language, to_language):
    url = "https://translate.yandex.net/api/v1.5/tr.json/translate?" \
          "key=" + config.dict_key +\
          "&text=" + word + \
          "&lang=" + from_language + "-" + to_language

    dict_result = requests.get(url).json()

    if dict_result['code'] == SUCCESS:
        return dict_result['text'][0]
    else:
        return "ERROR"


