import requests
import time
import sys
import telegram
import os
from dotenv import load_dotenv
from telegram import ParseMode


def main():
    load_dotenv()
    telegram_api_key = os.environ['TG_HTTP_TOKEN']
    bot = telegram.Bot(token=telegram_api_key)
    chat_id = os.environ['TG_CHAT_ID']

    response = None
    timestamp_to_request = None
    devman_token = os.environ['DEVMAN_TOKEN']
    headers = {'Authorization': f'Token {devman_token}'}
    params = {'timestamp': timestamp_to_request}
    url = 'https://dvmn.org/api/long_polling/'

    while True:
        raw_response = None
        try:
            raw_response = requests.get(
                url, headers=headers, params=params, timeout=100)
            raw_response.raise_for_status()

        except requests.HTTPError as err:
            print(*err, file=sys.stderr)
            continue

        except requests.exceptions.ReadTimeout:
            print('Сервер не ответил в течение указанного времени ожидания. ' +
                  'Повторный запрос.')
            continue

        except requests.exceptions.ConnectionError:
            print('Интернет соединение прервано. Ожидание соединения...')
            time.sleep(5)
            continue

        if raw_response:
            response = raw_response.json()
            if response['status'] == 'timeout':
                timestamp_to_request = response['timestamp_to_request']
            if response['status'] == 'found':
                for lesson in response['new_attempts']:
                    lesson_title = lesson['lesson_title']
                    if lesson['is_negative']:
                        bot.send_message(
                            chat_id=chat_id,
                            text=f"""У вас проверили работу "{lesson_title}" """ +
                            f"""([Ссылка на урок]({lesson['lesson_url']})).\n\n""" +
                            """К сожалению, в работе нашлись ошибки.""",
                            parse_mode=ParseMode.MARKDOWN
                        )
                    else:
                        bot.sendMessage(
                            chat_id=chat_id,
                            text=f"""У вас проверили работу "{lesson_title}" """ +
                            f"""([Ссылка на урок]({lesson['lesson_url']})).\n\n""" +
                            """Преподавателю все понравилось, можно приступать к следующему уроку!""",
                            parse_mode=ParseMode.MARKDOWN
                        )


if __name__ == '__main__':
    main()
