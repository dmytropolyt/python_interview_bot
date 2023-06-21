import os

import django


if __name__ == '__main__':
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'interview_tg_bot.settings')
    django.setup()

    from telegram_bot.bot import run_bot
    run_bot()
