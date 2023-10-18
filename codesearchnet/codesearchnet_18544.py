def timestamp_to_datetime(timestamp):
        '''
        1514736000 --> datetime object

        :param int timestamp: unix timestamp (int)
        :return: datetime object or None
        :rtype: datetime or None
        '''

        if isinstance(timestamp, (int, float, str)):
            try:
                timestamp = float(timestamp)
                if timestamp.is_integer():
                    timestamp = int(timestamp)
            except:
                return None

            temp = str(timestamp).split('.')[0]
            if len(temp) == 13:
                timestamp = timestamp / 1000.0

            if len(temp) < 10:
                return None

        else:
            return None

        return datetime.fromtimestamp(timestamp)