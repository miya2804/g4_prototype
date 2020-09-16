import configparser
from logging import getLogger

import mysql.connector

logger = getLogger(__name__)


class SensordbManager():
    def __init__(self, config_path, section):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.section = section

    def regist_sensor(self, room_id, host):
        try:
            cnx = mysql.connector.connect(
                host=self.config.get(self.section, 'host'),
                port=self.config.getint(self.section, 'port'),
                user=self.config.get(self.section, 'user'),
                password=self.config.get(self.section, 'password'),
                database=self.config.get(self.section, 'database')
            )
            cur = cnx.cursor()
            cur.execute('insert into sensors values (null, %s, %s)',
                        (room_id, host))
            cnx.commit()
            id_ = cur.lastrowid
        except mysql.connector.Error:
            logger.debug('DB error.', exc_info=True)
            id_ = None
            success = False
        else:
            cur.close()
            cnx.close()
            success = True

        return id_, success

    def get_sensors(self, room_id):
        try:
            cnx = mysql.connector.connect(
                host=self.config.get(self.section, 'host'),
                port=self.config.getint(self.section, 'port'),
                user=self.config.get(self.section, 'user'),
                password=self.config.get(self.section, 'password'),
                database=self.config.get(self.section, 'database')
            )
            cur = cnx.cursor()
            cur.execute('select room_id,host from sensors where room_id= %s',
                        (room_id, ))
            sensors = cur.fetchall()
        except mysql.connector.Error:
            logger.debug('DB error.', exc_info=True)
            sensors = []
            success = False
        else:
            cur.close()
            cnx.close()
            success = True

        return sensors, success
