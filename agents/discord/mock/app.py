import configparser
import datetime
import time
import sys
import logging

import requests
import embed
from discordwebhook import Discord

logging.basicConfig()
logger = logging.getLogger(__name__)

CONFIG_PATH = 'config.ini'
config = configparser.ConfigParser(interpolation=configparser.
                                   ExtendedInterpolation())
config.read(CONFIG_PATH)

greet = embed.Embed(CONFIG_PATH, 'greet')
greet.add_field(field={"name": "Notification interval",
                       "value": "Every {} hours {} minutes {} seconds."
                       .format(config.get('notification',
                                          'interval_hours'),
                               config.get('notification',
                                          'interval_minutes'),
                               config.get('notification',
                                          'interval_seconds'))})
ventilated = embed.Embed(CONFIG_PATH, 'ventilated')
not_ventilated = embed.Embed(CONFIG_PATH, 'not_ventilated')

activated = False
payload = {'password': config.get('room', 'password')}
td = datetime.timedelta(hours=config.getint('notification',
                                            'interval_hours'),
                        minutes=config.getint('notification',
                                              'interval_minutes'),
                        seconds=config.getint('notification',
                                              'interval_seconds'))
interval_sec = td.total_seconds()

discord = Discord(url=config.get('webhook', 'url'))

while True:
    try:
        response = requests.get(config.get('api', 'url'), params=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        logger.error("ventilation server: {}".format(e))
        time.sleep(5)
        continue
    else:
        sensors = response.json()

    if not activated:
        greet.add_field({"name": "Number of window",
                         "value": "{} windows.".format(len(sensors))})
        embeds = [greet.embed]
        activated = True
    else:
        count = 0
        for sensor in sensors.values():
            if sensor['state']['opened']:
                count += 1

        fields = []
        fields.append({"name": "Number of window",
                       "value": "{} windows.".format(len(sensors)),
                       "inline": True})
        fields.append({"name": "Opened windows",
                       "value": "{} windows.".format(count),
                       "inline": True})

        if count >= config.getint('notification', 'threshold_window_num'):
            ventilated.set_fields(fields)
            embeds = [ventilated.embed]
        else:
            not_ventilated.set_fields(fields)
            embeds = [not_ventilated.embed]

    try:
        response = discord.post(embeds=embeds)
        response.raise_for_status()
    except requests.exceptions.MissingSchema:
        logger.error('Discord webhook URL is invalid.')
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        logger.error("discord post: {}".format(e))
        logger.debug("post embeds: {}".format(embeds))
        time.sleep(5)
        continue

    time.sleep(interval_sec)
