# Уведомления о проверке работ
Программа для получения статуса работ на курсах Девмана с помощью телеграм-бота.

## Окружение

### Требования
Для запуска программы вам понадобится Python 3.10. Скачайте репозиторий и установите python пакеты из `requirements.txt`:
```bash
git clone https://github.com/AlexRikka/devman_notifications_bot.git
cd devman_notifications_bot
pip install -r requirements.txt
```

### Переменные окружения
Часть настроек проекта берётся из переменных окружения. Чтобы их определить, создайте файл `.env` в корне проекта и добавьте в него следующие переменные:
- DEVMAN_TOKEN: персональный токен API Девмана
- TG_NOTIFICATIONS_BOT_TOKEN: токен основного телеграм бота, который присылает статусы работ.
- TG_NOTIFICATIONS_LOG_BOT_TOKEN: токен телеграм бота, который сообщает о состоянии основого бота.
- TG_CHAT_ID: chat_id чата пользователя с ботом, можно узнать через телеграм-бот @userinfobot

### Запуск
Запустите программу:
```
python bot.py
```


## Цель проекта
Код написан в образовательных целях на онлайн-курсе для веб-разработчиков dvmn.org.