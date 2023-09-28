import requests
from credentials import TELEGRAM_BOT_API_KEY, TELEGRAM_BOT_CHAT_ID

class Telegram:
    def __init__(self):
        self.bot_token = TELEGRAM_BOT_API_KEY
        self.bot_chat_id = TELEGRAM_BOT_CHAT_ID

    def send_message(self, message):
        send_text = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chat_id + '&parse_mode=Markdown&text=' + message

        response = requests.get(send_text)
        response.raise_for_status()
        return response.json()