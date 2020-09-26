import configparser
from logging import getLogger

import mysql.connector

logger = getLogger(__name__)


class SensordbManager():
    def __init__(self, config_path, section):
        self.config = configparser.ConfigParser()
        self.config.read(config_path)
        self.section = section

        table = self.config.get(section, 'table')
        self.insert_sensor = ('insert into {} '
                              'values (null, %s, %s)').format(table)
        self.select_sensor = ('select id, room_id, host from {} '
                              'where room_id= %s').format(table)

    def register_sensor(self, room_id, host):
        try:
            cnx = self._connect()
            cur = cnx.cursor()
            cur.execute(self.insert_sensor, (room_id, host,))
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
            cnx = self._connect()
            cur = cnx.cursor()
            cur.execute(self.select_sensor, (room_id,))
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

    def _connect(self):
        cnx = mysql.connector.connect(
            host=self.config.get(self.section, 'host'),
            port=self.config.getint(self.section, 'port'),
            user=self.config.get(self.section, 'user'),
            password=self.config.get(self.section, 'password'),
            database=self.config.get(self.section, 'database')
        )
        return cnx
