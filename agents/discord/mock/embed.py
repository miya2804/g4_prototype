import configparser


class Embed():
    def __init__(self, config_path, section):
        self.config = configparser.ConfigParser(interpolation=configparser.
                                                ExtendedInterpolation())
        self.config.read(config_path)

        self.embed = {
            "color": self.config.get(section, 'color'),
            "author": {
                "name": self.config.get(section, 'author_name'),
                "icon_url": self.config.get(section, 'icon_url')
            },
            "title": self.config.get(section, 'title'),
            "description": self.config.get(section, 'description'),
            "fields": [],
            "image": {"url": self.config.get(section, 'image_url')},
        }

    def set_color(self, color):
        self.embed['color'] = color

    def set_description(self, description):
        self.embed['description'] = description

    def add_field(self, field):
        self.embed['fields'].append(field)

    def set_fields(self, fields):
        self.embed['fields'] = fields
