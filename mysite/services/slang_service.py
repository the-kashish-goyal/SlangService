import requests
import json


class Slang:

    @classmethod
    def get_slang(cls, word, lang):
        # Make a GET request to the Google Translate web API
        url = 'https://translate.google.co.in/translate_a/single'
        params = {
            'client': 'gtx',
            'sl': 'auto',  # Set the source language to 'auto' for auto-detection
            'tl': lang,  # Set the target language to the provided lang parameter
            'dt': 't',
            'q': word,
        }

        response = requests.get(url, params=params)
        data = json.loads(response.text)

        # Extract the translated slang text
        slang = data[0][0][0]
        return slang