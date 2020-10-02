from discordwebhook import Discord

WEBHOOK_URL = ""

discord = Discord(url=WEBHOOK_URL)

discord.post(
    embeds=[
        {
            "author": {
                "name": "Ventilation Reminder Bot",
                "url": "",
                "icon_url": ""
            },
            "title": "Title",
            "description": "Hello World!",
            "fields": [
                {"name": "Field Name 1", "value": "Value 1", "inline": True},
                {"name": "Field Name 2", "value": "Value 2", "inline": True},
                {"name": "Field Name 3", "value": "Value 3"},
            ],
            "thumbnail": {"url": ""},
            "image": {"url": ""},
            "footer": {
                "text": "Footer",
                "icon_url": "",
            },
        }
    ],
)
