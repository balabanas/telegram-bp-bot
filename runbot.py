import os

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bpb.settings.local')
django.setup()

from bot.echobot import main


def run():
    main()


if __name__ == "__main__":
    run()
