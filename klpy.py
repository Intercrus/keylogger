from contracts import contract, new_contract


SEND_REPORT_EVERY = 60
TELEGRAM_BOT_TOKEN = ""
EMAIL = ""
EMAIL_PASSWORD = ""


@new_contract
def validationCheckReportMethod(s):
    if s not in ("email", "file", "telegram"):
        raise ValueError("report_method can only be one of these three:"
                         "email, telegram, file. Unacceptable %s" % s)


class Keylogger(object):
    @contract
    def __init__(self, interval=3600, report_method="telegram"):
        """
        :param interval: time interval between reports (in seconds)
        :param report_method: where to send report

        :type interval: int,>0
        :type report_method: str,validationCheckReportMethod
        """
        self.interval = interval
        self.report_method = report_method
        self.log = ""

    def callback(self):
        pass

    def dispatcher(self):
        pass

    def start(self):
        pass


def main():
    """

    :return:
    """
    keylogger = Keylogger(SEND_REPORT_EVERY, "email")
    keylogger.start()


if __name__ == "__main__":
    main()
