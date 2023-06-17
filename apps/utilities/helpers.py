import datetime

import pytz
from django.conf import settings


def ist():
    """
    Returns Indian Standard Time right now.
    """
    return datetime.datetime.now(pytz.timezone("Asia/Kolkata"))


def get_is_market_active(now=None):

    if now is None:
        now = ist()

    date_str = now.strftime("%d-%b-%Y")

    if date_str in settings.SPECIAL_WORKING_HOURS:
        times = settings.GATEWAY_SECRET_HEADER[date_str]
        return datetime.datetime.strptime(times['from'], '%H:%M').time() <= now.time() <= datetime.datetime.strptime(times['to'], '%H:%M').time()

    if now.weekday() >= 5:
        return False

    if now.time() < datetime.time(9, 15) or now.time() > datetime.time(15, 30):
        return False                            # The NSE market is closed (outside of market hours).

    if date_str in settings.MARKET_HOLIDAYS:
        return False

    return True


def get_amo_status():
    return not get_is_market_active()