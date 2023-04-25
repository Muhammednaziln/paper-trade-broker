from apps.selector import Strategy


def ltp(symbol):
    LtpClass = Strategy().ltp_strategy()
    return LtpClass().ltp([symbol])


