from datetime import datetime

import pytz


class TimeHelper:
    @staticmethod
    def addTzInfo(dt):
        tzUTC = pytz.timezone('UTC')
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tzUTC)
        return dt

    @staticmethod
    def getUTCTime(dt: [datetime, None] = None) -> datetime:
        tzUTC = pytz.timezone('UTC')
        if not isinstance(dt, datetime):
            dt = datetime.now(tz=tzUTC)
        if dt.tzinfo is None:
            dt = dt.replace(tzinfo=tzUTC)
        return dt.astimezone(tz=tzUTC)

    @staticmethod
    def getLocalTime(dt: [datetime, None] = None) -> datetime:
        # TODO: configure time dynamically
        tz = pytz.timezone('Asia/Hong_Kong')

        dt = TimeHelper.getUTCTime(dt)
        return dt.astimezone(tz=tz)

    @staticmethod
    def getLocalTimeString(dt: datetime) -> str:
        tz = pytz.timezone('Asia/Hong_Kong')
        dt = TimeHelper.getUTCTime(dt)
        return str(dt.astimezone(tz=tz).isoformat())

    @staticmethod
    def formatTime(dt: [datetime, None] = None, fmt='%Y-%m-%d %H:%M') -> str:
        dt = TimeHelper.getLocalTime(dt)
        return dt.strftime(fmt)
