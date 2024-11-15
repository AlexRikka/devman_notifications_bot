import logging
import os
import requests
import telegram
import time

from dotenv import load_dotenv
from telegram import ParseMode


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


def run_bot(bot, chat_id):
    info_text = """У вас проверили работу "{}" """ + \
        """([Ссылка на урок]({})).\n\n"""
    negative_text = 'К сожалению, в работе нашлись ошибки.'
    positive_text = 'Преподавателю все понравилось, можно приступать ' + \
        'к следующему уроку!'

    response = None
    timestamp_to_request = None
    devman_token = os.environ['DEVMAN_TOKEN']
    headers = {'Authorization': f'Token {devman_token}'}
    params = {'timestamp': timestamp_to_request}
    url = 'https://dvmn.org/api/long_polling/'

    logger.info('Бот запущен')

    while True:
        raw_response = None
        try:
            raw_response = requests.get(
                url, headers=headers, params=params, timeout=100)
            raw_response.raise_for_status()

        except requests.HTTPError as err:
            logger.warning("Ошибка обращения к dvmn.org")
            logger.warning(err)
            continue

        except requests.exceptions.ReadTimeout:
            continue

        except requests.exceptions.ConnectionError:
            print('Интернет соединение прервано. Ожидание соединения...')
            time.sleep(5)
            continue

        if not raw_response:
            continue

        response = raw_response.json()
        if response['status'] == 'timeout':
            timestamp_to_request = response['timestamp_to_request']
            continue

        if response['status'] == 'found':
            for lesson in response['new_attempts']:
                message_text = info_text \
                    .format(lesson['lesson_title'], lesson['lesson_url']) + \
                    negative_text if lesson['is_negative'] else positive_text

                bot.sendMessage(
                    chat_id=chat_id,
                    text=message_text,
                    parse_mode=ParseMode.MARKDOWN
                )


if __name__ == '__main__':
    load_dotenv()
    notifications_bot = telegram.Bot(
        token=os.environ['TG_NOTIFICATIONS_BOT_TOKEN'])
    log_bot = telegram.Bot(
        token=os.environ['TG_NOTIFICATIONS_LOG_BOT_TOKEN'])
    chat_id = os.environ['TG_CHAT_ID']

    logger = logging.getLogger('Logger')
    logger.setLevel(logging.INFO)
    logger.addHandler(TelegramLogsHandler(log_bot, chat_id))

    run_bot(notifications_bot, chat_id)
